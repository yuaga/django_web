from django.conf import settings
from django.db.models import Count
from django.http import Http404
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.template.defaultfilters import escape
from apps.news.forms import CommentForm
from apps.news.serializers import CommentSerializer, NewsListSerializer
from utils import restful
from .models import News, Comment, Category
from .models import UpAndDown


class QuerySet:
    categories = Category.objects.annotate(news_count=Count('news'))
    hot_newses = News.objects.order_by('-views')[0:5]
    archives = News.objects.dates('pub_time', 'month', order='DESC').annotate(news_num=Count('id'))


def news_detail(request, news_id):
    try:
        news = News.objects.select_related('author', 'category').prefetch_related('comments__comment_author', ).annotate(comments_num=Count('comments')).get(pk=news_id)
    except Exception:
        raise Http404
    news.increase_views()
    return render(request, 'news/news_detail.html', context={'news': news})


@require_POST
def news_comment(request):
    form = CommentForm(request.POST)
    if form.is_valid():
        try:
            content = escape(form.cleaned_data.get('comment_content'))  # 对提取出来的数据进行转义，即使django模板默认转义。
            news_id = form.cleaned_data.get('news_id')
            news = News.objects.get(pk=news_id)  # 这里必须将新闻查询到，不能直接将id保存到数据库中，会报错。当保存时数据中要保存实列，而不是一个id
            comment = Comment.objects.create(comment_content=content, comment_news=news,
                                             comment_author=request.user)  # 评论的作者直接从request中获取
            serializer = CommentSerializer(comment)
            return restful.result(data=serializer.data)
        except News.DoesNotExist:
            raise Http404
    else:
        return restful.params_error(message=form.get_errors())


def news_list(request):
    category_id = request.GET.get('category_id')
    page = int(request.GET.get('p', 1))
    start = int((page - 1) * settings.ONE_PAGE_NEWS_COUNT)
    end = int(start + settings.ONE_PAGE_NEWS_COUNT)
    newses = News.objects.select_related('category', 'author').annotate(comments_num=Count('comments')).filter(category__id=category_id)[start:end]
    serializer = NewsListSerializer(newses, many=True)
    return restful.result(data=serializer.data)


def news_category(request, category_id):
    try:
        Category.objects.get(pk=category_id)
    except Exception:
        raise Http404
    count = settings.ONE_PAGE_NEWS_COUNT
    newses = News.objects.select_related('category', 'author').annotate(news_num=Count('pub_time__month'), comments_num=Count('comments')).filter(category__id=category_id)[0:count]
    categories = Category.objects.annotate(news_count=Count('news'))
    hot_newses = News.objects.order_by('-views')[0:5]
    archives = News.objects.dates('pub_time', 'month', order='DESC').annotate(news_num=Count('id'))
    return render(request, 'news/news_category.html', context={
        'newses': newses,
        'categories': categories,
        'hot_newses': hot_newses,
        'archives': archives
    })


def archives(request, year, month):
    newses = News.objects.filter(pub_time__year=year,
                                 pub_time__month=month
                                 ).order_by('-pub_time').annotate(news_count=Count('id'))
    categories = Category.objects.annotate(news_count=Count('news'))
    hot_newses = News.objects.order_by('-views')[0:5]
    archives = News.objects.dates('pub_time', 'month', order='DESC').annotate(news_num=Count('id'))
    return render(request, 'blog/index.html', context={
        'newses': newses,
        'categories': categories,
        'hot_newses': hot_newses,
        'archives': archives
    })


def up(request):
    user = request.user
    up = request.POST.get('up')
    news_id = request.POST.get('news_id')
    news = News.objects.filter(pk=news_id).first()
    updown_query = UpAndDown.objects.filter(up_news=news, up_user=user)
    updown_obj = updown_query.first()
    if updown_query.exists():
        if updown_obj.up is False:
            updown_obj.up = up
            updown_obj.save()
            news.up_num += 1
            news.save()
            return restful.result(message='点赞成功')
        else:
            return restful.params_error(message='你已经点过赞啦！')
    else:
        UpAndDown.objects.create(up_user=user, up_news=news, up=up)
        news.up_num += 1
        news.save()
        return restful.result(message='点赞成功')


def down(request):
    user = request.user
    down = request.POST.get('down')
    news_id = request.POST.get('news_id')
    news = News.objects.filter(pk=news_id).first()
    updown_query = UpAndDown.objects.filter(up_news=news, up_user=user)
    updown_obj = updown_query.first()
    if updown_query.exists():
        if updown_obj.up is True:
            updown_obj.up = down
            updown_obj.save()
            news.up_num -= 1
            news.save()
            return restful.result(message='取消成功')
        else:
            return restful.params_error(message='你没有赞这篇文章')
    else:
        return restful.params_error(message='你没有赞这篇文章')
