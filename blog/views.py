from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count

from taggit.models import Tag

from .models import Post, Comment
from .forms import EmailPostForm, CommentForm


# Create your views here.


class IndexView(ListView):
    template_name = 'blog/index.html'  # template name
    model = Post  # model for context - Post.objects.all()
    paginate_by = 2  # pagination by 2 posts
    queryset = model.objects.filter(status__iexact='published') # queryset for only published posts
    # context_object_name = posts # if we need to change context from 'object_list' to something
    tag = None

    def get_queryset(self):
        # if got kwargs > redirect to 'tag/<str:slug>/' and creatind qs with filter tag.slug
        if self.kwargs:
            # getting tag for kwargs (in model function "get_tag_url")
            self.tag = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
            # filtering qs with tags
            qs = self.queryset.filter(tags__in=[self.tag])
            return qs
        else:
            # if index page and not slug filter
            return self.queryset


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_queryset(self):
        return self.model.objects.filter(slug__iexact=self.kwargs.get('slug'),
                                         status__iexact='published',
                                         publish__year=self.kwargs.get('year'),
                                         publish__month=self.kwargs.get('month'),
                                         publish__day=self.kwargs.get('day'))

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        post = self.get_queryset().get()
        # getting id current post's tag <QuerySet [3]>
        post_tags_ids = post.tags.values_list('id', flat=True)
        # filtering posts by tags in list post_tags_ids, and excluding current post.
        similar_post = self.model.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
        # top 4 post, by similar tags
        similar_post = similar_post.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
        context['comment_form'] = CommentForm
        # from QuerySet of Posts, method get() getting an object, then we getting by related_name comments and
        # filtering them active = True
        context['comments'] = self.get_queryset().get().comments.filter(active=True)
        print(similar_post)
        context['similar_posts'] = similar_post
        return context

    def post(self, request, *args, **kwargs):
        # comment was posted
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            # creating object for db, but not saving
            new_comment = comment_form.save(commit=False)
            # assign the current post to the comment, from queryset getting instance
            new_comment.post = self.get_queryset().get()
            # savind comment to db
            new_comment.save()
            # ?? #self.object = self.get_object
            self.object = self.get_queryset().get()
            # ??
            context = context = super().get_context_data(**kwargs)
            context['comment_form'] = CommentForm
            context['comments'] = self.get_queryset().get().comments.filter(active=True)

            return self.render_to_response(context=context)
        else:
            # if not post, just render from
            self.object = self.get_queryset().get()
            context = super().get_context_data(**kwargs)
            context['comment_form'] = comment_form

            return self.render_to_response(context=context)


def post_email(request, post_id):
    # get back post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # form was submitted:
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # forms fields passed validation
            cd = form.cleaned_data
            # send mail
            # creating url of post,  build_absolute_uri() creating full url  http://site.com/post/1/
            post_url = request.build_absolute_uri(post.get_absolute_url())
            # message subject for send mail
            subject = f"{cd['name']}, {cd['email_from']} recommends your reading {post.title}"
            # message for send_mail
            message = f"Read {post.title}, at {post_url} \n\n {cd['name']} \n {cd['comments']}"
            # send_mail(subject, message, from, [to])
            send_mail(subject, message, settings.EMAIL_HOST_USER, [cd['email_to']])
            sent = True

    else:
        # render empty form
        form = EmailPostForm()

    return render(request, 'blog/share_post.html', {'post': post, 'form': form, 'sent': sent})
