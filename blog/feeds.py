from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords

from .models import Post


class LatestPostFeed(Feed):
    """
    creating class for our blog feed
    ::title blog-title
    ::link link blog. but if we are making url path('feed/' ...), url will be example.com/feed/
    :: description blog desc
    items() - objects for channel
    item_title() - title of objects
    item_description() - desc of objects than truncatewords at 30 symbols
    """
    title = 'My Blog'
    link = '/blog/'
    description = 'New post of my blog'

    def items(self):
        return Post.objects.filter(status__iexact='published')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)
