from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Article, Category

# def home_view(request, page=1):
#     article_list = Article.objects.published()
#     # page = request.GET.get('page', 1)
#     paginator = Paginator(article_list, 3)
#     try:
#         articles = paginator.page(page)
#     except PageNotAnInteger:
#         articles = paginator.page(1)
#     except EmptyPage:
#         articles = paginator.page(paginator.num_pages)
#
#     context = {
#         'articles': articles,
#         'page_numbers': list(range(1, paginator.num_pages + 1)),
#         'categories': Category.objects.filter(status=True)
#     }
#     return render(request, 'blog/home.html', context)

class ArticleListView(generic.ListView):
    queryset = Article.objects.published()
    template_name = 'blog/article_list.html'
    context_object_name = 'articles'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        article_list = Article.objects.published()
        paginator = Paginator(article_list, 3)

        context = super().get_context_data(**kwargs)
        context['page_numbers'] = list(range(1, paginator.num_pages + 1))
        return context

class ArticleDetailView(generic.DetailView):
    template_name = 'blog/article_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Article.objects.published(), slug=self.kwargs.get('slug'))


# def article_detail_view(request, slug):
#     article = get_object_or_404(Article.objects.published(), slug=slug)
#     context = {
#         'article': article,
#     }
#     return render(request, 'blog/article_detail.html', context)

class CategoryListView(generic.ListView):
    template_name = 'blog/category.html'
    context_object_name = 'articles'
    paginate_by = 3

    def get_queryset(self):
        global category
        category = get_object_or_404(Category.objects.published(), slug=self.kwargs.get('slug'), status=True)
        return category.article.published()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context

# def category_view(request, slug, page=1):
#     category = get_object_or_404(Category, slug=slug, status=True)
#     category_list = category.article.published()
#     paginator = Paginator(category_list, 2)
#     try:
#         articles = paginator.page(page)
#     except EmptyPage:
#         articles = paginator.page(paginator.num_pages)
#     except PageNotAnInteger:
#         articles = paginator.page(page)
#
#     context = {
#         'articles': articles,
#         'category': category,
#     }
#     return render(request, 'blog/category.html', context)


