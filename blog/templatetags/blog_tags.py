from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe

import markdown
from blog.models import Post

register = template.Library()


@register.simple_tag()
def total_post():
    return Post.objects.count()


@register.inclusion_tag('blog/snippets/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.objects.filter(status__iexact='published').order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag()
def get_most_commented_post(count=5):
    # <QuerySet [<Post: Fouth Post>, <Post: Initial Post>, <Post: Second Post>, <Post: Third Post>, <Post: Five Post>]>
    return Post.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]

# creating filter for reformat html like https://daringfireball.net/projects/markdown/syntax
@register.filter(name='markdown')
def markdown_format(text):
    # mark_safe function of django to mark html as safe code
    return mark_safe(markdown.markdown(text))
