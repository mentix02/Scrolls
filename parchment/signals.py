"""
Actions that have to take place
after the parchment/models.py's
models are going change - either
being inserted, deleted, or updated.
"""
from parchment.models import Parchment

from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import pre_save


# noinspection PyUnusedLocal
@receiver(pre_save, sender=Parchment)
def create_parchment_slug(sender, instance: Parchment, **kwargs):
    """
    Populates the slug attribute
    of the Parchment instance with
    django's inbuilt slugify
    method for text conversion.
    """
    instance.slug = slugify(instance.title)
