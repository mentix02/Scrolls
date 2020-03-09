from parchment.models import Parchment

from django.contrib import admin


class ParchmentAdmin(admin.ModelAdmin):
    search_fields = ['title', 'timestamp']
    prepopulated_fields = {
        'slug': ('title',)
    }


admin.site.register(Parchment, ParchmentAdmin)
