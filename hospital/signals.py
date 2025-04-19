from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Bill, Transaction

@receiver(post_save, sender=Bill)
def create_initial_transaction(sender, instance, created, **kwargs):
    if created:
        Transaction.objects.create(
            bill=instance,
            amount=instance.amount,
            payment_method='unpaid'
        )
