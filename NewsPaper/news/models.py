from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce


class Author(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    rating = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def update_rating(self):

        author_posts_rating = self.posts.aggregate(apr=Coalesce(Sum('rating'), 0))['apr']

        author_comments_rating = self.user.comments.aggregate(acr=Coalesce(Sum('rating'), 0))['acr']

        author_posts_comments_rating = self.posts.aggregate(apcr=Coalesce(Sum('comment__rating'), 0))['apcr']

        self.rating = author_posts_rating * 3 + author_comments_rating + author_posts_comments_rating
        self.save()

    def __str__(self):
        return f"{self.user.username}"


class Category(models.Model):

    name = models.CharField(max_length=255,
                            unique=True)

    subscribers = models.ManyToManyField(User,
                                         related_name='categories')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Post(models.Model):

    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')

    article = 'ART'
    news = 'NEW'

    POSTS = [
        (article, "Статья"),
        (news, "Новость")
    ]

    type = models.CharField(max_length=3,
                            choices=POSTS,
                            default=article)

    creation_time = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=255)

    text = models.TextField()

    rating = models.IntegerField(default=0)

    category = models.ManyToManyField(Category, through='PostCategory')

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return f'/news/{self.id}'


class Comment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    text = models.TextField()

    creation_time = models.DateTimeField(auto_now_add=True)

    rating = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class PostCategory(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post}: {self.category}'

    class Meta:
        verbose_name = 'Промежуточная модель PostCategory'
        verbose_name_plural = 'Промежуточная модель PostCategories'


from django.db import models

# Create your models here.
