from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('personal/', views.Personal.as_view(), name='personal'),
    path('news_list/', views.news_list, name='news_list'),
    path('about_me/', views.about_web, name='about_web'),
    path('contact_me/', views.contact, name='contact'),
]
