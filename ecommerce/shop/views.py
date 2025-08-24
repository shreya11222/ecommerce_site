from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem, Order, OrderItem
from .form import SignUpForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Product, Review
from django.contrib.auth.decorators import login_required
from .form import ReviewForm
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages



def home(request):
    return render(request, 'shop/home.html')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'shop/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'shop/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
def about_view(request):
    return render(request, 'shop/about.html')
def contact_view(request):
    return render(request, 'shop/contact.html')
def about(request):
    return render(request, 'shop/about.html')


@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    return render(request, 'shop/cart_detail.html', {'cart': cart, 'items': items})

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_detail')

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if request.method == 'POST':
        address = request.POST.get('address')
        if not address:
            return render(request, 'shop/checkout.html', {'cart': cart, 'error': 'Address required!'})

        order = Order.objects.create(user=request.user, delivery_address=address)
        for item in cart.items.all():
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
        cart.delete()

        return render(request, 'shop/order_confirmation.html', {'order': order})

    return render(request, 'shop/checkout.html', {'cart': cart})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart, CartItem, Order, OrderItem
from django.shortcuts import render, redirect
from .form import SignUpForm
from django.contrib.auth import login, authenticate


@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if request.method == 'POST':
        address = request.POST.get('address')
        if not address:
            return render(request, 'shop/checkout.html', {'cart': cart, 'error': 'Please enter a delivery address.'})
        
        order = Order.objects.create(user=request.user, delivery_address=address)
        for item in cart.items.all():
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
        cart.delete()  # Clear cart after order placed

        return render(request, 'shop/order_confirmation.html', {'order': order})

    return render(request, 'shop/checkout.html', {'cart': cart})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically log user in after signup
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home after signup
    else:
        form = SignUpForm()
    return render(request, 'shop/signup.html', {'form': form})



@staff_member_required
def admin_product_add(request):
    # Code to add new product, only accessible by admin
    pass

@staff_member_required
def admin_order_list(request):
    # Code to view all orders, only accessible by admin
    pass

from django.contrib.auth.decorators import login_required

@login_required
def cart_detail(request):
    # Cart viewing logic here
    pass


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import Product
from .form import ProductForm

@staff_member_required
def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'shop/product_form.html', {'form': form})

@staff_member_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop/product_form.html', {'form': form})

@staff_member_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'shop/product_confirm_delete.html', {'product': product})
def product_list(request):
    query = request.GET.get('search', '')
    products = Product.objects.all()
    if query:
        products = products.filter(name__icontains=query)
    return render(request, 'shop/product_list.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = product.reviews.order_by('-created_at')

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.product = product
                review.save()
        else:
            return redirect('login')
    else:
        form = ReviewForm()

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form,
    })
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from django.contrib.auth.decorators import login_required

@login_required
def cart_detail(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(pk__in=cart.keys())
    
    cart_items = []
    total = 0
    for product in products:
        quantity = cart.get(str(product.pk), 0)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
    
    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total': total})

@login_required
def add_to_cart(request, pk):
    cart = request.session.get('cart', {})
    cart[str(pk)] = cart.get(str(pk), 0) + 1
    request.session['cart'] = cart
    return redirect('cart_detail')

@login_required
def update_cart(request, pk):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        if quantity > 0:
            cart[str(pk)] = quantity
        else:
            cart.pop(str(pk), None)
        request.session['cart'] = cart
    return redirect('cart_detail')

@login_required
def remove_from_cart(request, pk):
    cart = request.session.get('cart', {})
    cart.pop(str(pk), None)
    request.session['cart'] = cart
    return redirect('cart_detail')
def home(request):
    featured_products = Product.objects.filter(stock_quantity__gt=0)[:6]
    return render(request, 'shop/home.html', {'featured_products': featured_products})
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        msg = request.POST.get('message')

        # Simple email sending example
        send_mail(
            f'Message from {name} ({email})',
            msg,
            settings.DEFAULT_FROM_EMAIL,
            [settings.CONTACT_EMAIL],
            fail_silently=False,
        )
        messages.success(request, "Your message has been sent!")
        return redirect('contact')

    return render(request, 'shop/contact.html')
from .models import Product

def cart_detail(request):
    cart = request.session.get('cart', {})
    
    products = Product.objects.filter(pk__in=cart.keys())
    cart_items = []
    total = 0
    for product in products:
        quantity = cart.get(str(product.pk), 0)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
    
    suggested_products = Product.objects.exclude(pk__in=cart.keys())[:4]  # 4 suggested products
    
    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total': total,
        'suggested_products': suggested_products,
    })
from .models import DiscountCode

def cart_detail(request):
    cart = request.session.get('cart', {})
    discount_code = None
    discount_percent = 0
    discount_amount = 0

    if request.method == 'POST':  # Apply discount code form
        entered_code = request.POST.get('discount_code', '').strip()
        try:
            discount_code_obj = DiscountCode.objects.get(code__iexact=entered_code, active=True)
            request.session['discount_code'] = discount_code_obj.code
        except DiscountCode.DoesNotExist:
            request.session['discount_code'] = None
    
    saved_code = request.session.get('discount_code', None)
    if saved_code:
        try:
            discount_code = DiscountCode.objects.get(code__iexact=saved_code, active=True)
            discount_percent = discount_code.discount_percent
        except DiscountCode.DoesNotExist:
            discount_percent = 0
            request.session['discount_code'] = None

    products = Product.objects.filter(pk__in=cart.keys())
    cart_items = []
    total = 0
    for product in products:
        quantity = cart.get(str(product.pk), 0)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    discount_amount = total * (discount_percent / 100)
    total_after_discount = total - discount_amount

    suggested_products = Product.objects.exclude(pk__in=cart.keys())[:4]

    context = {
        'cart_items': cart_items,
        'total': total,
        'discount_code': discount_code,
        'discount_amount': discount_amount,
        'total_after_discount': total_after_discount,
        'suggested_products': suggested_products,
    }
    return render(request, 'shop/cart.html', context)
