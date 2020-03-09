from django.contrib import admin

from thought.models import Thought


class ThoughtAdmin(admin.ModelAdmin):
    search_fields = ['body']


admin.site.register(Thought, ThoughtAdmin)
