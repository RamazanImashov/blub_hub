from django.contrib import admin
from .models import Video, Topics


class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'topics', 'created_at']
    list_filter = ['topics']
    search_fields = ['title', 'description']


admin.site.register(Video, VideoAdmin)
admin.site.register(Topics)
