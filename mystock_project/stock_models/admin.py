from django.contrib import admin
from .models import *

# Register your models here.

class StockModelAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'model_name')
    
class StockModelPredictAdmin(admin.ModelAdmin):
    list_display = ('model_number', 'stock_number', 'predicted_day')
    
class StockModelPredictDayAdmin(admin.ModelAdmin):
    list_display = ('model_number', 'predicted_day')

class StockModelDayAdmin(admin.ModelAdmin):
    list_display = ('model_number', 'current_day')
    
class StockModelTradeBlockAdmin(admin.ModelAdmin):
    list_display = ('model_number', 'stock_number')
    
admin.site.register(StockModel, StockModelAdmin)
admin.site.register(StockModelPredict, StockModelPredictAdmin)
admin.site.register(StockModelPredictDay, StockModelPredictDayAdmin)
admin.site.register(StockModelDay, StockModelDayAdmin)
admin.site.register(StockModelTradeBlock, StockModelTradeBlockAdmin)
