from django.urls import path
from . import views

# define application namespace to allow us to reference urls in applications
# by their name
app_name = 'blog'

urlpatterns = [

    # colinhowlin.com/blog/
    # path('', views.post_list, name='post_list'),
    path('', views.PostListView.as_view(), name='post_list'),

    # colinhowlin.com/2019/08/02/first-post/
    # angle brackets are used to capture values from URL
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail,
         name='post_detail')
]