import typing

from django.db import models

from taggit.managers import TaggableManager


class Parchment(models.Model):
    """
    Parchment model - acts as the "post"
    model for the blog (named Scrolls).
    Has all the generic attributes of a post ->
        title: str
        body: str
        draft: boolean
        tags: list of strings
        slug: dash separated title
        timestamp: datetime object

    Has inbuilt ordering with respect
    to reverse timestamp (and if not)
    then primary keys. Slugs are auto
    generated via helper methods that
    live in parchment/signals.py file.
    """

    # tags are used via a 3rd
    # party django module. A custom
    # implementation would be too
    # much hassle involving string
    # separation and having a new app
    # only for Tags, etc.
    tags = TaggableManager()

    body = models.TextField()
    title = models.CharField(max_length=100)
    draft = models.BooleanField(default=False)

    # slugs are human readable but
    # pre-urlencoded strings that
    # are generally directed related
    # to a field of a model - in this
    # case, the title of a Parchment.
    slug = models.SlugField(max_length=200, blank=True)

    # just in case someone else
    # wants to try out Scrolls.
    # Maybe it can be a 3rd party
    # pluggable app for a custom
    # blogging application.
    #
    # TODO look into configuring default AUTHOR settings.
    author = models.CharField(max_length=200, default='mentix02')

    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        """
        For the admin page.
        """
        return self.title

    class Meta:
        """
        Reverses the order of Parchments
        so that newer instances appear first
        sorting by timestamp but if one is
        updated, it's timestamp is updated as
        well and thus an older Parchment that
        was changed would appear newer as well.

        TODO implement a boolean attribute that
             would change to True once a Parchment
             has been updated.
        """
        ordering = ('-timestamp', '-pk')

    def add_tag(self, tag: str) -> typing.List[str]:
        """
        A helper method for easily adding
        tags to a Parchment instance while
        also returning the updated list of them (tags).
        """
        self.tags.add(tag)
        return [tag.name for tag in self.tags.all()]

    def serialize(self) -> typing.Dict[str, str]:
        """
        A custom serializer method that converts
        important fields of a Parchment instance
        into a Python dict object that can be used
        to convert to json easily for AJAX or
        other REST-like purposes.
        """
        return {
            'slug': self.slug,
            'body': self.body,
            'title': self.title,
            'author': self.author,
            'tags': [tag.name for tag in self.tags.all()],
            'timestamp': self.timestamp.strftime('%b. %d, %Y')
        }
