from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from listings.models import Agent, PropertyType, Listing, Favorite, ListingImage


class Command(BaseCommand):
    help = 'Seed the database with Nepali real estate demo data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')

        # Create user
        user, created = User.objects.get_or_create(
            username='Damodar_Joshi',
            defaults={
                'email': 'damodar@example.com',
                'first_name': 'Damodar',
                'last_name': 'Joshi',
            }
        )
        if created:
            user.set_password('demo12345')
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Created user: {user.username}'))
        else:
            self.stdout.write(f'User {user.username} already exists')

        # Create agent user
        agent_user, created = User.objects.get_or_create(
            username='anita_sharma',
            defaults={
                'email': 'anita@homefind.com',
                'first_name': 'Anita',
                'last_name': 'Sharma',
            }
        )
        if created:
            agent_user.set_password('demo12345')
            agent_user.save()
            self.stdout.write(self.style.SUCCESS(f'Created agent user: {agent_user.username}'))
        else:
            self.stdout.write(f'Agent user {agent_user.username} already exists')

        # Create agent profile
        agent, created = Agent.objects.get_or_create(
            user=agent_user,
            defaults={
                'phone': '985-1234567',
                'bio': 'Nepal ma ghar khojdai? Ma tapailai sahayog garna yahaan chu! 10 years of real estate experience across Kathmandu Valley.',
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created agent profile: {agent.user.username}'))
        else:
            self.stdout.write(f'Agent profile for {agent.user.username} already exists')

        # Create property types
        types = ['House', 'Apartment', 'Condo', 'Townhouse', 'Villa', 'Studio']
        for name in types:
            pt, created = PropertyType.objects.get_or_create(name=name)
            if created:
                self.stdout.write(f'  Created property type: {name}')

        house = PropertyType.objects.get(name='House')
        condo = PropertyType.objects.get(name='Condo')
        apartment = PropertyType.objects.get(name='Apartment')
        villa = PropertyType.objects.get(name='Villa')

        # Clear old listings and images
        ListingImage.objects.all().delete()
        Listing.objects.all().delete()

        # Create Nepali listings with NPR prices
        listings_data = [
            {
                'title': 'Luxury Family Home in Chabhil',
                'description': 'Chabhil ko yo aadhunik ghar ma sundar open floor plan, quartz countertops, hardwood floors, ra lush garden cha. Pariwar ko lagi ekdam perfect. Shant chhima ma basna paune, top-rated schools pani najikai.',
                'price': 55000000,
                'bedrooms': 4,
                'bathrooms': 3,
                'square_feet': 2800,
                'address': 'Chabhil, Kathmandu',
                'city': 'Kathmandu',
                'state': 'Bagmati',
                'zip_code': '44600',
                'property_type': house,
            },
            {
                'title': 'Downtown Luxury Condo, Durbar Marg',
                'description': 'Durbar Marg ko yo luxury condole panoramic city views dincha. Floor-to-ceiling windows, stainless steel appliances, spa-like bathroom. Gym, pool, ra concierge service pani cha. Restaurants ra shopping lai walkable distance ma.',
                'price': 32000000,
                'bedrooms': 2,
                'bathrooms': 2,
                'square_feet': 1200,
                'address': 'Durbar Marg, Kathmandu',
                'city': 'Kathmandu',
                'state': 'Bagmati',
                'zip_code': '44600',
                'property_type': condo,
            },
            {
                'title': 'Traditional Bungalow in Patan Durbar Square Area',
                'description': 'Patan ko historic area ma restore gariyeko traditional bungalow. Original woodwork, crown molding, updated kitchen ra bathrooms. Spacious front porch ra private backyard garden cha. Local cafes ra handicraft shops najikai.',
                'price': 25000000,
                'bedrooms': 3,
                'bathrooms': 2,
                'square_feet': 1800,
                'address': 'Mangal Bazar, Lalitpur',
                'city': 'Lalitpur',
                'state': 'Bagmati',
                'zip_code': '44700',
                'property_type': house,
            },
            {
                'title': 'Cozy Apartment in Lakeside, Pokhara',
                'description': 'Pokhara ko Lakeside ma raheko yo apartment le Fewa Lake ko breathtaking view dincha. Open kitchen, in-unit laundry, private balcony. Rooftop terrace, fitness center, ra parking cha. Santi ra nature maya garne manche ko lagi perfect.',
                'price': 15000000,
                'bedrooms': 2,
                'bathrooms': 1,
                'square_feet': 850,
                'address': 'Lakeside, Pokhara',
                'city': 'Pokhara',
                'state': 'Gandaki',
                'zip_code': '33700',
                'property_type': apartment,
            },
            {
                'title': 'Modern Villa in Budhanilkantha',
                'description': 'Budhanilkantha ko hillside ma raheko yo modern villa le Kathmandu Valley ko breathtaking view dincha. Private pool, outdoor kitchen, terraced gardens, wine cellar, ra grand master suite. Luxury living ko lagi sabai kura milera baseko.',
                'price': 95000000,
                'bedrooms': 5,
                'bathrooms': 4,
                'square_feet': 4200,
                'address': 'Budhanilkantha, Kathmandu',
                'city': 'Kathmandu',
                'state': 'Bagmati',
                'zip_code': '44602',
                'property_type': villa,
            },
            {
                'title': 'Affordable Home in Bhaktapur',
                'description': 'Bhaktapur ma raheko yo affordable ghar first-time buyers ra investment ko lagi perfect cha. Freshly painted, new flooring, modern fixtures, ra energy-efficient appliances. Low-maintenance yard, attached garage. Move-in ready!',
                'price': 8500000,
                'bedrooms': 3,
                'bathrooms': 1,
                'square_feet': 1300,
                'address': 'Durbar Square Area, Bhaktapur',
                'city': 'Bhaktapur',
                'state': 'Bagmati',
                'zip_code': '44800',
                'property_type': house,
            },
        ]

        for data in listings_data:
            pt = data.pop('property_type')
            listing = Listing.objects.create(
                **data,
                agent=agent,
                property_type=pt
            )
            self.stdout.write(f'  Created listing: {listing.title}')

        self.stdout.write(self.style.SUCCESS('Seeding complete!'))
