from tkinter import CASCADE
from django.db import models

# Create your models here.

class Stock(models.Model):
    stock_number = models.CharField(max_length=10,
                                    unique=True, 
                                    verbose_name="종목번호", 
                                    primary_key=True)
    stock_name = models.CharField(max_length=20,
                                  unique=True, 
                                  verbose_name="종목명")
    
    def __str__(self):
        return self.stock_name

class StockTradeInfo(models.Model):
    # stock_number = models.ForeignKey(Stock, on_delete=models.CASCADE, verbose_name="종목번호", related_name='stock_number')
    stock_number = models.ForeignKey(Stock,
                                     on_delete=models.CASCADE,
                                     verbose_name="종목번호")
    price_dttm = models.DateTimeField(verbose_name="날짜")
    high_price = models.FloatField(verbose_name="고가")
    middle_price = models.FloatField(verbose_name="중가")
    low_price = models.FloatField(verbose_name="저가")
    end_price = models.FloatField(verbose_name="종가")
    volume = models.FloatField(verbose_name="거래량")
    
    # def __str__(self):
    #     return self.stock_number
    