from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# This is a custom model manager class that filters the queryset on
# whether the post is published or not.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset()\
                                            .filter(status='published')


# Class to represent our blog posts. Inherits from Django's models.Model class
class Post(models.Model):

    # Here we define a CHOICES data structure to hold options for a data field.
    # Note: this is not a data field, but can be referenced by one.
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    # Here we define our table fields
    title = models.CharField(max_length=250) # standard CharField to represent VARCHAR datatype in database

    # The SlugField is used when constructing the URL for our blog post.
    # 'unique_for_date' ensures that no two posts will have the same slug for a given date.
    slug = models.SlugField(max_length=250, unique_for_date='publish')

    # Here we set up a Many-to-One relationship to the User model in the Django Auth system
    # The foreign key is the primary key of the related model.
    # on_delete is set to CASCADE, which means if the related user is deleted,
    # all their blog posts will be as well.
    # The related_name attribute specifies the name of the reverse relationship, i.e from User to Post
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')

    # The body of the blog post as a TextField which translates to TEXT column in SQL database
    body = models.TextField()

    # Field to hold the published date of the post.
    # defaults to the current time.
    # Using Django's timezone.now method to get timezone aware datetime
    publish = models.DateTimeField(default=timezone.now)

    # When post was created is represented by the created field.
    # auto_add_now=True means this will be set to the current time when the post is created.
    created = models.DateTimeField(auto_now_add=True)

    # This field holds when the post was last updated.
    # Using auto_add=True means this will be automatically set to current time whenever the
    # post is saved.
    updated = models.DateTimeField(auto_now=True)

    # The status of the blog post - published or draft.
    # We use the choices attribute which means this can only be one of the values in the
    # choices parameter defined at the top of the class.
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    # THis inner class contains the post meta data.
    # The ordering specifies that posts appear in the order they were published.
    # The negative prefix means the posts will appear with most recent first.
    class Meta:
        ordering = ('-publish',)

    # Here we define objects as the default model manager
    objects = models.Manager()
    # And published as the custom manager we defined at the top of the file.
    published = PublishedManager()

    def get_absolute_url(self):
        """This method returns the canonical URL for a specific post"""

        # Using the urls.reverse method we can build a URL from a name and
        # by passing optional parameters.
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])

    # String representation of the class which will return the blog post title
    def __str__(self):
        return self.title
