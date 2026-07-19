"""
Celery tasks for user-related emails.
"""

from __future__ import annotations

import os

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


# =============================================================================
# Internal Helper
# =============================================================================


# def _send_email(
#     *,
#     subject: str,
#     recipient: str,
#     html_template: str,
#     text_template: str,
#     context: dict,
# ) -> None:
#     """
#     Render and send an email.
#     """

#     text_body = render_to_string(
#         text_template,
#         context,
#     )

#     html_body = render_to_string(
#         html_template,
#         context,
#     )

#     email = EmailMultiAlternatives(
#         subject=subject,
#         body=text_body,
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to=[recipient],
#     )

#     email.attach_alternative(
#         html_body,
#         "text/html",
#     )

#     email.send(
#         fail_silently=False,
#     )

def _send_email(
    *,
    subject: str,
    recipient: str,
    html_template: str,
    text_template: str,
    context: dict,
) -> None:
    print("TEXT TEMPLATE:", text_template)
    print("HTML TEMPLATE:", html_template)

    text_body = render_to_string(
        text_template,
        context,
    )

    html_body = render_to_string(
        html_template,
        context,
    )

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient],
    )

    email.attach_alternative(
        html_body,
        "text/html",
    )

    # ---------------- DEBUG ----------------

    print("=" * 60)
    print("ABOUT TO SEND EMAIL")
    print("Recipient:", recipient)
    print("Subject:", subject)

    count = email.send(
        fail_silently=False,
    )

    print("EMAIL.SEND() RETURNED:", count)
    print("=" * 60)

    with open("email-debug.txt", "a", encoding="utf-8") as f:
        f.write(
            f"recipient={recipient}, subject={subject}, sent={count}\n"
        )

    # ---------------------------------------


# =============================================================================
# Password Reset
# =============================================================================


@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True,
    retry_kwargs={
        "max_retries": settings.EMAIL_MAX_RETRIES,
    },
)

def send_password_reset_email(
    *,
    recipient: str,
    full_name: str,
    reset_url: str,
) -> None:
    """
    Send a password reset email.
    """
    _send_email(
        subject="Réinitialisation de votre mot de passe",
        recipient=recipient,
        html_template="emails/password_reset.html",
        text_template="emails/password_reset.txt",
        context={
            "full_name": full_name,
            "reset_url": reset_url,
        },
    )


# =============================================================================
# Email Verification
# =============================================================================


@shared_task
def send_email_verification_email(
    *,
    recipient: str,
    full_name: str,
    verification_url: str,
):
    with open("celery-test.txt", "a", encoding="utf-8") as f:
        f.write(
            f"PID={os.getpid()} recipient={recipient}\n"
        )

    _send_email(
        subject="Test",
        recipient=recipient,
        html_template="emails/verification.html",
        text_template="emails/verification.txt",
        context={
            "full_name": full_name,
            "verification_url": verification_url,
        },
        
    )
    
    
# =============================================================================
# Welcome
# =============================================================================


@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True,
    retry_kwargs={
        "max_retries": settings.EMAIL_MAX_RETRIES,
    },
)
def send_welcome_email(
    *,
    recipient: str,
    full_name: str,
) -> None:
    """
    Send a welcome email.
    """

    _send_email(
        subject="Bienvenue chez LWNF",
        recipient=recipient,
        html_template="emails/welcome.html",
        text_template="emails/welcome.txt",
        context={
            "full_name": full_name,
        },
    )