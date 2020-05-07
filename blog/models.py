from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.

class Post(models.Model):
    """
    model for Post
    """
    STATUS_CHOISES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    class Meta:
        ordering = ['-publish']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    title = models.CharField('Название', max_length=128)
    slug = models.SlugField(max_length=250, unique_for_date='publish', db_index=True)
    author = models.ForeignKey(User, related_name='blog_post', on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOISES, default='draft')

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug,
                                              'year': self.publish.year,
                                              'month': self.publish.month,
                                              'day': self.publish.day})

    # def get_comment_save(self):
    #     return reverse('save_comment', kwargs={'slug': self.slug,
    #                                            'year': self.publish.year,
    #                                            'month': self.publish.month,
    #                                            'day': self.publish.day})


class Comment(models.Model):
    """
    model for comments at our posts, foreign key for posts
    """

    class Meta:
        ordering = ('created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
