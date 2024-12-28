from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the shop index.")


from django.shortcuts import render
from django.views.generic import ListView
from .models import Instrument, Category
from django.db.models import Q
from django.views.generic import ListView
from .models import Instrument, Category
from django.db.models import Q

class ShopListView(ListView):
    model = Instrument
    template_name = 'shop/shop.html'
    context_object_name = 'instruments'
    paginate_by = 9  

    def get_queryset(self):
        queryset = Instrument.objects.all()
        
        # Filtrare după categorie
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__instrument=category)
            
        # Filtrare după tip (electric/acoustic)
        type_filter = self.request.GET.get('type')
        if type_filter:
            queryset = queryset.filter(category__type=type_filter)
            
        # Sortare
        sort = self.request.GET.get('sort')
        if sort == 'price_low':
            queryset = queryset.order_by('price')
        elif sort == 'price_high':
            queryset = queryset.order_by('-price')
        elif sort == 'rating':
            queryset = queryset.order_by('-rating')
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = self.request.GET.get('category')
        context['current_type'] = self.request.GET.get('type')
        return context