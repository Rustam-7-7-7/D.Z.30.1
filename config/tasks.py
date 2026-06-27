from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.models import User

@shared_task
def send_course_update_email(course_id, user_email):
    send_mail(
        'Обновление курса',
        f'Курс с ID {course_id} был обновлен.',
        'from@example.com',
        [user_email],
        fail_silently=False,
    )

@shared_task
def deactivate_inactive_users():
    one_month_ago = timezone.now() - timezone.timedelta(days=30)
    User.objects.filter(last_login__lt=one_month_ago, is_active=True).update(is_active=False)
