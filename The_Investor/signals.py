from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Evaluation
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone


@receiver(pre_save, sender=Evaluation)
def evaluation_pre_save(sender, instance, **kwargs):
    # store previous status to detect changes in post_save
    if instance.pk:
        try:
            prev = Evaluation.objects.get(pk=instance.pk)
            instance._pre_save_status = prev.status
        except Evaluation.DoesNotExist:
            instance._pre_save_status = None
    else:
        instance._pre_save_status = None


@receiver(post_save, sender=Evaluation)
def evaluation_post_save(sender, instance, created, **kwargs):
    subject = ''
    message = ''
    from_email = getattr(settings, 'DEFAULT_FORM_EMAIL', settings.EMAIL_HOST_USER)

    # on creation -> notify investor and admin
    if created:
        subject = 'تم إرسال تقييم جديد'
        message = f'تم إرسال تقييم جديد للمستثمر {instance.investor.user.username} من قبل {instance.evaluator.user.username if instance.evaluator else "N/A"}.\nحالة التقييم: {instance.status}.\nالتعليق: {instance.comment or "لا يوجد"}.'
        recipients = [instance.investor.user.email]
        # also notify site admin email if present
        if settings.EMAIL_HOST_USER:
            recipients.append(settings.EMAIL_HOST_USER)
        try:
            send_mail(subject, message, from_email, recipients, fail_silently=True)
        except Exception:
            pass

    # on status change (e.g., approved/rejected)
    prev_status = getattr(instance, '_pre_save_status', None)
    if prev_status and prev_status != instance.status:
        if instance.status in ('approved', 'rejected'):
            subject = f'تحديث حالة التقييم: {instance.status}'
            message = f'حالة التقييم للمستثمر {instance.investor.user.username} تم تغييرها إلى {instance.status} من قبل {instance.approved_by.username if instance.approved_by else "النظام"}.'
            recipients = [instance.investor.user.email]
            if instance.evaluator and instance.evaluator.user.email:
                recipients.append(instance.evaluator.user.email)
            try:
                send_mail(subject, message, from_email, recipients, fail_silently=True)
            except Exception:
                pass
