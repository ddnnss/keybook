from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.db.models import Q
from django.contrib import messages
from .models import *
from filter.models import *
from customuser.forms import *
from django.contrib.auth import authenticate,logout,login
from .forms import *
from filter.models import *


def index(request):
    allNews = News.objects.filter(isShowAtIndex=True)
    allHouses = House.objects.all()
    allfavs = []
    if request.user.is_authenticated:
        favs = Favorite.objects.filter(client=request.user)
        for x in favs:
            allfavs.append(x.house.id)
    return render(request, 'pages/index.html', locals())
def product(request,slug):
    house = House.objects.get(name_slug=slug)

    filters = CategoryFilter.objects.filter(category=house.category)
    images = HousePhotos.objects.filter(house=house)

    filterValues = FilterValue.objects.filter(house=house)


    return render(request, 'pages/product.html', locals())


def login_page(request):
    form = SignUpForm()
    return render(request, 'pages/login.html', locals())

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

def search(request):
    allTowns = Town.objects.all()
    allTypes = HouseCategory.objects.all()
    products = House.objects.all()
    anchor = ''
    searchResult = None
    filtered = False
    if request.GET.get('town') and request.GET.get('type'):
        searchResult = products.filter(Q(town_id=request.GET.get('town')) & Q(category_id=request.GET.get('type')))
        anchor = 'results'
        filtered = True
    elif request.GET.get('town'):
        searchResult= products.filter(town_id=request.GET.get('town'))
        anchor = 'results'
        filtered = True
    elif request.GET.get('type'):
        searchResult = products.filter(category_id=request.GET.get('type'))
        anchor = 'results'
        filtered = True

    if filtered:
        result = searchResult
    else:
        result = products

    if request.GET.get('price_from') and request.GET.get('price_to'):
        allProduct  = result.filter(Q(price__gte=request.GET.get('price_from')) & Q(price__lte=request.GET.get('price_to')))
    elif request.GET.get('price_from'):
        allProduct = result.filter(price__gte=request.GET.get('price_from'))
    elif request.GET.get('price_to'):
        allProduct = result.filter(price__lte=request.GET.get('price_to'))
    else:
        allProduct = result

    return render(request, 'pages/search.html', locals())

def login_req(request):
    user = authenticate(username=request.POST.get('email'), password=request.POST.get('password'))
    if user is not None:
        login(request, user)
        return HttpResponseRedirect("/lk")
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
        login(request, new_user)
        return HttpResponseRedirect("/lk")
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
    if request.user.is_authenticated:
        allTypes = HouseCategory.objects.all()
        allTowns = Town.objects.all()
        favs = Favorite.objects.filter(client=request.user)

        form = HouseForm()
        updateForm = UpdateForm()
        curUser = request.user
        myHouses = House.objects.filter(client=curUser)
        return render(request, 'pages/lk.html', locals())
    else:
        return render(request, 'pages/login.html', locals())


def addhouse(request):
    print(request.POST)

    form = HouseForm(request.POST, request.FILES)
    if not form.errors:
        newhouse = form.save()
        for f in request.FILES.getlist('images'):
            print(f)
            HousePhotos.objects.create(house=newhouse,image=f)

    return HttpResponseRedirect("/lk")

def edit(request,id):
    allTypes = HouseCategory.objects.all()
    allTowns = Town.objects.all()
    house = House.objects.get(id=id)
    form = HouseUpdateForm()
    return render(request, 'pages/edit.html', locals())

def edithouse(request):
    print(request.POST)
    house = House.objects.get(id=request.POST.get('id'))
    form = HouseUpdateForm(request.POST, request.FILES, instance=house)
    if not form.errors:
        newhouse = form.save()


    return HttpResponseRedirect("/lk")

def addfilter(request,id):
    house = House.objects.get(id=id)
    filters = CategoryFilter.objects.filter(category=house.category)
    return render(request, 'pages/addfilter.html', locals())

def addfilter_req(request):
    print(request.POST)
    for x in request.POST:

        if not x == 'csrfmiddlewaretoken' and not x == 'house':
            print('filter_id=',str(x).split('-')[1])
            print('value=',request.POST[x])
            print('house_id=',request.POST.get('house'))

            FilterValue.objects.create(value=request.POST[x],house_id=request.POST.get('house'), filter_id=str(x).split('-')[1])
    return HttpResponseRedirect("/product/{}".format(House.objects.get(id=request.POST.get('house')).name_slug))

def delfav(request,id):
    Favorite.objects.filter(id=id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def addfav(request,id):
    Favorite.objects.create(client=request.user, house_id=id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))