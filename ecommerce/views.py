from django.http import  JsonResponse
from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from .forms import CustomUserForm
from django.contrib.auth import authenticate,login,logout
import json
from django.contrib.auth.decorators import login_required
def index(request):
    products=Product.objects.filter(trending=1)
    return render(request,'index.html',{'products':products})
def login_page(request):
    if request.user.is_authenticated:
        return redirect("index")
    else:
        if(request.method=="POST"):
            username=request.POST.get("username")
            password=request.POST.get("password")
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                messages.success(request,"You logged in successfully")
                return redirect('index')
            else:
                messages.error(request,"Invalid Username or Password")
                return redirect('login')
        return render(request,'login.html')
def navbar(request):
    return render(request,'navbar.html')
def register(request):
    data=CustomUserForm()
    if(request.method=='POST'):
        data=CustomUserForm(request.POST)
        if(data.is_valid):
            data.save()
            messages.success(request,"Registration success you can login now...")
            return redirect('login')
    return render(request,'register.html',{'form':data})

def collections(request):
    collections=Catagory.objects.filter(status=0)
    data={'collections':collections}
    return render(request,'collections.html',data)
def collectionview(request,name):
    if(Catagory.objects.filter(name=name,status=0)):
        products=Product.objects.filter(category__name=name)
        return render(request,'products/index1.html',{'products':products,'category__name':name})
    else:
        messages.warning(request,"No Such Catagory Found")
        return redirect("collections")
def products(request,cname,pname):
    if(Catagory.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
            products=Product.objects.filter(name=pname,status=0).first()
            return render(request,"products/product.html",{'products':products})
        else:
            messages.warning(request,"No Such Product Found")
            return redirect("collections")
    else:
        messages.warning(request,"No Such Catagory Found")
        return redirect("collections")
def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out Successfully")
    return redirect("index")
def cart_page(request):
  if request.user.is_authenticated:
    cart=Cart.objects.filter(user=request.user)
    return render(request,"cart.html",{"cart":cart})
  else:
    return redirect("register")



def add_cart(request):
     if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=data['product_qty']
            product_id=data['pid']
            #print(request.user.id)
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product Already in Cart'}, status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'Product Added to Cart'}, status=200)
                    else:
                        return JsonResponse({'status':'Product Stock Not Available'}, status=200)
        else:
            return JsonResponse({'status':'Login to Add Cart'}, status=200)
     else:
        return JsonResponse({'status':'Invalid Access'}, status=200)
def remove_fav(request,fid):
  item=Favourite.objects.get(id=fid)
  item.delete()
  return redirect("favviewpage")    
def remove(request,cid):
    cartitem=Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect('cart')
def favviewpage(request):
  if request.user.is_authenticated:
    fav=Favourite.objects.filter(user=request.user)
    return render(request,"fav.html",{"fav":fav})
  else:
    return redirect("register")
def fav_page(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_id=data['pid']
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if Favourite.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product Already in Favourite'}, status=200)
                else:
                    Favourite.objects.create(user=request.user,product_id=product_id)
                    return JsonResponse({'status':'Product Added to Favourite'}, status=200)
        else:
            return JsonResponse({'status':'Login to Add Favourite'}, status=200)
    else:
        return JsonResponse({'status':'Invalid Access'}, status=200)