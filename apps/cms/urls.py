from django.urls import path
from . import views

app_name = 'cms'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('category_manage/', views.category_manage, name='category_manage'),
    path('add_category/', views.add_category, name='add_category'),
    path('edit_category/', views.edit_category, name='edit_category'),
    path('del_category/', views.del_category, name='del_category'),

    path('write_news/', views.WriteNews.as_view(), name='write_news'),
    path('news_manage/', views.CmsNewsManage.as_view(), name='news_manage'),
    path('edit_news/', views.EditNews.as_view(), name='edit_news'),
    path('del_news/', views.del_news, name='del_news'),

    path('staff_manage/', views.StaffManage.as_view(), name='staff_manage'),
    path('del_permission/', views.del_permission, name='del_permission'),
    path('del_staff/', views.del_staff, name='del_staff'),

    path('comment_manage', views.CommentManage.as_view(), name='comment_manage'),
    path('del_comment/', views.del_comment, name='del_comment')
]
