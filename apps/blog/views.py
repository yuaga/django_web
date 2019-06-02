from django.conf import settings
from django.db.models import Count
from django.shortcuts import render, redirect, reverse
from apps.news.serializers import NewsListSerializer
from utils import restful
from django.views import View
from .models import User
from apps.news.models import News, Category
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm, EditForm


def index(request):
    count = settings.ONE_PAGE_NEWS_COUNT
    newses = News.objects.annotate(news_num=Count('pub_time__month'), comments_num=Count('comments')).all()[0:count]
    categories = Category.objects.annotate(news_count=Count('news')).all()
    hot_newses = News.objects.order_by('-views')[0:5]
    return render(request, 'blog/index.html', context={
        "newses": newses,
        "categories": categories,
        "hot_newses": hot_newses,
    })


def news_list(request):
    page = int(request.GET.get('p', 1))
    start = int((page - 1) * settings.ONE_PAGE_NEWS_COUNT)
    end = int(start + settings.ONE_PAGE_NEWS_COUNT)
    newses = News.objects.select_related('category', 'author').annotate(comments_num=Count('comments')).all()[start:end]
    serializer = NewsListSerializer(newses, many=True)
    return restful.result(data=serializer.data)


def logout_view(request):
    logout(request)
    return redirect(reverse('blog:index'))


class LoginView(View):

    def get(self):
        return redirect(reverse('blog:index'))

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data.get('telephone')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user = authenticate(request, username=telephone, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    if remember:
                        request.session.set_expiry(None)
                    else:
                        request.session.set_expiry(0)
                        return restful.ok()
                else:
                    return restful.params_error(message='此账号被关进了小黑屋')
            else:
                if User.objects.filter(telephone=telephone).exists():
                    return restful.params_error(message='密码错误！')
                else:
                    return restful.params_error(message='还未进行注册，请进行注册！')
        else:
            return restful.params_error(message=form.get_errors())


class RegisterView(View):

    def get(self):
        return redirect(reverse('blog:index'))

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data.get('telephone')
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            exists = User.objects.filter(telephone=telephone).exists()
            if not exists:
                if password1 == password2:
                    user = User.objects.create_user(telephone=telephone, username=username, password=password1)
                    login(request, user)
                    return restful.ok()
                else:
                    message = '两次输入密码不一致，请重新输入！'
                    return restful.params_error(message=message)
            else:
                message = '你的手机号码已被注册了！'
                return restful.params_error(message=message)
        else:
            return restful.params_error(message=form.get_errors())


class Personal(View):

    def get(self, request):
        user = request.user
        personal_newses = News.objects.select_related('category').filter(author=user)

        return render(request, 'blog/personal.html', context={
            "personal_newses": personal_newses
        })

    def post(self, request):
        form = EditForm(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data.get('telephone')
            old_pwd = form.cleaned_data.get('old_pwd')
            new_pwd1 = form.cleaned_data.get('new_pwd1')
            new_pwd2 = form.cleaned_data.get('new_pwd2')
            if telephone == str(request.user):
                if old_pwd != new_pwd1:
                    if new_pwd1 == new_pwd2:
                        user = authenticate(request, username=telephone, password=old_pwd)
                        if user:
                            user = User.objects.filter(telephone=telephone).first()
                            user.set_password(new_pwd2)
                            user.save()
                            login(request, user)
                            return restful.ok()
                        else:
                            return restful.params_error(message='输入的旧密码错误')
                    else:
                        return restful.params_error(message='两次输入的新密码不一致！')
                else:
                    return restful.params_error(message='新旧密码一样！重新输入新密码！')
            else:
                return restful.params_error(message='请不要耍小聪明，输入自己的手机号码！')

        else:
            return restful.params_error(message=form.get_errors())


def about_web(request):
    return render(request, 'blog/about_web.html')


def contact(request):
    return render(request, 'blog/contact_me.html')
