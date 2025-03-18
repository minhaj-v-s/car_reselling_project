from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_booking_email(appointment):
    """
    Send email to admin when a new booking is created
    """
    subject = 'New Test Drive Booking'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = settings.ADMIN_EMAIL
    
    # Context for the template
    context = {
        'appointment': appointment,
        'admin_url': f"{settings.SITE_URL}admin/",
    }
    
    # Render HTML content
    html_content = render_to_string('emails/booking_notification.html', context)
    text_content = strip_tags(html_content)  # Plain text version
    
    # Create the email
    email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    email.attach_alternative(html_content, "text/html")
    email.send()

def send_cancellation_email(appointment, reason, cancellation_time):
    """
    Send email to admin when a booking is cancelled
    """
    subject = 'Booking Cancelled'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = settings.ADMIN_EMAIL
    
    # Context for the template
    context = {
        'appointment': appointment,
        'reason': reason,
        'cancellation_time': cancellation_time,
    }
    
    # Render HTML content
    html_content = render_to_string('emails/cancellation_notification.html', context)
    text_content = strip_tags(html_content)  # Plain text version
    
    # Create the email
    email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    email.attach_alternative(html_content, "text/html")
    email.send()

def send_confirmation_email(appointment):
    """
    Send email to customer when their booking is confirmed
    """
    subject = 'Your Test Drive Appointment is Confirmed!'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = appointment.customer.email
    
    # Context for the template
    context = {
        'appointment': appointment,
        'website_url': settings.SITE_URL,
    }
    
    # Render HTML content
    html_content = render_to_string('emails/confirmation_notification.html', context)
    text_content = strip_tags(html_content)  # Plain text version
    
    # Create the email
    email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    email.attach_alternative(html_content, "text/html")
    email.send()

def send_purchase_notification_email(purchase, feedback):
    """
    Send email to admin when a vehicle is purchased
    """
    
    subject = 'Vehicle Purchase Notification'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = settings.ADMIN_EMAIL
    
    # Context for the template
    context = {
        'purchase': purchase,
        'feedback': feedback,
        'admin_url': f"{settings.SITE_URL}admin/",
    }
    
    # Render HTML content
    html_content = render_to_string('emails/purchase_notification.html', context)
    text_content = strip_tags(html_content)  # Plain text version

    # Create the email
    email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    email.attach_alternative(html_content, "text/html")
    email.send()