from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from django.db.models import Q, Avg

from products.forms import ProductForm, ProductUpdateForm
from products.models import Product, ProductImage
from settings import settings
from shoppingcart.models import ShoppingCart


# Create your views here.
def product_list(request):
    query = request.GET.get('q')
    rating = request.GET.get('rating')

    products = Product.objects.annotate(
        avg_rating=Avg('reviews__rating'),
    )
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    if rating:
        products = products.filter(
            avg_rating__gte=float(rating)
        )

    context = {
        'all_the_products': products,
        'fallback_image': settings.MEDIA_URL + 'product_images/default_image.jpeg',
        'query': query,
        'rating': rating,
    }
    return render(request, 'product_list.html', context)

def product_detail(request, **kwargs):
    product_id = kwargs['id']
    product = Product.objects.get(id=product_id)
    myuser = request.user
    if request.method == 'POST':
        print('Add to cart')
        ShoppingCart.add_product(myuser, product)

    context = {
        'product': product,
        'fallback_image': settings.MEDIA_URL + 'product_images/default_image.jpeg',
    }
    return render(request, 'product_detail.html', context)

@login_required
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        images = request.FILES.getlist('images')
        if form.is_valid():
            # form.instance.seller = request.user
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            for image in images:
                ProductImage.objects.create(
                    product = product,
                    image = image
                )
            # form.save()
            print("New product saved !")
        else:
            print(form.errors)
        return redirect('product_list')

    else:
        form = ProductForm()
        context = {'form': form}

    return render(request, 'product_create.html', context)

@login_required
def product_update(request, **kwargs):
    product_id = kwargs['id']
    product = Product.objects.get(id=product_id)
    if not(
        request.user == product.seller
        or request.user.is_staff
        or getattr(request.user, "is_cs", False)
    ):
        return HttpResponseForbidden("You are not allowed to edit this product.")

    if request.method == "POST":
        form = ProductUpdateForm(request.POST, instance=product)
        images = request.FILES.getlist('images')
        if form.is_valid():
            form.save()
            for image in images:
                ProductImage.objects.create(
                    product = product,
                    image = image
                )
            return redirect('product_detail', id=product_id)
    else:
        form = ProductUpdateForm(instance=product)

    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'product_edit.html', context)

@login_required
def product_delete(request, product_id):
    product = Product.objects.get(id=product_id)
    if not (
            request.user == product.seller
            or request.user.is_staff
            or getattr(request.user, "is_cs", False)
    ):
        return HttpResponseForbidden("You are not allowed to delete this product.")

    if request.method == "POST":
        product.delete()
        return redirect('product_list')

    return HttpResponseForbidden("Invalid request.")

@login_required
def product_image_delete(request, image_id):
    image = ProductImage.objects.get(id=image_id)
    product = image.product
    if not(
        request.user == product.seller
        or request.user.is_staff
        or getattr(request.user, "is_cs", False)
    ):
        return HttpResponseForbidden("You are not allowed to delete this image.")

    image.delete()
    return redirect('product_update', id=product.id)

def generate_pdf(request, product_id):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    product = Product.objects.get(id=product_id)
    p.drawString(100, 750, 'Product Details')
    p.drawString(100, 700, f'Name: {product.name}')
    p.drawString(100, 680, f'Description: {product.description}')
    p.drawString(100, 660, f'Price: {product.price} €')
    p.drawString(100, 640, f'Seller: {product.seller.username}')

    images = product.product_images.all()
    image_width = 150
    image_height = 150
    x = 100
    y = 620
    if not images.exists():
        images = ProductImage.objects.filter(image = 'product_images/default_image.jpeg')

    for image in images:
        try:
            img = ImageReader(image.image.path)
            # New page if not enough space
            if y - image_height < 50:
                p.showPage()
                y = 750

            p.drawImage(img, x, y - image_height,
                width=image_width,
                height=image_height,
                preserveAspectRatio=True,
                mask='auto'
            )

            x += image_width + 20

            # Wrap images to next row
            if x > 400:
                x = 100
                y -= image_height + 20

        except Exception as e:
            print(f"Could not load image: {e}")

    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f'{product.name}.pdf')
