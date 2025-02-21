from django.shortcuts import render, redirect
from rest_framework import generics, permissions
from rest_framework.generics import get_object_or_404
from django.db.models import Avg
from .models import Product
from .serializers import ProductSerializer
from .forms import ProductForm
from django.core.paginator import Paginator
from .services import get_product
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

def product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    avg_rating = product.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
    return render(request, 'products/product_detail.html', {
        'product': product,
        'avg_rating': avg_rating or 0
    })

def product_list_view(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

def product_detail_view(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

def add_product_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('products:product_list')
    else:
        form = ProductForm()
    return render(request, 'products/add_product.html', {'form': form})




def product_detail(request, product_id):
    product = get_product(product_id)
    return render(request, "product_detail.html", {"product": product})



def search_products(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query) if query else []
    return render(request, 'products/search_results.html', {'products': products, 'query': query})

