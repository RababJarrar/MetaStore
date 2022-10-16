from django.shortcuts import render, redirect
from storeapp.models import Customer, Seller, Product, Product_category, Order, Order_item
from utils.views import Cart


def index(request):
    return redirect('/home')


def home(request):
    context = {}
    if 'seller_id' in request.session:
        seller = Seller.objects.get(id=request.session['seller_id'])
        if seller:
            context = {
                'seller': seller,
                'sellers': Seller.objects.all,
                'products': Product.objects.all(),
            }
    if 'customer_id' in request.session:
        user = Customer.objects.get(id=request.session['customer_id'])
        if user:
            context = {
                'user': user,
                'sellers': Seller.objects.all,
                'products': Product.objects.all(),

            }
    else:
        context = {
            'seller': None,
            'user': None,
            'sellers': Seller.objects.all,
            'products': Product.objects.all(),

        }
    return render(request, 'store/home.html', context)


def create_product(request):
    seller_id = request.session['seller_id']
    seller = Seller.objects.get(id=seller_id)
    category = request.POST.get('category')
    category = Product_category.objects.create(
        name=category
    )
    category.save()
    name = request.POST.get('name')
    price = request.POST.get('price')
    quantity = request.POST.get('quantity')
    description = request.POST.get('description')
    sale = request.POST.get('sale')
    image = request.FILES.get('image')
    new_product = Product.objects.create(
        name=name,
        quantity=quantity,
        category=category,
        description=description,
        price=price,
        sale=sale
    )
    if image:
        new_product.image = image
    new_product.seller.add(seller)
    new_product.save()
    return redirect('/store/seller')


def view_product(request, id):
    product = Product.objects.get(id=id)

    context = {
        'product': product,
        'cart': Cart(request)

    }
    return render(request, 'store/product.html', context)


def view_seller_profile(request, id):
    context = {
        'seller': Seller.objects.get(id=id)
    }
    return render(request, 'store/seller_profile.html', context)


def best_sellers(request):
    context = {
        'sellers': Seller.objects.all(),
        'products': Product.objects.all(),
    }
    return render(request, 'store/best_seller.html', context)


def all_products(request):
    context = {
        'sellers': Seller.objects.all(),
        'all_products': Product.objects.all(),
    }
    return render(request, 'store/all_products.html', context)


def view_sales(request):
    sales = Product.objects.all()
    sellers = Seller.objects.all()
    context = {
        'products_on_sales': sales,
        'sellers': sellers
    }
    return render(request, 'store/sales.html', context)


def customer_profile(request):
    if 'customer_id' in request.session:
        customer = Customer.objects.get(id=request.session['customer_id'])
        context = {
            'customer': customer,
            'orders': customer.orders.all(),
        }
        return render(request, 'store/customer.html', context)
    else:
        return redirect('/')


def seller_profile(request):
    if 'seller_id' in request.session:
        seller = Seller.objects.get(id=request.session['seller_id'])
        context = {
            'seller': seller,
            'categories': Product_category.objects.all()
        }
        return render(request, 'store/seller.html', context)
    else:
        return redirect(request.META.get('HTTP_REFERER'))


def add_profile_picture(request):
    if request.FILES.get('seller_image'):
        seller = Seller.objects.get(id=request.session['seller_id'])
        seller.picture = request.FILES.get('seller_image')
        seller.save()
        print(seller.picture)

    return redirect(request.META.get('HTTP_REFERER'))


""" cart functionality for adding items clearing the cart,
    increase, decrease Items and calculate the order
"""


def add_to_cart(request):
    cart = Cart(request)
    quantity = request.POST.get('quantity')
    product_id = request.POST.get('product_id')
    product = Product.objects.get(id=product_id)
    cart.add(product, quantity)
    return redirect('/store/cart')


def item_clear(request, id):
    item = Product.objects.get(id=id)
    cart = Cart(request)
    cart.remove(item)
    return redirect("/store/cart")


def update_cart(request):
    cart = Cart(request)
    quantity = request.post.get(quantity)
    product = Product.POST.get(id=request.POST.get('product_id'))


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("/store/cart")


def show_cart(request):
    cart = Cart(request)
    product_ids = cart.cart.keys()
    cart_items = Product.objects.filter(id__in=product_ids)
    context = {
        'cart': cart.cart,
        'items_in_cart': len(cart),
        'cart_items': cart_items,
        'total': cart.get_total_price(),
    }
    return render(request, 'store/cart.html', context)


# @login_required
def place_order(request):
    cart = Cart(request)
    if 'customer_id' in request.session:
        customer_id = request.session['customer_id']
        customer = Customer.objects.get(id=customer_id)
        total = cart.get_total_price()
        new_order = Order.objects.create(
            customer=customer,
            total=total
        )
        product_ids = cart.cart.keys()
        cart_items = Product.objects.filter(id__in=product_ids)
        for item in cart_items:
            new_item = Order_item.objects.create(product=item)
            new_item.save()
            new_order.item.add(new_item)
        new_order.save()
        customer.orders.add(new_order)
        return redirect('/store/customer_profile')


def about_page(request):
    return render(request, 'store/about.html')


def logout(request):
    request.session.clear()
    request.session.modified = True
    return redirect('/')


def test(request):

    return render(request, 'store/test.html')
