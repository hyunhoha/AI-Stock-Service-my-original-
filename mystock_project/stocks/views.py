from django.shortcuts import render, redirect
from django.views.generic import ListView

from .models import StockTradeInfo

def homepage(request):
    return render(request, 'home.html')
    
class StockInfo(ListView):
    model = StockTradeInfo
    template_name = "stock_info.html"
    context_object_name = "stock_data"
    paginate_by = 25
    filtering = ""
    
    def get_queryset(self):
        qs = super().get_queryset()
        # print("Kwargs : ********* : ", kwargs)
        qs = qs.filter(stock_number=self.filtering)
        return qs
    
    def dispatch(self, request, *args, **kwargs):
        self.filtering = kwargs['stock_number']
        return super().dispatch(request, *args, **kwargs)