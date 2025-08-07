from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Admission, Discharge
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Admission)
def log_admission(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Patient {instance.patient.id} admitted to Bed {instance.bed.id}")

@receiver(post_save, sender=Discharge)
def log_discharge(sender, instance, **kwargs):
    logger.info(f"Patient {instance.admission.patient.id} discharged from Bed {instance.admission.bed.id}")