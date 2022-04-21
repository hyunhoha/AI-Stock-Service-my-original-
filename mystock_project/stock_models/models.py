from django.db import models

# Create your models here.

class StockModel(models.Model):
    model_number = models.IntegerField(verbose_name="모델번호",
                                       primary_key=True,
                                       unique=True)
    model_name = models.CharField(verbose_name="모델명",
                                  max_length=12)
    description = models.TextField(verbose_name="상세정보")
    
class StockModelPredict(models.Model):
    model_number = models.ForeignKey(StockModel,
                                     verbose_name="모델번호",
                                     on_delete=models.CASCADE)
    stock_number = models.ForeignKey('stocks.Stock',
                                     on_delete=models.CASCADE,
                                     verbose_name="종목명")
    predicted_day = models.DateField(verbose_name="예측날짜")
    predicted_out = models.FloatField(verbose_name="예측결과")
    
class StockModelPredictDay(models.Model):
    model_number = models.ForeignKey(StockModel,
                                     verbose_name="모델번호",
                                     on_delete=models.CASCADE)
    predicted_day = models.DateField(verbose_name="예측날짜")
    predicted_day_out = models.TextField(verbose_name="당일예측결과")

class StockModelDay(models.Model):
    model_number = models.ForeignKey(StockModel,
                                     on_delete=models.CASCADE,
                                     verbose_name="모델번호")
    current_day = models.DateField(verbose_name="날짜")
    bought_items = models.CharField(verbose_name="당일매수종목",
                                    max_length=128)
    sold_items = models.CharField(verbose_name="당일매도종목",
                                  max_length=128)
    yields = models.FloatField(verbose_name="수익률")
    cash = models.IntegerField(verbose_name="총 자금")
    items = models.CharField(verbose_name="현재주식",
                             max_length=128)
    
class StockModelTradeBlock(models.Model):
    model_number = models.ForeignKey(StockModel,
                                     on_delete=models.CASCADE,
                                     verbose_name="모델번호")
    stock_number = models.ForeignKey('stocks.Stock',
                                     on_delete=models.CASCADE,
                                     verbose_name="종목명")
    current_day = models.DateField(verbose_name="날짜")
    trade_type = models.CharField(verbose_name="거래종류",
                                  max_length=5)
    price = models.IntegerField(verbose_name="가격")