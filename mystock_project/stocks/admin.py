from django.contrib import admin
from .models import Stock, StockTradeInfo
# from .models import Stock

# Register your models here.

class StockAdmin(admin.ModelAdmin):
    list_display = ('stock_name', 'stock_number')
    # pass

class StockInfoAdmin(admin.ModelAdmin):
    list_display = ('stock_number', 'high_price')
    pass

admin.site.register(Stock, StockAdmin)
admin.site.register(StockTradeInfo, StockInfoAdmin)