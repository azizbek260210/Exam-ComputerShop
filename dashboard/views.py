from io import BytesIO
from msilib.schema import File
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Sum
from datetime import datetime, timezone
from django.http import HttpResponse
import qrcode
from main import models

# ---------CATEGORY-------------

@login_required(login_url='log_in')
def category_list(request):
    categories = models.Category.objects.all()
    return render(request, 'dashboard/category/list.html', {'categories': categories})

@login_required(login_url='log_in')
def category_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        models.Category.objects.create(name=name)
        return redirect('category_list')
    return render(request, 'dashboard/category/create.html')

@login_required(login_url='log_in')
def category_update(request, id):
    category = get_object_or_404(models.Category, id=id)
    if request.method == 'POST':
        name = request.POST.get('name')
        category.name = name
        category.save()
        return redirect('category_list')
    return render(request, 'dashboard/category/update.html', {'category': category})

@login_required(login_url='log_in')
def category_delete(request, id):
    category = get_object_or_404(models.Category, id=id)
    category.delete()
    return redirect('category_list')

# ---------PRODUCT-------------
@login_required(login_url='log_in')
def create_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        category = get_object_or_404(models.Category, id=category_id)
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        image = request.FILES.get('image')
        
        product = models.Product.objects.create(
            name=name, 
            category=category, 
            description=description,
            price=price, 
            quantity=quantity, 
            image=image
        )
        return redirect('product_list')
    else:
        categories = models.Category.objects.all()
        return render(request, 'dashboard/product/create.html', {'categories': categories})


@login_required(login_url='log_in')
def product_list(request):
    categories = models.Category.objects.all()
    category_code = request.GET.get('code')

    filter_items = {}
    if category_code:
        filter_items['product__category__code'] = category_code

    for key, value in request.GET.items():
        if value and not value == '0':
            if key == 'start_date':
                key = 'created_at__gte'
            elif key == 'end_date':
                key = 'created_at__lte'
            elif key == 'name':
                key = 'product__name__icontains'
            filter_items[key] = value

    products = models.Product.objects.filter(**filter_items)
    context = {
        'products': products,
        'categories': categories,
        'category_code': category_code,
    }
    return render(request, 'product/list.html', context)
    

@login_required(login_url='log_in')
def delete_product(request, id):
    product = get_object_or_404(models.Product, id=id)
    product.delete()
    return redirect('product_list')

@login_required(login_url='log_in')
def update_product(request, id):
    product = get_object_or_404(models.Product, id=id)
    categories = models.Category.objects.all()
    if request.method == 'POST':
        product.name = request.POST['name']
        product.category_id = request.POST['category']
        product.price = request.POST['price']
        product.quantity = request.POST['quantity']
        if 'image' in request.FILES:
            product.image = request.FILES['image']
        product.save()
        return redirect('product_list')
    return render(request, 'dashboard/product/update.html', {'product': product, 'categories': categories})

@login_required(login_url='log_in')
def product_detail(request, id):
    product = get_object_or_404(models.Product, id=id)
    return render(request, 'dashboard/product/detail.html', {'product': product})

# ---------ENTER PRODUCT-------------

@login_required(login_url='log_in')
def create_enter_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        product = get_object_or_404(models.Product, id=product_id)
        models.EnterProduct.objects.create(product=product, quantity=quantity)
        return redirect('enter_product_list')
    else:
        products = models.Product.objects.all()
        return render(request, 'dashboard/enter_product/create.html', {'products': products})

@login_required(login_url='log_in')
def enter_product_detail(request, id):
    enter_product = get_object_or_404(models.EnterProduct, id=id)
    return render(request, 'dashboard/enter_product/detail.html', {'enter_product': enter_product})

