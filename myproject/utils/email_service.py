from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.core.mail import send_mail
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

def send_admin_cancellation_email(appointment):
    """
    Send email to customer when their appointment is cancelled by admin
    """
    subject = 'Your Test Drive Appointment Has Been Cancelled'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = appointment.customer.email
    
    # Context for the template
    context = {
        'appointment': appointment,
        'website_url': settings.SITE_URL,
    }
    
    # Render HTML content
    html_content = render_to_string('emails/admin_cancellation_notification.html', context)
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


def send_otp_email(user, otp):
    """Send OTP to user's email for password reset"""

    subject = "Password Reset OTP - Soorath Autos"

    html_message = f"""
    <div style = "font-family: 'Arial', sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 5px;">
        <div style = "text-align: center; margin-bottom: 20px;">
            <h2 style = "color: #D01000;"> Soorath Autos Password Reset</h2>
        </div>

        <div style="padding: 20px; background-color: #f9f9f9; border-radius: 5px;">
            <p>Hello {user.name},</p>
            <p>We received a request to reset your password. Please use the following One Time Password (OTP) to reset your password:</p>
            
            <div style = "text-align: center; margin: 30px 0;">
                <div style = "display: inline-block; padding: 12px 30px; background-color: #f0f0f0; border-radius: 5px; letter-spacing: 8px; font-size: 24px; font-weight: bold;">
                    {otp}
                </div>
            </div>

            <p>This OTP is valid for 15 minutes. If you did not request a password reset, please ignore this email or contact support if you have concerns. </p>
            <p>Thank you, <br> Soorath Autos Team</p>
        </div>

        <div style= "text-align:center; margin-top: 20px; font-size: 12px; color:#888;">
            <p>This is an automated message, please do not reply to this email.</p>
        </div>
    </div>
    """

    from_email = "mtem7118@gmail.com" 
    recipient_list = [user.email]

    send_mail(
        subject,
        "Please use this OTP to reset your password: " +otp,
        from_email,
        recipient_list,
        html_message=html_message,
        fail_silently = False,
    )
