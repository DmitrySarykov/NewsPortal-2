from django.urls import path
from .views import ArticlesList, ArticlesDetail

urlpatterns = [
    path('', ArticlesList.as_view()),
    path('<int:pk>', ArticlesDetail.as_view(), name="article"),
]