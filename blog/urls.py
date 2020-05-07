from django.urls import path, re_path
from .views import IndexView, PostDetail, post_email



urlpatterns = [
    path('', IndexView.as_view(), name='index_list'),
    path('post/<str:slug>/<int:year>/<int:month>/<int:day>/', PostDetail.as_view(), name='post_detail'),
    # path('post/<str:slug>/<int:year>/<int:month>/<int:day>', save_comment, name='save_comment'),
    # re_path(r'^(?P<post_id>\d+)/share/$', post_email, name='post_share'),
    path('<int:post_id>/share/', post_email, name='post_share'),
]
