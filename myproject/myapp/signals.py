from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Appointment, Cancellation,Purchase,Vehicle
from utils.email_service import send_confirmation_email,send_purchase_notification_email

@receiver(post_save, sender=Appointment)
def appointment_status_changed(sender, instance, created, **kwargs):
    """
    Signal to detect when an appointment status changes to 'Confirmed'
    and send an email to the customer
    """
    # Skip if this is a new appointment (booking emails are handled in the view)
    if not created and instance.status == 'Confirmed':
        # Send confirmation email to customer
        send_confirmation_email(instance)

@receiver(post_save, sender=Purchase)

def vehicle_purchased(sender, instance, created, **kwargs):
    """
    Signal to detect when a purchase is created and update the vehicle status
    """
    if created and instance.status == 'Completed':
        # Update vehicle status to 'Sold'
        vehicle = instance.vehicle
        vehicle.status = 'Sold'
        vehicle.save(update_fields=['status'])

        # If the purchase has feedback, send purchase notification
        if hasattr(instance, 'feedback'):
            send_purchase_notification_email(instance, instance.feedback)

