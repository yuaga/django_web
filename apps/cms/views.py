from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
from django.db.models import Count, F
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from apps.blog.decorator import blog_super_decorator
from apps.blog.models import User
from apps.news.models import Category, News, Comment
from django.views.decorators.http import require_POST, require_GET
from utils import restful
from apps.cms.forms import WriteNewsForms, EditNewsForm
from django.http import Http404
from datetime import datetime
from django.utils.timezone import make_aware
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required(login_url='index')
def index(request):
    return render(request, 'cms/base.html')


@require_GET
@permission_required(perm='news.view_category', login_url='/')
def category_manage(request):
    categories = Category.objects.annotate(news_count=Count('news'))
    return render(request, 'cms/category.html', context={'categories': categories})


@require_POST
@permission_required(perm='news.add_category', login_url='/')
def add_category(request):
    try:
        name = request.POST.get('name')
        if not Category.objects.filter(name=name).exists():
            Category.objects.create(name=name)
            return restful.ok()
        else:
            return restful.params_error(message='分类已存在')
    except Exception:
        pass


@require_POST
@permission_required(perm='news.change_category', login_url='/')
def edit_category(request):
    try:
        pk = request.POST.get('pk')
        name = request.POST.get('name')
        old_category = Category.objects.filter(pk=pk)
        if not Category.objects.filter(name=name).exists():
            old_category.update(name=name)
            return restful.ok()
        else:
            return restful.params_error(message='分类已存在')
    except Exception:
        pass


@require_POST
@permission_required(perm='news.delete_category', login_url='/')
def del_category(request):
    try:
        pk = request.POST.get('pk')
        category = Category.objects.filter(pk=pk)
        if category.exists():
            category.delete()
            return restful.ok()
        else:
            return restful.params_error(message='分类不存在！')
    except Exception:
        pass


@method_decorator(permission_required(perm='news.add_news', login_url='/'), name='dispatch')
class WriteNews(View):

    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'cms/write_news.html', context={'categories': categories})

    def post(self, request):
        form = WriteNewsForms(request.POST)
        if form.is_valid():
            user = request.user
            title = form.cleaned_data.get('title')
            category_id = form.cleaned_data.get('category')
            category = Category.objects.filter(pk=category_id).first()
            intro = form.cleaned_data.get('intro')
            content = form.cleaned_data.get('content')
            News.objects.create(title=title, category=category, intro=intro, content=content, author=user)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())


@method_decorator(permission_required(perm='news.view_news', login_url='/'), name='dispatch')
class CmsNewsManage(View):

    def get(self, request):
        page = int(request.GET.get('p', 1))  # 获取当前的页码, 如果没有拿到，默认第一页，保险起见，转化为整数。
        start = request.GET.get('start')
        end = request.GET.get('end')
        title = request.GET.get('title')
        category_id = int(request.GET.get('category') or 0)  # 获取分类的id, 如果没有就默认为1

        # 使用select_related提前将相关联的数据提取出来，避免模板中在一次查询
        newses = News.objects.select_related('category', 'author')

        if start or end:
            if start:
                # 将字符串时间改为格式化的时间
                start = datetime.strptime(start, '%Y/%m/%d')
            else:
                # 如果没有设置开始查询时间，则默认使用2019/01/01
                start = datetime(year=2019, month=1, day=1)
            if end:
                end = datetime.strptime(end, '%Y/%m/%d')
            else:
                end = datetime.today()

            newses = newses.filter(pub_time__range=(make_aware(start), make_aware(end)))
            # newses = newses.filter(pub_time__range=(start, end))

        if title:
            newses = newses.filter(title__icontains=title)

        if category_id:
            newses = newses.filter(category=category_id)

        paginator = Paginator(newses, 5)  # 要实现分页的模型的对象是newses， 每页5条数据。
        page_obj = paginator.page(page)  # 获取当前页的对象

        context = {
            # object_list 方法是将当前页的所有对象放入列表中，方便前端遍历
            'page_objs': page_obj.object_list,  # 这个地方不能再传newses了，因为要显示分页后的数据
            'categories': Category.objects.all(),
            'title': title,
            'category_id': category_id,
            'paginator': paginator,
            'current_page': page_obj.number,
            'num_pages': paginator.num_pages,
            'page_obj': page_obj,  # 后面4项一定要传，如果没有传，在模板中调用这三个方法是不行的。
        }
        return render(request, 'cms/news_manage.html', context=context)


