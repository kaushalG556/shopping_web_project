from django.shortcuts import render,redirect,HttpResponse
from django.views.generic import DetailView
from django.views import View 
from .models import Customer,Product,Cart,OrderPlaced
from .forms import UserRegisterForm,CustomerProfileForm
from django.contrib import messages 
from django.db.models import Q 
from django.http import JsonResponse 
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProductView(View):
    def get(self,request):
        totalitem=0
        topwears=Product.objects.filter(category='TW')
        bottomwears=Product.objects.filter(category='BW')
        mobiles=Product.objects.filter(category='M')
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
        return render(request,'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles,'totalitem':totalitem})
  
from django.shortcuts import render, get_object_or_404
from .models import Product

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'app/productdetail.html', {'product': product})
  
    
# class ProductDetailView(DetailView):
#     model = Product
#     template_name = 'app/productdetail.html' 
#     context_object_name = 'product'

# class ProductDetailView(View):
#         def get(self,request,pk):
#             product.objects.get(pk=pk)
#             item_already_in_cart=False
#             item_already_in_cart=Cart.objects.filter(Q(product=product.id)&
#                         Q(user=request.user)).exists()
#             return render(request,'app/productdetail.html',\
# {'product':product,'item_already_in_cart':item_already_in_cart})      
    
@login_required
def add_to_cart(request):
    
    user=request.user 
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()    
    return redirect('/cart')
@login_required
def show_cart(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0.0
        shipping_amount=70.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==user]
        if cart_product:
            for p in cart_product:
                tempamount=(p.quantity*p.product.discount_price)
                amount+=tempamount
                totalamount=amount+shipping_amount
            return render(request, 'app/addtocart.html',{'carts':cart,'totalamount':totalamount,'amount':amount,'totalitem':totalitem})
        else:
            return HttpResponse('<h1>EMPTY Cart</h1>')
        


login_required
def buy_now(request):
 return render(request, 'app/buynow.html')

@login_required
def address(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    add=Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary','totalitem':totalitem})
@login_required
def orders(request):
    op=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed':op})
@login_required
def mobile(request,data=None):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    if data==None:
        mobiles=Product.objects.filter(category='M')
    elif data=='vivo' or data=='samsung':
        mobiles=Product.objects.filter(category='M').filter(brand=data)
    elif data=='below':
        mobiles=Product.objects.filter(category='M').filter(discount_price__lt=10000)
    elif data=='above':
        mobiles=Product.objects.filter(category='M').filter(discount_price__gt=10000)
    return render(request, 'app/mobile.html',{'mobiles':mobiles,'totalitem':totalitem})

 
class customerregistration(View):
    def get(self,request):
        form=UserRegisterForm()
        return render(request,'app/customerregistration.html',{'form':form})
    def post(self,request):
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations! Registered Successfully..')
            form.save()
        return render(request,'app/customerregistration.html',{'form':form})
        
@login_required
def checkout(request):
    user=request.user
    add=Customer.objects.filter(user=user)
    cart_items=Cart.objects.filter(user=user)
    amount=0.0
    shipping_amount=70.0
    total_amount=0.0
    cart_product=[p for p in Cart.objects.all() if p.user==user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
            amount += tempamount
        totalamount = amount + shipping_amount
    return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items})


################################################
from django.contrib.auth import logout as auth_logout

def logout(request):
    auth_logout(request)
    return redirect('login')

    

########################################################
@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
        form=CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary','totalitem':totalitem})

    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            usr=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']  
            reg=Customer(user=usr,name=name,locality=locality,city=city,zipcode=zipcode)
            reg.save()
            messages.success(request,'congratulations!! Profile Updated Successfully...')
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
#######################################################
@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        try:
            c = Cart.objects.get(product_id=prod_id, user=request.user)
            c.quantity += 1
            c.save()
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Product not found in cart'})

        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
            amount += tempamount
        totalamount = amount + shipping_amount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)
#############################################################
@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        try:
            c = Cart.objects.get(product_id=prod_id, user=request.user)
            c.quantity -= 1
            c.save()
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Product not found in cart'})

        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
            amount += tempamount
        totalamount = amount + shipping_amount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)
####################################################################
@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        try:
            c = Cart.objects.get(product_id=prod_id, user=request.user)
            c.delete()
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Product not found in cart'})

        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
            amount += tempamount
        totalamount = amount + shipping_amount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)
    
#########################################################
@login_required
def payment_done(request):
    user=request.user 
    custid=request.GET.get('custid')
    customer=Customer.objects.get(id=custid)
    cart=Cart.objects.filter(user=user)
    for c in cart:
        quantity = c.quantity  # Fetch quantity from the Cart object
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=quantity).save()
        c.delete()
    return redirect('orders')

####################################################################

from django.db.models import Q

def search_products(request):
    query = request.GET.get('q', 'default_value')  
    products = []
    if query:
        products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    return render(request, 'app/search_result.html',{'products': products, 'query': query})

############################################################
def laptop(request,data=None):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    if data==None:
        laptops=Product.objects.filter(category='L')
    elif data=='dell' or data=='hp':
        laptops=Product.objects.filter(category='L').filter(brand=data)
    elif data=='below':
        laptops=Product.objects.filter(category='L').filter(discount_price__lt=30000)
    elif data=='above':
        laptops=Product.objects.filter(category='L').filter(discount_price__gt=50000)
    return render(request, 'app/laptop.html',{'laptops':laptops,'totalitem':totalitem})

