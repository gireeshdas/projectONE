
from django.shortcuts import render,redirect

# Create your views here.
from django.template import context
from django.views import View
from django.views.generic import CreateView,TemplateView,FormView,DetailView,ListView,DeleteView
from rest_framework.reverse import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from owner.models import Products,Carts,Order,Categories
from django.contrib import messages
from customer.decorators import signin_required
from django.utils.decorators import method_decorator

from customer import forms

class RegistrationView(CreateView):
    form_class = forms.RegistrationForm
    template_name = "registration.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        messages.success(self.request, "your account has been created")
        return super().form_valid(form)


class LoginView(FormView):
    template_name = "login.html"
    form_class = forms.LoginForm

    def post(self,request,*args,**kwargs):
        form=forms.LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            user=authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                if request.user.is_superuser:
                    return redirect("dashboard")
                else:
                    return redirect("home")
        else:
            return render(request,"login.html",{"forms":form})


@method_decorator(signin_required,name="dispatch")
class HomeView(TemplateView):
    template_name = "home.html"


    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        all_products=Products.objects.all()
        context["products"]=all_products
        return context


@method_decorator(signin_required,name="dispatch")
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("login")


@method_decorator(signin_required,name="dispatch")
class ProductDetailView(DetailView):
    template_name = "product-detail.html"
    model = Products
    context_object_name = "product"
    pk_url_kwarg = "id"


@method_decorator(signin_required,name="dispatch")
class AddToCartView(FormView):
    template_name = "addto-cart.html"
    form_class = forms.CartForm

    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        product=Products.objects.get(id=id)
        return render(request,self.template_name,{"form":forms.CartForm(),"product":product})

    def post(self, request, *args, **kwargs):
        id = kwargs.get("id")
        product = Products.objects.get(id=id)
        qty=request.POST.get("qty")
        user=request.user
        Carts.objects.create(product=product,user=user,qty=qty)
        messages.success(self.request, "item has been added into your carts")
        return redirect("home")


@method_decorator(signin_required,name="dispatch")
class MyCartView(ListView):
    model=Carts
    template_name = "cart-list.html"
    context_object_name = "carts"

    def get_queryset(self):
        return Carts.objects.filter(user=self.request.user).exclude(status="cancelled").order_by("-created_date")



def remove_cart_item(request,*args,**kwargs):
    cart_id=kwargs.get("cid")
    print(cart_id)
    cart=Carts.objects.get(id=cart_id)
    cart.status="cancelled"
    cart.save()
    messages.success(request,"item Removed from your cart")

    return redirect("mycart")

#


class PlaceOrderView(FormView):
    template_name = "place-order.html"
    form_class = forms.OrderForm

    def post(self, request, *args, **kwargs):
        cart_id=kwargs.get("cid")
        product_id=kwargs.get("pid")
        cart=Carts.objects.get(id=cart_id)
        product=Products.objects.get(id=product_id)
        user=request.user
        delivery_address=request.POST.get("delivery_address")
        Order.objects.create(product=product,user=user,delivery_address=delivery_address)
        cart.status="order-placed"
        cart.save()
        return redirect('home')



