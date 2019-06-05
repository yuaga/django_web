# from django import template
# from apps.news.models import News, Category
# from django.db.models import Count
#
# register = template.Library()
#
# @register.simple_tag
# def archives():
#     archives = News.objects.dates('pub_time', 'month', order='DESC').annotate(news_num = Count('id'))
#     return archives