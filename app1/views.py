from django.shortcuts import render, HttpResponse, redirect
import os

userdict = {
    "1": {"name": "a", "gender": "male", "age": "31"},
    "2": {"name": "ab", "gender": "male", "age": "32"},
    "3": {"name": "abc", "gender": "female", "age": "33"}
}


# def detail(request):
#     nid = request.GET.get("nid")
#     userinfo = userdict[nid]
#     return render(request, "detail.html", {"user_info": userinfo})

def detail(request, nid):
    # nid = request.GET.get(str(id))
    userinfo = userdict[nid]
    return render(request, "detail.html", {"user_info": userinfo})


# Create your views here.
# FBV(function based views)
def index(request):
    return render(request, "home.html", {"user_dict": userdict})


# def login(request):
#     if request.method == "GET":
#         return render(request, "login.html")
#     elif request.method == "POST":
#         user = request.POST.get("user", None)
#         pwd = request.POST.get("pwd", None)
#         file = request.FILES.get('fa', None)
#         if user == "zs" and pwd == "111":
#             if file:
#                 # 类似文件上传
#                 path = os.path.join("upload", file.name)
#                 f = open(path, mode="wb")
#                 for i in file.chunks():
#                     f.write(i)
#                 f.close()
#             return redirect("/index")
#     else:
#         return render(request, "login.html")

def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        user = request.POST.get("user", None)
        pwd = request.POST.get("pwd", None)
        # file = request.FILES.get('fa', None)
        obj = models.UserInfo.objects.filter(username=user, password=pwd).first()
        if obj:
            return render(request, "user_info.html")
        else:
            return render(request, "home.html")

    else:
        return render(request, "login.html")


def user_info(request):
    # Query_set
    if request.method == "GET":
        info_list = models.UserInfo.objects.all()
        group_list = models.UserGroup.objects.all()
        return render(request, "user_info.html", {"user_list": info_list, "group_list": group_list})
    elif request.method == "POST":
        u = request.POST.get("user")
        p = request.POST.get("pwd")
        # 单选用的是select的name得到值！！！
        user_group_id = request.POST.get("group_id")
        models.UserInfo.objects.create(username=u, password=p, user_group_id=user_group_id)
        return redirect("/user_info")


def user_detail(request, nid):
    obj = models.UserInfo.objects.filter(id=nid).first()
    return render(request, "user_detail.html", {"obj": obj})


def user_del(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user_info')


def user_edit(request, nid):
    if request.method == "GET":
        obj = models.UserInfo.objects.filter(id=nid).first()
        # render返回html,redirect里面为url参数，并且没有request
        return render(request, "user_edit.html", {"obj": obj})
    elif request.method == "POST":
        nid = request.POST.get("id")
        u = request.POST.get("user")
        p = request.POST.get("pwd")
        models.UserInfo.objects.filter(id=nid).update(id=nid, username=u, password=p)
        return redirect("/user_info")


# CBV(class based views)
from django.views import View


class Home(View):
    # 在get，post方法前调用
    def dispatch(self, request, *args, **kwargs):
        print("before")
        result = super(Home, self).dispatch(request, *args, **kwargs)
        print("after")
        return result

    def get(self, request):
        print(request.method)
        return render(request, "home.html")

    def post(self, request):
        print(request.method)
        return render(request, "home.html")


from app1 import models


def orm(request):
    # 创建下面这三种方式
    # models.UserInfo.objects.create(
    #     username="zs1",password="111"
    # )
    # dic = {'username': 'zs2', 'password': '222'}
    # models.UserInfo.objects.create(**dic)

    # obj = models.UserInfo(username='zs3',password='333')
    # obj.save()

    # 查找
    # res=models.UserInfo.objects.all()
    # res=models.UserInfo.objects.filter(username="zs1")
    # for i in res:
    #     print (i.id,i.username,i.password)
    # print (res)

    # 删除
    # models.UserInfo.objects.filter(id=3).delete()

    # 更新
    # models.UserInfo.objects.filter(username="zs3").update(username="zs2", password="2222")

    # 一对多
    models.UserInfo.objects.create(
        username="root1",
        password="123",
        email="root@123.com",
        user_group_id=1
    )
    return HttpResponse("orm")
