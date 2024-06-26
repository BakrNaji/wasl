from django.contrib import admin
from .models import Chat, FeasibilityStudy, FeasibilityStudyRequest

class ChatInline(admin.TabularInline):
    model = Chat
    extra = 0
    readonly_fields = ['admin', 'owner', 'investor', 'text', 'date']

class FeasibilityStudyAdmin(admin.ModelAdmin):
    list_display = ['project_name', 'owner', 'investor', 'created_at', 'is_allowed']
    search_fields = ['project_name', 'owner__user__username', 'investor__user__username']
    inlines = [ChatInline]

class FeasibilityStudyRequestAdmin(admin.ModelAdmin):
    list_display = ['project_name', 'user', 'created_at', 'study_type']
    search_fields = ['project_name', 'user__username']

admin.site.register(Chat)
admin.site.register(FeasibilityStudy, FeasibilityStudyAdmin)
admin.site.register(FeasibilityStudyRequest, FeasibilityStudyRequestAdmin)
