from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden

from products.models import Product
from reviews.forms import ReviewForm, ReviewReportForm
from reviews.models import Review, ReviewReport


@login_required
def review_create(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Check if the user already reviewed the product
    if Review.objects.filter(user=request.user, product=product).exists():
        return HttpResponseForbidden("You already reviewed this product.")

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            return redirect('product_detail', id=product.id)
        else:
            print(form.errors)
    else:
        form = ReviewForm()

    return render(request, 'review_create.html', {'form': form, 'is_edit': False})


@login_required
def review_edit(request, product_id, review_id):
    review = get_object_or_404(Review, id=review_id, product_id=product_id)
    if not (
        request.user == review.user
        or request.user.is_staff
        or getattr(request.user, "is_cs", False)
    ):
        return HttpResponseForbidden("You are not allowed to edit this Review.")

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('product_detail', id=review.product.id)
    else:
        form = ReviewForm(instance=review)

    context = {
        'form': form,
        'is_edit': True,
    }
    return render(request, 'review_create.html', context)


@login_required
def review_delete(request, product_id, review_id):
    review = get_object_or_404(Review, id=review_id, product_id=product_id)
    if not (
        request.user == review.user
        or request.user.is_staff
        or getattr(request.user, "is_cs", False)
    ):
        return HttpResponseForbidden("You are not allowed to delete this Review.")

    if request.method == 'POST':
        review.delete()
        return redirect('product_detail', id=product_id)
    return HttpResponseForbidden("Invalid request.")


@login_required
def review_vote(request, product_id, review_id, choice):
    review = get_object_or_404(Review, id=review_id, product_id=product_id)
    user = request.user
    choix = True if choice == 'up' else False
    review.vote(user, choix)
    return redirect('product_detail', id=product_id)


@login_required
def review_report(request, product_id, review_id):
    review = get_object_or_404(Review, id=review_id, product_id=product_id)

    # If already reported, show a styled page (instead of raw 403 text)
    already_reported = ReviewReport.objects.filter(
        reporter=request.user,
        review=review
    ).exists()

    if already_reported:
        return render(
            request,
            "review_report_already.html",
            {"review": review}
        )

    if request.method == 'POST':
        form = ReviewReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.review = review
            report.save()
            return redirect('product_detail', id=product_id)
        else:
            print(form.errors)
    else:
        form = ReviewReportForm()

    return render(request, 'review_report.html', {'form': form, 'review': review})


# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponseForbidden

# from products.models import Product
# from reviews.forms import ReviewForm, ReviewReportForm
# from reviews.models import Review


# @login_required
# def review_create(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     # Check if the user already reviewed the product
#     if Review.objects.filter(user=request.user, product=product).exists():
#         return HttpResponseForbidden("You already reviewed this product.")

#     if request.method == 'POST':
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.user = request.user
#             review.product = product
#             review.save()
#             return redirect('product_detail', id=product.id)
#         else:
#             print(form.errors)
#     else:
#         form = ReviewForm()

#     return render(request, 'review_create.html', {'form': form, 'is_edit': False})


# @login_required
# def review_edit(request, product_id, review_id):
#     review = get_object_or_404(Review, id=review_id, product_id=product_id)
#     if not (
#         request.user == review.user
#         or request.user.is_staff
#         or getattr(request.user, "is_cs", False)
#     ):
#         return HttpResponseForbidden("You are not allowed to edit this Review.")

#     if request.method == 'POST':
#         form = ReviewForm(request.POST, instance=review)
#         if form.is_valid():
#             form.save()
#             return redirect('product_detail', id=review.product.id)
#     else:
#         form = ReviewForm(instance=review)

#     context = {
#         'form': form,
#         'is_edit': True,
#     }
#     return render(request, 'review_create.html', context)


# @login_required
# def review_delete(request, product_id, review_id):
#     review = get_object_or_404(Review, id=review_id, product_id=product_id)
#     if not (
#         request.user == review.user
#         or request.user.is_staff
#         or getattr(request.user, "is_cs", False)
#     ):
#         return HttpResponseForbidden("You are not allowed to delete this Review.")

#     if request.method == 'POST':
#         review.delete()
#         return redirect('product_detail', id=product_id)
#     return HttpResponseForbidden("Invalid request.")


# @login_required
# def review_vote(request, product_id, review_id, choice):
#     review = get_object_or_404(Review, id=review_id, product_id=product_id)
#     user = request.user
#     choix = True if choice == 'up' else False
#     review.vote(user, choix)
#     return redirect('product_detail', id=product_id)


# @login_required
# def review_report(request, product_id, review_id):
#     review = get_object_or_404(Review, id=review_id, product_id=product_id)
#     if request.method == 'POST':
#         form = ReviewReportForm(request.POST)
#         if form.is_valid():
#             report = form.save(commit=False)
#             report.reporter = request.user
#             report.review = review
#             report.save()
#             return redirect('product_detail', id=product_id)
#         else:
#             print(form.errors)
#     else:
#         form = ReviewReportForm()

#     return render(request, 'review_report.html', {'form': form, 'review': review})
