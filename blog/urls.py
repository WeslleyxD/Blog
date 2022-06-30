from django.urls import path
from .import views


app_name = 'blog'

# https://docs.djangoproject.com/en/4.0/topics/http/urls/#pathconverters.
urlpatterns = [
    path('search/', views.post_search, name='post_search'),
    path('publication/', views.post_publication, name='post_publication'), 
    path('<slug:post>/',views.post_detail, name='post_detail'),  
    path('', views.post_list, name='post_list'), 
    path('<slug:post_slug>/share/',views.post_share, name='post_share'),
    path('tag/<str:tag_slug>/',views.post_list, name='post_list_by_tag'),  
]