@login_required(login_url='log_in')
def enter_product_list(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    enter_products = models.EnterProduct.objects.all()

    if start_date and end_date:
        enter_products = enter_products.filter(entered_at__range=[start_date, end_date])

    return render(request, 'dashboard/enter_product/list.html', {'enter_products': enter_products})

# ---------SELL PRODUCT-------------

@login_required(login_url='log_in')
def sell_product_list(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    sell_products = models.SellProduct.objects.all()

    if start_date and end_date:
        sell_products = sell_products.filter(sold_at__range=[start_date, end_date])

    return render(request, 'dashboard/sell_product/list.html', {'sell_products': sell_products})

@login_required(login_url='log_in')
def sell_product_detail(request, id):
    sell_product = get_object_or_404(models.SellProduct, id=id)
    return render(request, 'dashboard/sell_product/detail.html', {'sell_product': sell_product})

@login_required(login_url='log_in')
def sell_product_create(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        product = get_object_or_404(models.Product, id=product_id)
        models.SellProduct.objects.create(product=product, quantity=quantity)
        return redirect('sell_product_list')
    else:
        products = models.Product.objects.all()
        return render(request, 'dashboard/sell_product/create.html', {'products': products})

@login_required(login_url='log_in')
def sell_product_update(request, id):
    sell_product = get_object_or_404(models.SellProduct, id=id)
    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = request.POST.get('quantity')
        refunded = request.POST.get('refunded', False)
        sell_product.product_id = product_id
        sell_product.quantity = quantity
        sell_product.refunded = refunded
        sell_product.save()
        return redirect('sell_product_list')
    return render(request, 'dashboard/sell_product/update.html', {'sell_product': sell_product})

# ---------REFUND-------------

@login_required(login_url='log_in')
def refund(request, id):
    sell_product = get_object_or_404(models.SellProduct, id=id)
    if not sell_product.refunded:
        if not models.Refund.objects.filter(sell_product=sell_product).exists():
            models.Refund.objects.create(sell_product=sell_product)
            sell_product.refunded = True
            sell_product.save()
            return HttpResponse("Mahsulot to`lovi muvaffaqiyatli qaytarildi.")
    return HttpResponse("Mahsulot allaqachon qaytarilgan.")

@login_required(login_url='log_in')
def refund_list(request):
    refunds = models.Refund.objects.all()
    return render(request, 'dashboard/refund/list.html', {'refunds': refunds})

@login_required(login_url='log_in')
def refund_detail(request, id):
    refund = get_object_or_404(models.Refund, id=id)
    return render(request, 'dashboard/refund/detail.html', {'refund': refund})

# ---------KIRIM CHIQIMLARNI HISOBLASH-------------

@login_required(login_url='log_in')
def filter(request):
    return render(request, 'dashboard/filter/filter.html')

@login_required(login_url='log_in')
def filter_entries(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return render(request, 'error.html', {'message': 'Sanalar noto\'g\'ri formatda'})

        entries = models.EnterProduct.objects.filter(entered_at__gte=start_date, entered_at__lte=end_date)
        total_entries = entries.count()
        total_entries_price = entries.aggregate(Sum('price'))['price__sum'] or 0
        sales = models.SellProduct.objects.filter(sold_at__gte=start_date, sold_at__lte=end_date)
        total_sales = sales.count()
        total_sales_price = sales.aggregate(Sum('price'))['price__sum'] or 0
        total_expenses = sales.aggregate(Sum('price'))['price__sum'] or 0
        total_profit = total_entries_price - total_expenses

        if total_entries == 0 and total_sales == 0:
            return HttpResponse("Belgilangan sana oralig'ida hech qanday yozuv kiritilmagan.")

        context = {
            'entries': entries,
            'total_entries': total_entries,
            'total_entries_price': total_entries_price,
            'total_sales': total_sales,
            'total_sales_price': total_sales_price,
            'total_expenses': total_expenses,
            'total_profit': total_profit,
        }

        return render(request, 'dashboard/filter/filter.html', context)

# ---------INDEX AND AUTH-------------

@login_required(login_url='log_in')
def index(request):
    categories = models.Category.objects.all()
    products = models.Product.objects.all()
    returns = models.Refund.objects.all()
    sales = models.SellProduct.objects.all()
    context = {
        'categories': categories,
        'products': products,
        'returns': returns,
        'sales': sales,
    }
    return render(request, 'dashboard/index.html', context)

def log_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'dashboard/auth/login.html', {'form': form})


@login_required(login_url='log_in')
def log_out(request):
    logout(request)
    return redirect('log_in')
