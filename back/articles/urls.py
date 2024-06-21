
from django.contrib import admin
from django.urls import path
from . import views

# app_name = 'articles'

urlpatterns = [
    path('', views.article_list),
    path('byliked/', views.article_list_by_likes),
    path('<int:article_pk>/', views.article_detail), 
    path('myarticles/', views.my_article_list),
    # comment
    path('<int:article_pk>/comments/', views.comment_list),
    path('comments/<int:comment_pk>/', views.comment_detail),    #댓글 수정 삭제 얻기?
    # like
    path('<int:article_pk>/likes/',views.likes),
    path('liked_articles/', views.liked_articles),  # 유저가 좋아요 한 게시물 출력하기용

]
