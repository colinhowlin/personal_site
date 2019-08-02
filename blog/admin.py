from django.contrib import admin
from .models import Post

# TODO: Need to run createsuperuser command to access admin site


# Here we use a custom class that inherits from ModelAdmin to register our model.
# the @admin.... decorator registers our model
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # the list_display attribute allows us to set what fields we want to display
    # in the admin object list page
    list_display = ('title', 'slug', 'author', 'publish', 'status')

    # The list_filter attribute adds a sidebar allowing us to filter posts
    # by the fields included
    list_filter = ('status', 'created', 'publish', 'author')

    # Adding a search bar to the page is done by setting the search_fields
    # attribute and listing the fields we want to search by
    search_fields = ('title', 'body')

    # The slug field will be automatically filled in with the content of the
    # title field when we use this attribute
    prepopulated_fields = {'slug': ('title',)}

    # We can replace the author drop-down select with a user lookup by using
    # the raw_id_fields attribute
    raw_id_fields = ('author',)

    # This attribute groups posts into a date hierarchy based on the date
    # they were published
    date_hierarchy = 'publish'

    # This attributes instructs Django to order the posts first by status,
    # then by published date.
    ordering = ('status', 'publish')
