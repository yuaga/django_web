from django.urls import path
from . import views


app_name = 'news'

urlpatterns = [
    path('news_detail/<int:news_id>', views.news_detail, name='news_detail'),
    path('news_comment/', views.news_comment, name='news_comment'),
    path('news_list/', views.news_list, name='news_list'),
    path('news_category/<int:category_id>', views.news_category, name='news_category'),
    path('archives/<int:year>/<int:month>', views.archives, name='archives'),
    path('up/', views.up, name='up'),
    path('down/', views.down, name='down'),

]