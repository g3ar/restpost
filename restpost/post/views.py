import short_url
from django.shortcuts import redirect


def short_url_reverse(request, hash):
    post_id = short_url.decode_url(hash)
    return redirect('post-detail', pk=post_id)
