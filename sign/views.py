from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from sign.models import Event,Guest
from django.shortcuts import render,get_object_or_404

# Create your views here.
def index(request):
    return render(request,'index.html')

# 登录动作
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        # 使用authenticate()函数认证给出的用户名和密码。它接受两个参数，用户名username和密码password
        # 并在用户名密码正确的情况下返回一个user对象。如果用户名密码不正确，则authenticate()返回None
        user = auth.authenticate(username=username,password=password)
        # if username == 'admin' and password == 'admin123':
        if user is not None:
            auth.login(request,user)
            #return HttpResponse("Login Success!")
            #return HttpResponseRedirect('/event_manage/')
            response = HttpResponseRedirect('/event_manage/')
            #response.set_cookie('user', username, 3600) # 添加浏览器Cookie
            request.session['user'] = username           # 将session信息添加到浏览器
            return response
        else:
            return render(request, 'index.html', {'error':'username or password error!'})

# 发布会管理
@login_required
def event_manage(request):
    #增加发布会列表
    event_list = Event.objects.all()
    #username = request.COOKIES.get('user', '') # 读取浏览器Cookie
    username = request.session.get('user', '')  # 读取浏览器session
    # 通过render()方法附加在event_mange.html页面返回给客户端
    return render(request, "event_manage.html", {"user":username,"events":event_list})

#发布会搜索
@login_required
def search_name(request):
    username = request.session.get('user','')
    search_name =request.GET.get("name","")
    event_list = Event.objects.filter(name__contains = search_name)
    return render(request,"event_manage.html",{"user":username,"events":event_list})

#嘉宾管理
@login_required
def guest_manage(request):
    username = request.session.get('user','')
    guest_list = Guest.objects.all()

    paginator = Paginator(guest_list,1)
    page = request.GET.get('page')
    try:
        contacts = paginator.page('page')
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    return render(request,'guest_manage.html',{"user":username,"guests":contacts})

#嘉宾搜索
@login_required
def search_name2(request):
    username = request.session.get('user', '')
    search_name2 = request.GET.get("name", "")
    guest_list = Guest.objects.filter(realname__contains=search_name2)
    return render(request, "guest_manage.html", {"user": username, "guests": guest_list})

#签到页面
@login_required
def sign_index(request,event_id):
    event = get_object_or_404(Event,id = event_id)
    return render(request,'sign_index.html',{'event':event})

#签到动作
@login_required
def sign_index_action(request,event_id):
    event = get_object_or_404(Event,id=event_id)
    phone = request.POST.get('phone','')

    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request,'sign_index.html',{'event':event,'hint':'phone error'})

    result = Guest.objects.filter(phone=phone,event_id=event_id)
    if not result:
        return render(request,'sign_index.html',{'event':event,'hint':'event_id or phone error'})

    result = Guest.objects.filter(phone=phone,event_id=event_id)
    if result.sign:
        return render(request,'sign_index.html',{'event':event,'hint':'user has sign in.'})
    else:
        Guest.objects.filter(phone=phone,event_id=event_id).update(sign = '1')
        return render(request,'sign_index.html',{'event':event,'hint':'sign in success!','guest':result})

#退出登录
@login_required
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/index')
    return response
1111
