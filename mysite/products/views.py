from django.shortcuts import render, get_object_or_404, redirect
from .models import product, Cart, Category
from .forms import productForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def products(request):
    search = request.GET.get("search")
    category = request.GET.get("category")

    if search:
        products = product.objects.filter(name__icontains=search)
    else:
        products = product.objects.all()

    if category:
        products = products.filter(category_id=category)
    paginator = Paginator(products, 5)
    page_number = request.GET.get("page")
    products = paginator.get_page(page_number)
    
    categories = Category.objects.all()

    return render(
        request,
        "products/products.html",
        {
            "products": products,
            "categories": categories
        }
    )


def about(request):
    return render(request, "products/about.html")


def product_detail(request, id):
    p = get_object_or_404(product, id=id)

    return render(
        request,
        "products/product_detail.html",
        {"p": p}
    )


@login_required
def add_product(request):
    if request.method == "POST":
        form = productForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()

            return redirect("products")

    else:
        form = productForm()

    return render(request, "products/add.html", {"form": form})


@login_required
def edit_product(request, id):
    item = product.objects.get(id=id, user=request.user)

    if request.method == "POST":
        form = productForm(request.POST, instance=item)

        if form.is_valid():
            form.save()
            return redirect("products")

    else:
        form = productForm(instance=item)

    return render(request, "products/edit.html", {"form": form})


@login_required
def delete_product(request, id):
    if request.method == "POST":
        item = get_object_or_404(
            product,
            id=id,
            user=request.user
        )
        item.delete()

    return redirect("products")


@login_required
def add_to_cart(request, id):
    item = get_object_or_404(product, id=id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=item,
        defaults={"quantity": 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("products")


@login_required
def cart_view(request):
    items = Cart.objects.filter(user=request.user)

    total = 0

    for item in items:
        total += item.product.price * item.quantity

    return render(
        request,
        "products/cart.html",
        {"items": items, "total": total}
    )


@login_required
def remove_from_cart(request, id):
    item = get_object_or_404(
        Cart,
        id=id,
        user=request.user
    )

    item.delete()

    return redirect("cart")


@login_required
def increase_cart(request, id):
    item = get_object_or_404(
        Cart,
        id=id,
        user=request.user
    )

    item.quantity += 1
    item.save()

    return redirect("cart")


@login_required
def decrease_cart(request, id):
    item = get_object_or_404(
        Cart,
        id=id,
        user=request.user
    )

    if item.quantity > 1:
        item.quantity -= 1
        item.save()

    return redirect("cart")



# change on test branch