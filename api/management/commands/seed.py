from django.core.management.base import BaseCommand
from api.models import Destination, Hotel, Cab


class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **options):
        # Clear existing data
        Destination.objects.all().delete()
        Hotel.objects.all().delete()
        Cab.objects.all().delete()

        # Create Destinations
        destinations = [
            {
                'name': 'Agra',
                'description': 'Home to the iconic Taj Mahal, one of the Seven Wonders of the World.',
                'city': 'Agra',
                'state': 'Uttar Pradesh',
                'country': 'India',
                'best_time_to_visit': 'October to March',
                'attractions': ['Taj Mahal', 'Agra Fort', 'Mehtab Bagh'],
                'average_cost': 5000,
                'rating': 4.8,
            },
            {
                'name': 'Jaipur',
                'description': 'The Pink City known for its vibrant culture and historical architecture.',
                'city': 'Jaipur',
                'state': 'Rajasthan',
                'country': 'India',
                'best_time_to_visit': 'September to March',
                'attractions': ['City Palace', 'Jantar Mantar', 'Hawa Mahal'],
                'average_cost': 4000,
                'rating': 4.6,
            },
            {
                'name': 'Goa',
                'description': 'Tropical paradise with beautiful beaches and Portuguese architecture.',
                'city': 'Goa',
                'state': 'Goa',
                'country': 'India',
                'best_time_to_visit': 'November to February',
                'attractions': ['Baga Beach', 'Fort Aguada', 'Basilica of Bom Jesus'],
                'average_cost': 6000,
                'rating': 4.7,
            },
            {
                'name': 'Kerala',
                'description': 'God\'s own country with lush backwaters and tropical beauty.',
                'city': 'Kochi',
                'state': 'Kerala',
                'country': 'India',
                'best_time_to_visit': 'September to February',
                'attractions': ['Backwaters', 'Chinese Fishing Nets', 'Fort Kochi'],
                'average_cost': 5500,
                'rating': 4.8,
            },
            {
                'name': 'Ladakh',
                'description': 'High-altitude desert with breathtaking mountain scenery.',
                'city': 'Leh',
                'state': 'Ladakh',
                'country': 'India',
                'best_time_to_visit': 'June to September',
                'attractions': ['Pangong Lake', 'Nubra Valley', 'Khardung La'],
                'average_cost': 7000,
                'rating': 4.9,
            },
            {
                'name': 'Varanasi',
                'description': 'Spiritual capital of India with sacred ghats along the Ganges.',
                'city': 'Varanasi',
                'state': 'Uttar Pradesh',
                'country': 'India',
                'best_time_to_visit': 'October to March',
                'attractions': ['Kashi Vishwanath Temple', 'Ganges Ghats', 'Sarnath'],
                'average_cost': 3500,
                'rating': 4.5,
            },
        ]

        created_destinations = []
        for dest_data in destinations:
            destination = Destination.objects.create(**dest_data)
            created_destinations.append(destination)
            self.stdout.write(self.style.SUCCESS(f'Created destination: {destination.name}'))

        # Create Hotels
        hotels_data = [
            {
                'name': 'Taj View Hotel',
                'location': 'Agra',
                'destination': created_destinations[0],
                'description': 'Luxury hotel with direct view of Taj Mahal',
                'price_per_night': 8000,
                'rating': 4.7,
                'amenities': ['WiFi', 'AC', 'Restaurant', 'Pool'],
                'available_rooms': 15,
                'total_rooms': 30,
                'phone': '+91-9876543210',
                'email': 'info@tajview.com',
            },
            {
                'name': 'Jaipur Palace Hotel',
                'location': 'Jaipur',
                'destination': created_destinations[1],
                'description': 'Royal experience in the heart of Pink City',
                'price_per_night': 6000,
                'rating': 4.5,
                'amenities': ['WiFi', 'Spa', 'Gym', 'Restaurant'],
                'available_rooms': 20,
                'total_rooms': 40,
                'phone': '+91-9876543211',
                'email': 'info@jaipurpalace.com',
            },
            {
                'name': 'Goa Beach Resort',
                'location': 'Goa',
                'destination': created_destinations[2],
                'description': 'Beach resort with water sports and evening entertainment',
                'price_per_night': 5500,
                'rating': 4.6,
                'amenities': ['Beach Access', 'Pool', 'Restaurant', 'Bar'],
                'available_rooms': 25,
                'total_rooms': 50,
                'phone': '+91-9876543212',
                'email': 'info@goabeach.com',
            },
            {
                'name': 'Kerala Backwaters Resort',
                'location': 'Kochi',
                'destination': created_destinations[3],
                'description': 'Serene resort overlooking the backwaters',
                'price_per_night': 7000,
                'rating': 4.8,
                'amenities': ['Backwater View', 'Boat Tours', 'Restaurant', 'Spa'],
                'available_rooms': 18,
                'total_rooms': 35,
                'phone': '+91-9876543213',
                'email': 'info@keralaresort.com',
            },
            {
                'name': 'Ladakh Mountain Lodge',
                'location': 'Leh',
                'destination': created_destinations[4],
                'description': 'Cozy lodge with stunning mountain views',
                'price_per_night': 4500,
                'rating': 4.4,
                'amenities': ['Mountain View', 'Heater', 'Restaurant', 'Tour Assistance'],
                'available_rooms': 12,
                'total_rooms': 25,
                'phone': '+91-9876543214',
                'email': 'info@ladakhlodge.com',
            },
        ]

        for hotel_data in hotels_data:
            hotel = Hotel.objects.create(**hotel_data)
            self.stdout.write(self.style.SUCCESS(f'Created hotel: {hotel.name}'))

        # Create Cabs
        cabs_data = [
            {
                'company_name': 'TourCabs',
                'vehicle_type': 'economy',
                'price_per_km': 8,
                'price_per_hour': 400,
                'capacity': 4,
                'rating': 4.5,
                'phone': '+91-9876543220',
                'email': 'info@tourcabs.com',
                'available_cars': 25,
                'description': 'Affordable cab service for budget travelers',
            },
            {
                'company_name': 'Premium Rides',
                'vehicle_type': 'premium',
                'price_per_km': 15,
                'price_per_hour': 800,
                'capacity': 5,
                'rating': 4.7,
                'phone': '+91-9876543221',
                'email': 'info@premiumrides.com',
                'available_cars': 15,
                'description': 'Comfortable premium cabs for leisure travel',
            },
            {
                'company_name': 'Luxury Transport',
                'vehicle_type': 'luxury',
                'price_per_km': 25,
                'price_per_hour': 1500,
                'capacity': 4,
                'rating': 4.9,
                'phone': '+91-9876543222',
                'email': 'info@luxurytransport.com',
                'available_cars': 8,
                'description': 'Ultra-luxury cars for premium experience',
            },
            {
                'company_name': 'Group Tours',
                'vehicle_type': 'van',
                'price_per_km': 20,
                'price_per_hour': 1200,
                'capacity': 12,
                'rating': 4.6,
                'phone': '+91-9876543223',
                'email': 'info@grouptours.com',
                'available_cars': 10,
                'description': 'Van service for group tours and family trips',
            },
        ]

        for cab_data in cabs_data:
            cab = Cab.objects.create(**cab_data)
            self.stdout.write(self.style.SUCCESS(f'Created cab: {cab.company_name}'))

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
