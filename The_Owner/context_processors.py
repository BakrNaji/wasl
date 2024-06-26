# The_Owner/context_processors.py
from .models import Message

def unread_messages_count(request):
    if request.user.is_authenticated:
        return {'unread_count': Message.objects.filter(name=request.user, is_read=False).count()}
    return {'unread_count': 0}
