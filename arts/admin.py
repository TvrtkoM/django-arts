from django.contrib import admin

from models import Artist, Art

admin.site.register(Artist)

class ArtAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Art)