from django.shortcuts import render, redirect
from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Product, Order, OrderItem, DiscountCode

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

def cart_detail(request):
    cart = request.session.get('cart', {})
    discount_code = None
    discount_percent = 0

    if request.method == 'POST':
        code_entered = request.POST.get('discount_code', '').strip()
        try:
            dc = DiscountCode.objects.get(code__iexact=code_entered, active=True)
            request.session['discount_code'] = dc.code
        except DiscountCode.DoesNotExist:
            request.session['discount_code'] = None
            messages.error(request, "Invalid discount code.")

    saved_code = request.session.get('discount_code', None)
    if saved_code:
        try:
            discount_code = DiscountCode.objects.get(code__iexact=saved_code, active=True)
            discount_percent = discount_code.discount_percent
        except DiscountCode.DoesNotExist:
            discount_percent = 0
            request.session['discount_code'] = None

    products = Product.objects.filter(pk__in=cart.keys())
    cart_items = []
    total = 0
    for product in products:
        qty = cart.get(str(product.pk), 0)
        subtotal = product.price * qty
        total += subtotal
        cart_items.append({'product': product, 'quantity': qty, 'subtotal': subtotal})

    discount_amount = total * (discount_percent / 100)
    total_after_discount = total - discount_amount

    suggested_products = Product.objects.exclude(pk__in=cart.keys())[:4]

    context = {
        'cart_items': cart_items,
        'total': total,
        'discount_code': discount_code,
        'discount_amount': discount_amount,
        'total_after_discount': total_after_discount,
        'suggested_products': suggested_products,
    }
    return render(request, 'shop/cart.html', context)

@transaction.atomic
def place_order(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect('product_list')

    try:
        order = Order.objects.create(user=request.user, delivery_address=request.POST.get('address'))
        for product_id, qty in cart.items():
            product = Product.objects.select_for_update().get(pk=product_id)
            if product.stock_quantity < qty:
                raise ValidationError(f"Not enough stock for {product.name}.")
            product.stock_quantity -= qty
            product.save()
            OrderItem.objects.create(order=order, product=product, quantity=qty)
        request.session['cart'] = {}
        messages.success(request, "Order placed successfully!")
        return redirect('order_confirmation')
    except ValidationError as e:
        messages.error(request, str(e))
        return redirect('cart_detail')
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Product, Cart, CartItem, Order, OrderItem, DiscountCode

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

def cart_detail(request):
    cart = None
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        messages.error(request, "Please log in to view your cart.")
        return redirect('login')

    cart_items = cart.items.select_related('product').all()
    total = sum(item.product.price * item.quantity for item in cart_items)

    discount_code = None
    discount_percent = 0
    discount_amount = 0
    total_after_discount = total

    if request.method == 'POST':
        code_entered = request.POST.get('discount_code', '').strip()
        if code_entered:
            try:
                discount_code_obj = DiscountCode.objects.get(code__iexact=code_entered, active=True)
                discount_code = discount_code_obj
                discount_percent = discount_code.discount_percent
                messages.success(request, f"Discount code '{code_entered}' applied!")
            except DiscountCode.DoesNotExist:
                messages.error(request, "Invalid discount code.")

    if discount_percent > 0:
        discount_amount = total * (discount_percent / 100)
        total_after_discount = total - discount_amount

    context = {
        'cart_items': cart_items,
        'total': total,
        'discount_code': discount_code,
        'discount_amount': discount_amount,
        'total_after_discount': total_after_discount,
    }
    return render(request, 'shop/cart.html', context)

@transaction.atomic
def place_order(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to place an order.")
        return redirect('login')

    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.select_related('product').all()

    if not cart_items:
        messages.error(request, "Your cart is empty.")
        return redirect('product_list')

    if request.method == 'POST':
        delivery_address = request.POST.get('delivery_address', '').strip()
        if not delivery_address:
            messages.error(request, "Delivery address is required.")
            return redirect('cart_detail')

        try:
            with transaction.atomic():
                order = Order.objects.create(
                    user=request.user,
                    delivery_address=delivery_address
                )

                for item in cart_items:
                    product = Product.objects.select_for_update().get(pk=item.product.pk)
                    if product.stock_quantity < item.quantity:
                        raise ValidationError(f"Insufficient stock for {product.name}.")

                    product.stock_quantity -= item.quantity
                    product.save()

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item.quantity
                    )

                # Clear cart after order
                cart.items.all().delete()

                messages.success(request, "Order placed successfully!")
                return redirect('order_confirmation', order_id=order.id)

        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('cart_detail')

    return redirect('cart_detail')
from django.shortcuts import render, get_object_or_404
from .models import Product

def home(request):
    # For home, typically show featured or recent products
    featured_products = Product.objects.all()[:6]  # Or add a featured flag in model
    return render(request, 'shop/home.html', {'featured_products': featured_products})

def product_list(request):
    # Show full product catalog
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})
