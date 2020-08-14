from django.test import TestCase, Client
from flights.models import Flight, Airport,Passenger
from django.db.models import Max

# Create your tests here.
class FlightTestCase (TestCase):
    def setUp(self):
        a1= Airport.objects.create(city="AAA" ,code="A")
        a2= Airport.objects.create(city="BBB", code="B")

        Flight.objects.create(origin=a1, destination=a2, duration=100)
        Flight.objects.create(origin=a1, destination=a1, duration=10)
        Flight.objects.create(origin=a1, destination=a2, duration=-10)

    def test_departures_count(self):
        a= Airport.objects.get(code="A")
        self.assertEqual(a.departures.count(), 3)
    def test_arrivals_count(self):
        a= Airport.objects.get (code="A")
        self.assertEqual(a.arrivals.count(), 1)

    def test_valid_flight(self):
        a1= Airport.objects.get(code="A")
        a2= Airport.objects.get(code="B")
        f= Flight.objects.get(origin= a1, destination=a2, duration=100)
        self.assertTrue (f.is_valid_flight())

    def test_invalid_flight_destination(self):
        a1= Airport.objects.get(code="A")
        f= Flight.objects.get(origin= a1, destination=a1, duration=10)
        self.assertFalse(f.is_valid_flight())

    def test_invalid_flight_duration(self):
        a1= Airport.objects.get(code="A")
        a2= Airport.objects.get(code="B")
        f= Flight.objects.get(origin= a1, destination=a2, duration=-10)
        self.assertFalse(f.is_valid_flight())

    def test_index(self):
        c=Client()
        response= c.get("/flights/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["flights"].count(), 3)

    def test_valid_flight_page(self):
        a1= Airport.objects.get(code="A")
        f=Flight.objects.get(origin= a1, destination=a1)
        c=Client()
        response= c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)

    def test_invalid_flight_page(self):
        max_id = Flight.objects.all().aggregate(Max("id"))["id__max"]

        c = Client()
        response = c.get(f"/flights/{max_id + 1}")
        self.assertEqual(response.status_code, 404)

    def test_flight_page_passengers(self):
        f=Flight.objects.get(pk=1)
        p=Passenger.objects.create(first='Roya', last='Shourouni')
        f.passenger.add(p)

        c=Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["passengers"].count(),1)
    
    def test_flight_page_nonpassengers(self):
        f=Flight.objects.get(pk=1)
        p=Passenger.objects.create(first='Roya', last='Shourouni')

        c=Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["non_passengers"].count(),1)

