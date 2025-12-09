from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render,redirect
from django.views import View

from shop.models import Category,Product
from shop.forms import SignupForm,StockForm



class CategoryView(View):
    def get(self, request):
        c=Category.objects.all()
        context = {'cat': c}
        return render(request,'categories.html',context)

class ProductView(View):
    def get(self,request,i):
        c=Category.objects.get(id=i)
        context={'category':c}
        return render(request,'products.html',context)

class ProductDetailView(View):
    def get(self,request,i):
        p=Product.objects.get(id=i)
        context={'product':p}
        return render(request,'productdetails.html',context)

class RegisterView(View):
    def post(self,request):
        form_instance = SignupForm(request.POST)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:userlogin')


    def get(self, request):
       form_instance = SignupForm()
       context = {'form': form_instance}
       return render(request, 'register.html', context)

from django.contrib.auth import authenticate,login,logout
from shop.forms import LoginForm
from django.contrib import messages
class UserLoginView(View):
    def post(self,request):
       form_instance = LoginForm(request.POST)
       if form_instance.is_valid():
        data = form_instance.cleaned_data
        u = data['username']
        p = data['password']
        user = authenticate(username=u, password=p)

        # if user:  # if user exists
        #     login(request, user)  # adds the user into current sessions
        #     return redirect('shop:category')
        # else:  # if user does not exist
        #     messages.error(request, "Invalid credentials.")
        #     return redirect('shop:userlogin')

        if user and user.is_superuser == True:
            login(request, user)
            return redirect('shop:category')
        elif user and user.is_superuser != True:
            login(request, user)
            return redirect('shop:category')

        else:
            messages.error(request, "invalid user credentials")
            return render(request, 'login.html', {'form': form_instance})
    def get(self,request):
        form_instance = LoginForm()
        context = {'form': form_instance}
        return render(request, 'login.html', context)

class UserLogoutView(View):
    def get(self,request):
            logout(request)  # remove the user from the  current session
            return redirect('shop:userlogin')

from django.utils.decorators import method_decorator
from shop.forms import CategoryForm,ProductForm
from django.contrib.auth.decorators import login_required


from django.http import HttpResponse
def admin_required(fun):
    def wrapper(request):
        if not request.user.is_superuser:
            return HttpResponse("not allowed")
        else:
            return fun(request)

    return wrapper
@method_decorator(admin_required,name="dispatch")
@method_decorator(login_required,name="dispatch")
class AddcategoryView(View):
    def post(self,request):
        form_instance=CategoryForm(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:category')
        else:
            print('error')
            return render(request,'addcategory.html',{'form':form_instance})
    def get(self, request):
        form_instance = CategoryForm()
        context = {'form': form_instance}
        return render(request, 'addcategory.html', context)
@method_decorator(admin_required,name="dispatch")
class AddproductView(View):
    def post(self,request):
        form_instance=ProductForm(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:category')
        else:
            print('error')
            return render(request,'addproducts.html',{'form':form_instance})
    def get(self, request):
        form_instance = ProductForm()
        context = {'form': form_instance}
        return render(request, 'addproducts.html', context)

class AddstockView(View):
    def post(self, request,i):
        p=Product.objects.get(id=i)
        form_instance = StockForm(request.POST, request.FILES,instance=p)
        if form_instance.is_valid():
            form_instance.save()
        return redirect('shop:category')


    def get(self, request,i):
        p = Product.objects.get(id=i)
        from_instance= StockForm(instance=p)
        context = {'form':from_instance}
        return render(request, 'addstock.html',context)

