from django.contrib import admin
from .models import BandStory

@admin.register(BandStory)
class BandStoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'company', 'claps')
    search_fields = ('name', 'intro', 'vibe', 'costume', 'moments', 'reflection')
    list_filter = ('company', 'user')
    readonly_fields = ('claps',)
    ordering = ('-claps',)

    fieldsets = (
        (None, {
            'fields': ('user', 'company', 'name', 'photos')
        }),
        ('Story Details', {
            'fields': ('intro', 'vibe', 'costume', 'moments', 'reflection'),
            'classes': ('collapse',),
        }),
        ('Engagement', {
            'fields': ('claps',),
        }),
    )
