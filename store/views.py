import os
import random
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import ProductForm
from .models import Product


def get_ai_tags(product_name, description, category):
    """Use OpenAI to auto-suggest tags for a product."""
    api_key = getattr(settings, 'OPENAI_API_KEY', '')
    if not api_key:
        return ''
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        prompt = (
            f"Suggest 3-5 short comma-separated tags for this product:\n"
            f"Name: {product_name}\nCategory: {category}\nDescription: {description}\n"
            f"Reply with only the tags, nothing else."
        )
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=60,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return ''


def product_list(request):
    products = list(Product.objects.all())

    # Simple AI recommender: suggest products from the same category as random picks
    recommendations = []
    if products:
        sample_size = min(3, len(products))
        recommendations = random.sample(products, sample_size)

    return render(request, 'store/product_list.html', {
        'products': products,
        'recommendations': recommendations,
    })


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            # AI-generated tags (Challenge Task)
            product.tags = get_ai_tags(product.name, product.description, product.category)
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form})
