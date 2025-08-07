from django.utils import timezone
from django.core import mail
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from .models import DrugCategory, Drug, Stock, Prescription, PrescriptionItem

User = get_user_model()

class PharmacyAPITest(APITestCase):
    def setUp(self):
        self.cat = DrugCategory.objects.create(name="Analgesic")
        self.drug = Drug.objects.create(name="Ibuprofen", category=self.cat, unit_price=2.00)
        self.user = User.objects.create_user('pharma', password='pass')
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_drug_list_and_create(self):
        # list
        resp = self.client.get('/api/pharmacy/drugs/')
        self.assertEqual(resp.status_code, 200)

        # create
        data = {
            "name": "Paracetamol",
            "unit_price": "1.50",
            "category_id": self.cat.id
        }
        resp = self.client.post('/api/pharmacy/drugs/', data)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(Drug.objects.count(), 2)

    def test_low_stock_signal_via_api(self):
        # Add a Stock below threshold
        resp = self.client.post('/api/pharmacy/stocks/', {
            "drug_id": self.drug.id,
            "batch_no": "B1",
            "quantity": 5,
            "expiry_date": timezone.localdate().isoformat()
        })
        self.assertEqual(resp.status_code, 201)
        # Signal should have sent one email
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Low Stock Alert: Ibuprofen", mail.outbox[0].subject)

    def test_prescription_and_dispense_flow(self):
        # Create Prescription with items
        payload = {
            "patient": 1,  # assumes patient pk=1 exists
            "prescribed_by": self.user.id,
            "items": [
                {"drug_id": self.drug.id, "dosage": "Take once daily", "quantity": 2}
            ]
        }
        resp = self.client.post('/api/pharmacy/prescriptions/', payload, format='json')
        self.assertEqual(resp.status_code, 201)
        presc_id = resp.data['id']
        item_id = resp.data['items'][0]['id']

        # Dispense it
        resp = self.client.post('/api/pharmacy/dispensations/', {
            "prescription_item_id": item_id,
            "dispensed_by": self.user.id
        })
        self.assertEqual(resp.status_code, 201)