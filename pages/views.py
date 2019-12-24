from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.db.models import Q
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .models import *
from filter.models import *
from customuser.forms import *
from customuser.models import *
from django.contrib.auth import authenticate,logout,login
from .forms import *
from filter.models import *
import json

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
    allfavs = []
    if request.user.is_authenticated:
        favs = Favorite.objects.filter(client=request.user)
        for x in favs:
            allfavs.append(x.house.id)
    house = House.objects.get(name_slug=slug)

    rentTime = 'no'
    try:
        rentime = GlobalRent.objects.get(house=house)
        rentTime = rentime.globalRentTime
        print(rentTime.rentTime)
    except:
        pass

    filters = CategoryFilter.objects.filter(category=house.category)
    images = HousePhotos.objects.filter(house=house)

    filterValues = FilterValue.objects.filter(house=house)


    return render(request, 'pages/product.html', locals())


def login_page(request):
    form = SignUpForm()
    return render(request, 'pages/login.html', locals())

def about(request):

    return render(request, 'pages/about.html', locals())

def post(request,slug):
    curPost = News.objects.get(name_slug=slug)

    return render(request, 'pages/post.html', locals())

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

def search(request):
    allfavs = []
    if request.user.is_authenticated:
        favs = Favorite.objects.filter(client=request.user)
        for x in favs:
            allfavs.append(x.house.id)
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
        allChats = Chat.objects.filter(users__in=[request.user.id])
        print(allChats)
        allChatPeoples = []
        for x in allChats:
            for y in x.users.all():
                print(y.id)
                if y.id !=request.user.id:
                    allChatPeoples.append(User.objects.get(id=y.id))
        print(allChatPeoples)
        # allMessages = Message.objects.filter(messageTo=request.user)
        # allMans = []
        # for x in allMessages:
        #     if x.messageFrom_id not in allMans:
        #         allMans.append(x.messageFrom_id)
        # print(allMans)
        # chatPeoples=[]
        # for x in allMans:
        #     y = User.objects.get(id=x)
        #     chatPeoples.append(y)
        # first = allMessages.first()
        # print(first)
        # try:
        #     firstMan = first.messageFrom.id
        # except:
        #     firstMan = None
        #
        # print('first=',firstMan)
        # firstMsg = allMessages.filter(messageFrom_id=firstMan)
        # try:
        #     lastmsg = firstMsg.last().id
        # except:
        #     lastmsg = None

        rentByme = Rent.objects.filter(clientWhoRent=request.user)
        whoHavehouse = Rent.objects.filter(clientWhoHaveHouse=request.user)

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


def rent(request):
    print(request.GET)
    curRent =None
    globalRent = None
    try:
        globalRent = GlobalRent.objects.get(house_id=request.GET.get('h'))
    except:
        GlobalRent.objects.create(house_id=request.GET.get('h'),globalRentTime=request.GET.get('globaltime'))
        print('rent created')
    if globalRent:
        globalRent.globalRentTime = request.GET.get('globaltime')
        globalRent.save()
        print('rent updated')

    try:
        curRent = Rent.objects.get(clientWhoRent=request.user,clientWhoHaveHouse_id=request.GET.get('whh'), house_id=request.GET.get('h'))
    except:
        Rent.objects.create(clientWhoRent=request.user,clientWhoHaveHouse_id=request.GET.get('whh'), house_id=request.GET.get('h'),rentTime=request.GET.get('time'))
        print('created')
    if curRent:
        curRent.rentTime = request.GET.get('time')
        curRent.save()
        print('updated')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@csrf_exempt
def new_msg(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    chat = Chat.objects.filter(users__in=[body['msgFrom'], body['msgTo']])
    for x in chat.all():
        if x.id != request.user.id:
            chat = False

    if chat:
        print('chat found')
        Message.objects.create(chat_id=chat[0].id, user_id=body['msgFrom'], message=body['msg'])
    else:
        print('chat not found')
        newChat = Chat.objects.create()
        newChat.users.add(body['msgFrom'], body['msgTo'])
        Message.objects.create(chat=newChat, user_id=body['msgFrom'], message=body['msg'])
    # Message.objects.create(messageTo_id=body['msgTo'],messageFrom_id=body['msgFrom'],message=body['msg'])
    return JsonResponse({'foo': 'bar'})

@csrf_exempt
def answer_msg(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    try:
        msg = Message.objects.get(id=body['answerFor'])
        msg.answer = message=body['msg']
        msg.save()
    except:
        Message.objects.create(messageTo_id=body['msgTo'], messageFrom_id=body['msgFrom'], message=body['msg'])

    return JsonResponse({'foo': 'bar'})


@csrf_exempt
def get_chat_msg(request):
    respose=[]
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    print(body['chat'])
    chat=Chat.objects.get(id=body['chat'])
    print(chat.message_set.all())
    for x in chat.message_set.all():
        chatItem = {}
        chatItemInner = []
        if x.user == request.user:
            chatItem['own']=[x.message,x.createdAt.strftime("%b %d %Y %H:%M:%S")]
        else:
            chatItem['from'] = [x.message,x.createdAt.strftime("%b %d %Y %H:%M:%S")]
        respose.append(chatItem)
    return JsonResponse(respose,safe=False)

@csrf_exempt
def add_msg(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    Message.objects.create(chat_id=body['chatId'], user_id=body['msgFrom'], message=body['msg'])
    return JsonResponse('ok',safe=False)