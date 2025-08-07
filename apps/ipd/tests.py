from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from .models import Ward, Bed, Admission, Discharge, VitalSign

User = get_user_model()

class IPDAPITest(APITestCase):
    def setUp(self):
        # create groups/users as needed...
        self.ward = Ward.objects.create(name="General")
        self.bed = Bed.objects.create(ward=self.ward, bed_number="G1")
        self.doctor = User.objects.create_user('doc', password='pass')
        self.nurse = User.objects.create_user('nurse', password='pass')
        self.patient = 1  # assume exists
        self.client = APIClient()

    def test_admission_flow(self):
        self.client.force_authenticate(self.doctor)
        resp = self.client.post('/api/ipd/admissions/', {
            "patient": self.patient,
            "ward": self.ward.id,
            "bed": self.bed.id,
            "reason": "Observation"
        })
        self.assertEqual(resp.status_code, 201)
        self.bed.refresh_from_db()
        self.assertTrue(self.bed.is_occupied)

    def test_vitalsign_recording(self):
        # admit first
        admission = Admission.objects.create(
            patient_id=self.patient,
            ward=self.ward,
            bed=self.bed,
            admitted_by=self.doctor,
            reason="Test"
        )
        self.client.force_authenticate(self.nurse)
        resp = self.client.post('/api/ipd/vitalsigns/', {
            "admission": admission.id,
            "temperature": 37.0,
            "bp_systolic": 120,
            "bp_diastolic": 80,
            "heart_rate": 75,
            "respiratory_rate": 18
        })
        self.assertEqual(resp.status_code, 201)

    def test_discharge_flow(self):
        admission = Admission.objects.create(
            patient_id=self.patient,
            ward=self.ward,
            bed=self.bed,
            admitted_by=self.doctor,
            reason="Test"
        )
        self.client.force_authenticate(self.doctor)
        resp = self.client.post('/api/ipd/discharges/', {
            "admission": admission.id,
            "summary_notes": "Recovered"
        })
        self.assertEqual(resp.status_code, 201)
        admission.refresh_from_db()
        self.assertEqual(admission.status, 'discharged')
        self.bed.refresh_from_db()
        self.assertFalse(self.bed.is_occupied)