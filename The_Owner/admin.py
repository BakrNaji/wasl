from django.contrib import admin
from .models import Owner, ProjectCategory, Project, Photo , ProjectStatus

admin.site.register(Owner)
admin.site.register(ProjectCategory)
admin.site.register(Photo)
admin.site.register(ProjectStatus)



# from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.models import AnonymousUser
from .models import Message 
from django.contrib import admin
from .models import Message 
from django.utils.html import format_html

class MessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_conversation']  
    list_display_links = ['name']  

    def display_conversation(self, obj):
        # احصل على جميع رسائل المستخدم مرتبة بترتيب الزمن
        user_messages = Message.objects.filter(name=obj.name, admin_response__isnull=False).order_by('timestamp')
        
        conversation_html = "<div>"  # بداية القالب
        previous_user = None  # متغير لتتبع اسم المستخدم السابق
        for message in user_messages:
            # فقط إذا كان اسم المستخدم الحالي يختلف عن السابق نقوم بإضافته إلى القالب
            if message.name != previous_user:
                conversation_html += f"<div><strong>Name:</strong> {message.name}</div>"
                previous_user = message.name  # تحديث اسم المستخدم السابق ليكون الحالي
            # إضافة كل رسالة ورد للقالب
            conversation_html += f"<div><strong>User:</strong> {message.body}</div>"
            conversation_html += f"<div><strong>Admin:</strong> {message.admin_response}</div><hr>"
        conversation_html += "</div>"  # نهاية القالب
        
        return format_html(conversation_html)

    display_conversation.short_description = "Conversation"  # تعيين عنوان القالب في الإدارة

admin.site.register(Message, MessageAdmin)
