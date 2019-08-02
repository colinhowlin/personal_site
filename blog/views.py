from django.shortcuts import render, get_object_or_404
from .models import Post


def post_list(request):
    """Retrieve a list of published posts and pass them
    to the rendered template"""

    # Here we retrieve all the published posts using the custom model manager
    # we created in the models.py file
    posts = Post.published.all()

    # Then we use Django's render shortcut to render a template
    # and pass the posts to the given template
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})


def post_detail(request, year, month, day, post):
    """Retrieve a single post with the passed criteria and pass
    to the rendered template"""
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,)

    return render(request,
                  'blog/post/detail.html',
                  {'post': post})
