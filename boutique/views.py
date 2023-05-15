from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .decorators import stock_manager_required, shop_keeper_required, admin_required
from django.contrib import messages
from .models import Category, Size, Item, Purchase, Warehouse, Supplier, Sales
from .forms import *
from django.contrib.auth.views import LoginView


class loginView(LoginView):
    template_name = 'login.html'

def Home(request):
    if request.user.groups.filter(name="shop-keeper").exists() and request.user.is_superuser != True:
        if request.method == 'POST':
            form = SalesForm(request.POST)
            if form.is_valid():
                item_id = form.cleaned_data['item']
                quantity = form.cleaned_data['quantity']
                
                try:
                    item = Item.objects.get(item_id=item_id.item_id)
                except Item.DoesNotExist:
                    # Handle the case when the item doesn't exist
                    return redirect('sales')
                
                if item.quantity >= quantity:
                    item.quantity -= quantity
                    item.save()

                    sale = Sales.objects.create(item=item, quantity=quantity)
                    return redirect('home')
                else:
                    # Handle the case when there's not enough stock
                    return redirect('sales')
        else:
            form = SalesForm()
            items = Item.objects.all()
            print(items)
            context = {
                'form': form,
                'items': items
            }
            return render(request, 'shop.html', context)
    
    elif request.user.groups.filter(name="stock-Manager").exists() and request.user.is_superuser != True:
        return render(request, 'STOCK.html')
    elif request.user.is_superuser:
        return render(request, 'index.html')
    else:
        return render(request, 'login.html')

@user_passes_test(lambda user: user.is_authenticated)
@shop_keeper_required
def sales_view(request):
    if request.method == 'POST':
        form = SalesForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data['item']
            size = form.cleaned_data['size']
            attribute = form.cleaned_data['attribute']
            quantity = form.cleaned_data['quantity']
            if quantity <= item.quantity:
                item.quantity -= quantity
                item.save()
                seller = request.user.employee
                Sales.objects.create(item=item, size=size, attribute=attribute, quantity=quantity, seller=seller)
                messages.success(request, 'Item sold successfully')
                return redirect('sales')
            else:
                messages.error(request, 'Not enough stock')
                return redirect('sales')
    else:
        form = SalesForm()
        categories = Category.objects.all()
        sizes = Size.objects.all()
        items = Item.objects.filter(quantity__gt=0)
        context = {
            'categories': categories,
            'sizes': sizes,
            'items': items,
            'form': form
        }
        return render(request, 'sales.html', context)


@user_passes_test(lambda user: user.is_authenticated)
@stock_manager_required
def stock_count(request):
    warehouse = Warehouse.objects.get(manager=request.user)
    items = Item.objects.filter(supplier__address=warehouse.address)
    context = {
        'items': items
    }
    return render(request, 'stock_count.html', context)

@user_passes_test(lambda user: user.is_authenticated)
@admin_required
def purchase_item(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            item_id = form.cleaned_data['item']
            supplier_id = form.cleaned_data['supplier']
            quantity = form.cleaned_data['quantity']
            item = Item.objects.get(id=item_id)
            supplier = Supplier.objects.get(id=supplier_id)
            Purchase.objects.create(item=item, supplier=supplier, quantity=quantity)
            stock, created = Stock.objects.get_or_create(item=item)
            stock.quantity += int(quantity)
            stock.save()
            messages.success(request, 'Purchase successful')
            return redirect('purchase')
        else:
            messages.error(request, 'Invalid form data')
    else:
        form = PurchaseForm()
    suppliers = Supplier.objects.all()
    items = Item.objects.all()
    context = {
        'form': form,
        'suppliers': suppliers,
        'items': items
    }
    return render(request, 'purchase_item.html', context)

@user_passes_test(lambda user: user.is_authenticated)
@admin_required
def admin_dashboard(request):
    purchases = Purchase.objects.all()
    sales = Sales.objects.all()
    stock_count = Item.objects.aggregate(total_stock_count=sum('quantity'))['total_stock_count']
    context = {
        'purchases': purchases,
        'sales': sales,
        'stock_count': stock_count
    }
    return render(request, 'admin_dashboard.html', context)

