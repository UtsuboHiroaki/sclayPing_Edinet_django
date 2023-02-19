from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView
from .models import SecCodeList, ScreeningList
from pathlib import Path

from .screening.rcs import cf_haitou_hiritsu


# Create your views here.
class SecCodeListV(ListView):
    model = SecCodeList
    template_name = 'sec_code_list.html'


class ScreeningListV(ListView):
    model = ScreeningList
    context_object_name = 'screening_lists'
    template_name = 'screening_list.html'

    def cf_div_ratio(self):
        """
        | 私のやりたいこと
        | 1. \decode\screeningにあるscreening_20221224083954.csvが他のサイトからダウンロードしたcsv
        | 2. 同一パッケージにあるrcs.pyのcf_haitou_hiritsuを使用してこの段階で調査対象の銘柄を絞り込んだbase_listを作成
        | 3. \seccode\models.pyのscreening_listクラスにおいてbase_listを基にした
        | screening_listsというデータベースを作成したい
        | 4. その後の利用目的としては調査対象であるbase_listと既に調査した銘柄リストの
        | 差分を抽出し今回の調査対象である銘柄リストを作成したいのが意図です
        | 2023/02/18の状況報告
        | cf_div_ratioは基のCSVファイルから条件に合わない銘柄を最初に除外するための関数です
        | table_createはbase_listを基にしたscreening_listsを作成する関数です
        | コンソ－ルメソッドを使用して一旦はscreening_listsを作成しました
        | 問題点等があればご指摘いただきたくお願いします
        """

        base_path = Path(__file__).parent
        csv_file_path = base_path / 'screening' / 'screening_20221224083954.csv'
        base_list = cf_haitou_hiritsu(csv_file_path)
        return base_list

    def __str__(self):
        return self.name

    def table_create(self, base_list):
        for row in base_list:
            screening_lists = ScreeningList.objects.create(
                seccode=int(row['銘柄コード']),
                company_name=row['会社名'],
                industry=row['業種'],
                priority_market=row['優先市場'],
                settlement_month=row['決算月'],
                accounting_standards=row['会計基準'],
                market_capitalization=int(row['時価総額'].replace(",", "")),
                ev_ebitda=float(row['EV/EBITDA']),
                dividends_zenki=int(float(row['配当金(前期)'])),
                dividends_yosou=int(float(row['配当金(会予)'])),
                dividend_yield=float(row['配当利回り(会予)']),
                own_capital_ratio=float(row['自己資本比率'].replace("-", "") or "0"),
                operating_cf=int(row['営業CF'].replace(",", "")),
                shares=int(float(row['発行済株式総数'].replace(",", ""))),
            )
        return screening_lists


class ScreeningListDeleteV(DeleteView):
    model = ScreeningList
    success_url = reverse_lazy('seccode:screening_list')
