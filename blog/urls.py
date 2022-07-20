from django.urls import path

from . import views

app_name = "blog"
urlpatterns = [
    path('', views.ArticleListView.as_view(), name='home'),
    path('page/<int:page>', views.ArticleListView.as_view(), name='home'),
    path('article_detail/<slug:slug>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('category/<slug:slug>/', views.CategoryListView.as_view(), name='category'),
    path('category/<slug:slug>/page/<int:page>', views.CategoryListView.as_view(), name='category'),
]
