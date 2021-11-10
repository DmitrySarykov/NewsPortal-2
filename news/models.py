from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Category (models.Model):
    name = models.CharField(max_length = 255, unique = True)

class Post (models.Model):
    news = "Н"
    article = "С"
    TYPE= [
        (news, 'Новость'),
        (article, 'Статья'),
    ]
    author = models.ForeignKey('Author', on_delete = models.CASCADE)
    type = models.CharField(max_length = 1, choices = TYPE, default = news)
    date = models.DateTimeField(auto_now_add = True)
    category = models.ManyToManyField(Category, through = 'PostCategory')
    title = models.CharField(max_length = 255)
    text = models.TextField(blank = True)
    rating = models.IntegerField(default = 0)

    def like(self):
        self.rating += 1
        self.save()
        return self.rating

    def dislike(self):
        self.rating -= 1
        self.save()
        return self.rating

    def preview(self):
        return self.text[0:124] + "..."

class PostCategory (models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)

class Comment (models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    comment = models.TextField(blank = True)
    date = models.DateTimeField(auto_now_add = True)
    rating = models.IntegerField(default = 0)

    def like(self):
        self.rating += 1
        self.save()
        return self.rating

    def dislike(self):
        self.rating -= 1
        self.save()
        return self.rating

class Author (models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    rating = models.IntegerField(default = 0)

    def update_rating(self):
        rating = 0 
        # суммарный рейтинг каждой статьи автора умножается на 3
        rating += Post.objects.filter(author = self.pk).aggregate(Sum('rating'))['rating__sum']*3
        # суммарный рейтинг всех комментариев автора
        rating += Comment.objects.filter(user = self.user).aggregate(Sum('rating'))['rating__sum']
        # суммарный рейтинг всех комментариев к статьям автора
        rating += Comment.objects.filter(post__author = self.pk).aggregate(Sum('rating'))['rating__sum']
        self.rating = rating
        self.save()
        return self.rating

