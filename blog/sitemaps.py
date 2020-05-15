from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    # frequency of post changing
    # https://docs.djangoproject.com/en/3.0/ref/contrib/sitemaps/
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.objects.all()

    # should return datetime
    def lastmod(self, obj):
        return obj.publish