from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post


def post_list(request):
    """Retrieve a list of published posts and pass them
    to the rendered template"""

    # Here we retrieve all the published posts using the custom model manager
    # we created in the models.py file
    object_list = Post.published.all()

    # Then we create a Paginator object to limit the number of posts
    # to three per page
    paginator = Paginator(object_list, 3)

    # the GET page parameter stores the current page
    page = request.GET.get('page')

    try:
        # we obtain the posts for the desired page by using Paginator page() method
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page parameter is not a number, retrieve the first page of results
        posts = paginator.page(1)
    except EmptyPage:
        # if out of range, return the last page
        posts = paginator.page(paginator.num_pages)

    # Then we use Django's render shortcut to render a template
    # and pass the posts to the given template
    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts})


def post_detail(request, year, month, day, post):
    """Retrieve a single published post with the parameters
    passed to the method and render with the given template."""

    # We use get_object_or_404 to get the post. If the post is
    # not found, Django serves a HTTP 404 exception
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,)

    return render(request,
                  'blog/post/detail.html',
                  {'post': post})
