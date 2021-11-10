from django.views.generic import ListView, DetailView  
from .models import Post
 
 
class ArticlesList(ListView):
    model = Post  
    template_name = 'articles.html' 
    context_object_name = 'articles'
    queryset = Post.objects.order_by('-date') 

class ArticlesDetail(DetailView):
    model = Post  
    template_name = 'article.html' 
    context_object_name = 'article'
