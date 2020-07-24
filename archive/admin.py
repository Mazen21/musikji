from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin

class CommentAdmin(admin.ModelAdmin):
    list_display = ('added_by', 'body', 'post', 'created_at', 'active')
    list_filter  = ('active','created_at')
    search_fields = ('added_by', 'body')
    actions = ['approve_comments']

    def approve_comments(self,request, queryset):
        queryset.update(active=True)

admin.site.register(Instrument)
admin.site.register(Maqam)
admin.site.register(Rythm)
admin.site.register(Jins)
admin.site.register(MusicForm)
admin.site.register(Artist)
admin.site.register(Song)
admin.site.register(Lyric)
admin.site.register(Score)
admin.site.register(Comment)
admin.site.register(MusicGenre)
admin.site.register(ArtistType)
admin.site.register(Vote)