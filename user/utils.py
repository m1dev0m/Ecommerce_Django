import random
from django.core.mail import send_mail

def send_verification_email(user):
    code = str(random.randint(100000, 999999))
    user.verification_code = code
    user.save()
    send_mail(
        'Ваш код верификации',
        f'Ваш код подтверждения: {code}',
        '@gmail.com',
        [user.email],
        fail_silently=False,
    )
