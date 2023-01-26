from django.db import models

class seccode_list(models.Model):
    """銘柄コ－ドリストモデル"""
    class Meta:
        db_table = 'seccode_list'

    # テ－ブルコラムに対応するテ－ブルを定義
    seccode = models.IntegerField(verbose_name='銘柄コード', primary_key=True)
    company_name = models.CharField(verbose_name='銘柄名', max_length=50)
    settlement_month = models.CharField(verbose_name='決済月', max_length=2)
    dividends_zenki = models.IntegerField(verbose_name='配当金（前期）')
    dividends_yosou = models.IntegerField(verbose_name='配当金（予想）')
    shares = models.IntegerField(verbose_name='発行済株式数')

    def __str__(self):
        return self.company_name

    def csv_import(self, file):
        """CSVファイルをインポートする"""
        import csv
        from io import TextIOWrapper

        reader = csv.reader(TextIOWrapper(file, encoding='utf-8'))
        count = 0
        for row in reader:
            if count == 0:
                count += 1  # ヘッダー行はスキップ
                continue
            else:
                self.objects.create(
                    seccode=row[0],
                    company_name=row[1],
                    settlement_month=row[2],
                    dividends_zenki=row[3],
                    dividends_yosou=row[4],
                    shares=row[5],
                )
