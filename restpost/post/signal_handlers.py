import short_url

from django.db.models.signals import post_save
from django.dispatch import receiver

from post.models import Post


@receiver(post_save, sender=Post, dispatch_uid="generate_post_shorturl")
def generate_post_shorturl(sender, instance, **kwargs):
    instance.short_url = short_url.encode_url(instance.pk)
    instance.save()
