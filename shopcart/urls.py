"""
URL configuration for shopcart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ecommerce import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('register',views.register,name='register'),
    path('login',views.login_page,name='login'),
    path('logout',views.logout_page,name="logout"),
    path('cart',views.cart_page,name="cart"),
    path('fav',views.fav_page,name="fav"),
    path('navbar',views.navbar,name="navbar"),
    path('collections',views.collections,name="collections"),
    path('collections/<str:name>',views.collectionview,name="collections"),
    path('collections/<str:cname>/<str:pname>',views.products,name="product_details"),
    path('add_cart',views.add_cart,name="add_cart"),
    path('remove/<str:cid>',views.remove,name="remove"),
    path('favviewpage',views.favviewpage,name='favviewpage'),
    path('remove_fav/<str:fid>',views.remove_fav,name="remove_fav"),
    
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)