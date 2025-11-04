from django.contrib import admin
from .models import Event,University,Profile
admin.site.register(University)
admin.site.register(Event)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "university")
    list_filter = ("role", "university")
    search_fields = ("user__username", "user__email")
