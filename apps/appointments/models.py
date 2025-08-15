from django.db import models
from django.utils import timezone

class Appointment(models.Model):
    doctor = models.ForeignKey("doctors.Doctor", on_delete=models.PROTECT)
    patient = models.ForeignKey("patients.Patient", on_delete=models.PROTECT)
    appointment_time = models.DateTimeField()
    token_number = models.PositiveIntegerField(null=True, blank=True)

    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')

 #   def save(self, *args, **kwargs):
  #      if self._state.adding and self.token_number is None:
   #         today = timezone.localdate()
    #        count = Appointment.objects.filter(
     #           doctor=self.doctor,
      #          appointment_time__date=today
       #     ).count()
        #    self.token_number = count + 1
        #super().save(*args, **kwargs)

    class Meta:
        ordering = ["appointment_time"]
        unique_together = [("doctor", "appointment_time")]

    def __str__(self):
        return f"{self.patient} with {self.doctor} at {self.appointment_time}"