from django.shortcuts import render
from django.http import JsonResponse
from .forms import InstrumentFilterForm
from .models import Instrument
from django.template.loader import render_to_string

from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import ContactForm
from django.shortcuts import get_object_or_404

def index(request):
    return render(request, 'shop/index.html')

def productView(request, product_id):
    product = get_object_or_404(Instrument, instrument_id=product_id)
    return render(request, 'shop/product.html', {'product': product})

def ShopView(request):
    form = InstrumentFilterForm(request.GET)
    queryset = Instrument.objects.all()
    
    if form.is_valid():
        # Filtrare după model
        if form.cleaned_data.get('model'):
            queryset = queryset.filter(model__icontains=form.cleaned_data['model'])
        
        # Filtrare după preț
        if form.cleaned_data.get('min_price'):
            queryset = queryset.filter(price__gte=form.cleaned_data['min_price'])
        if form.cleaned_data.get('max_price'):
            queryset = queryset.filter(price__lte=form.cleaned_data['max_price'])
            
        # Filtrare după categorie
        if form.cleaned_data.get('category'):
            queryset = queryset.filter(category__instrument=form.cleaned_data['category'])
            
        # Filtrare după tip
        if form.cleaned_data.get('type'):
            queryset = queryset.filter(category__type=form.cleaned_data['type'])
            
        # Filtrare după rating
        if form.cleaned_data.get('min_rating'):
            queryset = queryset.filter(rating__gte=form.cleaned_data['min_rating'])
            
        # Sortare
        sort = form.cleaned_data.get('sort')
        if sort == 'price_low':
            queryset = queryset.order_by('price')
        elif sort == 'price_high':
            queryset = queryset.order_by('-price')
        elif sort == 'rating':
            queryset = queryset.order_by('-rating')

    print(queryset)
    context = {
        'form': form,
        'products': queryset,
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string(
            template_name='shop/products_list.html', 
            context=context,
            request=request
        )
        return JsonResponse({'html': html})
        
    return render(request, 'shop/shop.html', context)


def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'shop/contact.html', {'form': form})
