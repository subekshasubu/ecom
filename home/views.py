from django.contrib import messages, auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic.base import View

from home.models import Category, Slider, Ad, Items, Brand, Cart, Contact


class BaseView(View):
    views = {}





class HomeView(BaseView):
    def get(self,request):
        self.views['categories'] = Category.objects.all()
        self.views['sliders'] = Slider.objects.all()
        self.views['ads1'] = Ad.objects.filter(rank=1)
        self.views['ads2'] = Ad.objects.filter(rank=2)
        self.views['ads3'] = Ad.objects.filter(rank=3)
        self.views['ads4'] = Ad.objects.filter(rank=4)
        self.views['ads5'] = Ad.objects.filter(rank=5)
        self.views['ads6'] = Ad.objects.filter(rank=6)
        self.views['ads7'] = Ad.objects.filter(rank=7)
        self.views['ads8'] = Ad.objects.filter(rank=8)

        self.views['items']= Items.objects.all()
        self.views['new_items'] = Items.objects.filter(label='New')
        self.views['hot_items'] = Items.objects.filter(label='Hot')
        self.views['sale_items'] = Items.objects.filter(label='sale')
        self.views['brands']  = Brand.objects.all()

        return render(request,'index.html',self.views)

class ProductDetailView(BaseView):
    def get(self,request,slug):
        category = Items.objects.get(slug=slug).category
        self.views['detail_item'] = Items.objects.filter(slug=slug)
        self.views['related_item'] = Items.objects.filter(category=category)
        self.views['category']= Category.objects.all()
        self.views['brands']= Brand.objects.all()
        return render(request,'product-detail.html',self.views)

class SearchView(BaseView):
        def get(self,request):
            query = request.GET.get('query',None)
            if not query:
                return redirect("/")
            self.views['search_query'] = Items.objects.filter(name__icontains = query,description__icontains=query)
            self.views['searched_for'] = query

            return render(request, 'search.html', self.views)

class CategoryView(BaseView):
    def get(self,request,slug):
        cat = Category.objects.get(slug=slug).id
        self.views['category_items']= Items.objects.filter(category=cat)
        self.views['category'] = Category.objects.all()
        self.views['brands']= Brand.objects.all()
        return render(request,'category.html',self.views)

class BrandView(BaseView):
    def get(self,request,name):
        bran=Brand.objects.get(name=name).id
        self.views['brand_items']=Items.objects.filter(brand=bran)
        self.views['category'] = Category.objects.all()
        self.views['brands'] = Brand.objects.all()
        return render(request,'brand.html',self.views)


def register(request):
    if request.method == "POST":
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.error(request,'The username already exists.')
                return redirect('home:signup')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'The email is already used.')
                return redirect('home:signup')
            else:
                data = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=password

                )
                data.save()
                messages.error(request,'You are signed up.')
                return redirect('home:signup')
        else:
            messages.error(request, 'The password is not matched.')
            return redirect('home:signup')
    return render(request,'signup.html')

def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Username and Password do not match.')
            return redirect('home: signin')

    return render(request, 'signin.html')

class CartDetails(BaseView):
    def get(self, request):
        self.views['carts'] = Cart.objects.filter(user=request.user.username)


        return render(request,'cart.html',self.views)

def cart(request,slug):
    if Cart.objects.filter(slug=slug, user=request.user.username).exists():
        quantity = Cart.objects.get(slug=slug,user=request.user.username).quantity
        quantity = quantity+1
        price = Items.objects.get(slug=slug).price
        discounted_price = Items.objects.get(slug=slug).discounted_price
        if discounted_price > 0:
            total = discounted_price*quantity
        else:
            total = price*quantity
        Cart.objects.filter(slug=slug, user=request.user.username).update(quantity=quantity, total=total)
    else:
        price = Items.objects.get(slug=slug).price
        discounted_price = Items.objects.get(slug=slug).discounted_price
        if discounted_price > 0:
            total = discounted_price
        else:
            total = price

        data = Cart.objects.create(
            user=request.user.username,
            slug=slug,
            item=Items.objects.filter(slug=slug)[0],
            total=total


        )
        data.save()
    return redirect('home:mycart')

def deletecart(request,slug):
    if Cart.objects.filter(slug=slug, user=request.user.username).exists():
        Cart.objects.filter(slug=slug, user=request.user.username).delete()
        messages.success(request, 'The item is deleted.')

    return redirect('home:mycart')

def delete_single_cart(request,slug):
    if Cart.objects.filter(slug=slug, user=request.user.username).exists():
        quantity = Cart.objects.get(slug=slug,user=request.user.username).quantity
        quantity = quantity-1
        price = Items.objects.get(slug=slug).price
        discounted_price = Items.objects.get(slug=slug).discounted_price
        if discounted_price > 0:
            total = discounted_price*quantity
        else:
            total = price*quantity
        Cart.objects.filter(slug=slug, user=request.user.username).update(quantity=quantity, total=total)

    return redirect('home:mycart')

def ContactDetails(request):
    if request.method == "POST":
            name = request.POST['name']
            email = request.POST['email']
            subject = request.POST['subject']
            messagey= request.POST['messagee']

            data=Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=messagey
            )
            data.save()



    return render(request, 'contact.html')








