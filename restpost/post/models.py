from django.db import models
from django.utils.translation import gettext as _
from django.conf import settings


class CreatedBase(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)
        abstract = True


class Post(CreatedBase):
    title = models.CharField(_('Title'), max_length=64)
    text = models.TextField(_('Text'))
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='posts',
                               on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} - {self.author}'

    def get_likes_count(self):
        return self.likes.count()

    def get_author_name(self):
        return self.author.username


class Like(CreatedBase):
    post = models.ForeignKey(Post, related_name='likes',
                             on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='liked_posts',
                               on_delete=models.CASCADE)

    class Meta(CreatedBase.Meta):
        unique_together = ['post', 'author']
