from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Review
from products.models import Product

def add_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if Review.objects.filter(product=product, user=request.user).exists():
        messages.error(request, 'Вы уже оставили отзыв для этого товара.')
        return redirect('products:product_detail', pk=product_id)

    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        comment = request.POST.get('comment')

        if rating not in range(1, 6):
            messages.error(request, 'Рейтинг должен быть от 1 до 5')
            return redirect('products:product_detail', product_id=product_id)

        Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            comment=comment
        )
        messages.success(request, 'Ваш отзыв успешно добавлен!')
        return redirect('products:product_detail', product_id=product_id)

    return render(request, 'reviews/add_review.html', {'product': product})
