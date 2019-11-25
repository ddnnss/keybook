from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate
from django.contrib import messages
from .models import *
from filter.models import *
from customuser.forms import *

def index(request):
    allNews = News.objects.filter(isShowAtIndex=True)
    allHouses = House.objects.all()
    return render(request, 'pages/index.html', locals())
def product(request,slug):
    house = House.objects.get(name_slug=slug)

    filters = CategoryFilter.objects.filter(category=house.category)
    images = HousePhotos.objects.filter(house=house)

    filterValues = FilterValue.objects.filter(house=house)


    return render(request, 'pages/product.html', locals())


def login(request):
    form = SignUpForm()
    return render(request, 'pages/login.html', locals())

def login_req(request):
    user = authenticate(username=request.POST.get('email'), password=request.POST.get('password'))
    if user is not None:
        return render(request, 'pages/lk.html', locals())
    else:
        messages.success(request, 'Проверьте введенные данные')
        return HttpResponseRedirect('/login')

def reg_req(request):
    print(request.POST)
    email = request.POST.get('email')

    phone = request.POST.get('phone')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')
    isOfferRent = request.POST.get('isOfferRent')
    # data = {'email': email, 'phone': phone, 'password2': password2, 'password1': password1, 'isOfferRent':isOfferRent}
    data = request.POST.copy()

    form = SignUpForm(data)

    if not form.errors:
        new_user = form.save(data)
        return HttpResponseRedirect("/")
    else:
        print(form.errors)
        data, errors = {}, {}
        messages.success(request, form.errors)
    return HttpResponseRedirect("/login?tab=reg")

def update_req(request):
    print(request.POST)
    form = UpdateForm(request.POST, request.FILES, instance=request.user)
    print(form.errors)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/lk')
    else:
        form = UpdateForm()
    return HttpResponseRedirect("/lk")

def lk(request):
    updateForm = UpdateForm()
    curUser = request.user
    return render(request, 'pages/lk.html', locals())