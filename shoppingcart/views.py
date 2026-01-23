from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import PaymentForm
from .models import ShoppingCart, ShoppingCartItem


def show_shopping_cart(request):
    # ---------- POST ACTIONS ----------
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("/accounts/login/")

        cart = ShoppingCart.objects.filter(myuser=request.user).first()

        if not cart:
            return redirect("shopping_cart_show")

        # Empty entire cart
        if "empty" in request.POST:
            cart.delete()
            return redirect("shopping_cart_show")

        # Remove ONE item (decrement quantity or delete row)
        if "remove_item" in request.POST:
            item_id = request.POST.get("remove_item")

            item = get_object_or_404(
                ShoppingCartItem,
                id=item_id,
                shopping_cart=cart
            )

            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                item.delete()

            return redirect("shopping_cart_show")

        # Go to payment
        if "pay" in request.POST:
            return redirect("shopping_cart_pay")

        return redirect("shopping_cart_show")

    # ---------- GET ----------
    shopping_cart_is_empty = True
    shopping_cart_items = None
    total = Decimal("0.00")

    if request.user.is_authenticated:
        cart = ShoppingCart.objects.filter(myuser=request.user).first()
        if cart:
            shopping_cart_is_empty = False
            shopping_cart_items = ShoppingCartItem.objects.filter(
                shopping_cart=cart)
            total = cart.get_total()

    context = {
        "shopping_cart_is_empty": shopping_cart_is_empty,
        "shopping_cart_items": shopping_cart_items,
        "total": total,
    }
    return render(request, "shopping_cart.html", context)


@login_required(login_url="/accounts/login/")
def pay(request):
    shopping_cart_is_empty = True
    paid = False
    form = None

    cart = ShoppingCart.objects.filter(myuser=request.user).first()

    if request.method == "POST":
        form = PaymentForm(request.POST)
        form.instance.myuser = request.user

        if form.is_valid():
            form.save()
            paid = True

            if cart:
                cart.delete()
        else:
            print(form.errors)

    else:  # GET
        if cart:
            shopping_cart_is_empty = False
            form = PaymentForm(initial={"amount": cart.get_total()})

    context = {
        "shopping_cart_is_empty": shopping_cart_is_empty,
        "payment_form": form,
        "paid": paid,
    }
    return render(request, "pay.html", context)