@method_decorator(permission_required(perm='news.change_news', login_url='/'), name='dispatch')
class EditNews(View):

    def get(self, request):
        try:
            news_id = request.GET.get('news_id')
            news = News.objects.get(pk=news_id)
            return render(request, 'cms/write_news.html', context={'news': news, 'categories': Category.objects.all()})
        except Exception:
            raise Http404

    def post(self, request):
        form = EditNewsForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data.get('id')
            title = form.cleaned_data.get('title')
            category = form.cleaned_data.get('category')
            intro = form.cleaned_data.get('intro')
            content = form.cleaned_data.get('content')
            News.objects.filter(pk=id).update(title=title, category=category, intro=intro, content=content)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())


@require_POST
@permission_required(perm='news.delete_news', login_url='/')
def del_news(request):
    try:
        pk = request.POST.get('pk')
        News.objects.filter(pk=pk).delete()
        return restful.ok()
    except Exception:
        return restful.params_error(message='要删除的新闻不存在！')


@method_decorator(blog_super_decorator, name='dispatch')
class StaffManage(View):

    def get(self, request):
        staffs = User.objects.filter(is_staff=True).prefetch_related('groups')
        groups = Group.objects.all()
        return render(request, 'cms/staffs.html', context={
            'staffs': staffs,
            'groups': groups
        })

    def post(self, request):
        telephone = request.POST.get('telephone')
        group_id = request.POST.get('group')
        user = User.objects.filter(telephone=telephone).first()
        if user:
            user.is_staff = True
            group = Group.objects.filter(pk=group_id).first()
            user.groups.add(group)
            user.save()
            return restful.ok()
        else:
            return restful.params_error(message='这个员工好像不存在呀！')


@require_POST
@blog_super_decorator
def del_permission(request):
    try:
        telephone = request.POST.get('telephone')
    except Exception:
        return restful.params_error(message='这个员工好像不存在呀')
    user = User.objects.filter(telephone=telephone).first()
    user.groups.clear()
    user.save()
    return restful.ok()


@require_POST
@blog_super_decorator
def del_staff(request):
    try:
        telephone = request.POST.get('telephone')
    except Exception:
        return restful.params_error(message='这个员工好像不存在呀')
    User.objects.filter(telephone=telephone).first().delete()

    return restful.ok()


@method_decorator(blog_super_decorator, name='dispatch')
class CommentManage(View):

    def get(self, request):
        page = int(request.GET.get('p', 1))  # 获取当前的页码, 如果没有拿到，默认第一页，保险起见，转化为整数。
        commnets = Comment.objects.select_related('comment_author', 'comment_news').all()
        paginator = Paginator(commnets, 10)  # 要实现分页的模型的对象是newses， 每页10条数据。
        page_obj = paginator.page(page)  # 获取当前页的对象

        context = {
            # object_list 方法是将当前页的所有对象放入列表中，方便前端遍历
            'page_objs': page_obj.object_list,  # 这个地方不能再传commnets了，因为要显示分页后的数据
            'paginator': paginator,
            'current_page': page_obj.number,
            'num_pages': paginator.num_pages,
            'page_obj': page_obj,  # 后面4项一定要传，如果没有传，在模板中调用这三个方法是不行的。
        }
        return render(request, 'cms/comment_manage.html', context=context)


@require_POST
@blog_super_decorator
def del_comment(request):
    try:
        pk = request.POST.get('pk')
        Comment.objects.filter(pk=pk).first().delete()
        return restful.ok()
    except Exception:
        return restful.params_error(message='这个评论好像不存在')