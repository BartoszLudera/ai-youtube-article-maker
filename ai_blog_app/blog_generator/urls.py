from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.user_login, name='index'),
    path('logout', views.user_logout, name='logout'),
    path('signup', views.user_signup, name='signup'),
    path('welcome-page', views.welcome_page, name='welcome_page'),
    path('generate-blog', views.generate_blog, name='generate_blog'),
    path('blog-details/<int:pk>/', views.blog_details, name='blog_details'),
    path('all-blogs', views.all_blogs, name='all_blogs')
]
