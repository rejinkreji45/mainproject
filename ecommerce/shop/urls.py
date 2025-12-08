"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from shop import views
app_name = 'shop'
urlpatterns = [

    path("",views.CategoryView.as_view(),name="category"),
    path("product/<int:i>/",views.ProductView.as_view(),name="products"),
    path("productdetails/<int:i>/",views.ProductDetailView.as_view(),name="productdetails"),
    path("register/",views.RegisterView.as_view(),name="register"),
    path("login/",views.UserLoginView.as_view(),name="userlogin"),
    path("logout/",views.UserLogoutView.as_view(),name="userlogout"),
    path('addcategory', views.AddcategoryView.as_view(), name="addcategory"),
    path('addproduct', views.AddproductView.as_view(), name="addproduct"),
    path('addstock/<int:i>/', views.AddstockView.as_view(), name="addstock"),
]
from django.conf.urls.static import static
from django.conf import settings

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
