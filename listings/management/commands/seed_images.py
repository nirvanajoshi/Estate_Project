from pathlib import Path
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from listings.models import Listing, ListingImage
from PIL import Image, ImageDraw, ImageFont
import io


class Command(BaseCommand):
    help = 'Generate placeholder images for all listings'

    def handle(self, *args, **options):
        listings = Listing.objects.all()
        listings_dir = Path('media/listings')
        listings_dir.mkdir(parents=True, exist_ok=True)

        colors = [
            ('#0F766E', '#0D5E57'),  # Teal
            ('#2563EB', '#1D4ED8'),  # Blue
            ('#7C3AED', '#6D28D9'),  # Purple
            ('#DC2626', '#B91C1C'),  # Red
            ('#D97706', '#B45309'),  # Amber
            ('#059669', '#047857'),  # Emerald
        ]

        for i, listing in enumerate(listings):
            color, dark = colors[i % len(colors)]
            img = Image.new('RGB', (800, 500), color)
            draw = ImageDraw.Draw(img)

            # Try to load a font, fall back to default
            try:
                font_large = ImageFont.truetype("arial.ttf", 48)
                font_small = ImageFont.truetype("arial.ttf", 28)
                font_price = ImageFont.truetype("arial.ttf", 36)
            except (IOError, OSError):
                try:
                    font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
                    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
                    font_price = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
                except (IOError, OSError):
                    font_large = ImageFont.load_default()
                    font_small = font_large
                    font_price = font_large

            # Draw a subtle pattern overlay
            for x in range(0, 800, 40):
                draw.line([(x, 0), (x + 200, 500)], fill=dark, width=1)
            for y in range(0, 500, 40):
                draw.line([(0, y), (800, y)], fill=dark, width=1)

            # Draw a white rounded rectangle for text
            draw.rectangle([(50, 150), (750, 400)], fill=(255, 255, 255, 220), outline=None)
            draw.rectangle([(50, 150), (750, 400)], fill=None, outline=(255, 255, 255), width=2)

            # Draw text
            price_text = f"${int(listing.price):,}"
            title_text = listing.title[:30]
            location_text = f"{listing.city}, {listing.state}"
            features_text = f"{listing.bedrooms} BD | {listing.bathrooms} BA | {listing.square_feet} SQFT"

            # Center and draw price
            bbox = draw.textbbox((0, 0), price_text, font=font_price)
            draw.text(((800 - (bbox[2] - bbox[0])) / 2, 170), price_text, fill='#0F172A', font=font_price)

            # Center and draw title
            bbox = draw.textbbox((0, 0), title_text, font=font_large)
            draw.text(((800 - (bbox[2] - bbox[0])) / 2, 225), title_text, fill='#1F2937', font=font_large)

            # Center and draw location
            bbox = draw.textbbox((0, 0), location_text, font=font_small)
            draw.text(((800 - (bbox[2] - bbox[0])) / 2, 285), location_text, fill='#6B7280', font=font_small)

            # Center and draw features
            bbox = draw.textbbox((0, 0), features_text, font=font_small)
            draw.text(((800 - (bbox[2] - bbox[0])) / 2, 330), features_text, fill='#6B7280', font=font_small)

            # Save to bytes
            buffer = io.BytesIO()
            img.save(buffer, format='PNG', optimize=True)
            buffer.seek(0)

            # Clean up old images for this listing
            ListingImage.objects.filter(listing=listing).delete()

            # Create the ListingImage with the file
            filename = f'listing_{listing.pk}_hero.png'
            listing_image = ListingImage(listing=listing)
            listing_image.image.save(filename, ContentFile(buffer.read()), save=True)

            self.stdout.write(self.style.SUCCESS(f'  Created image for: {listing.title}'))

        self.stdout.write(self.style.SUCCESS(f'Done! Generated images for {listings.count()} listings.'))
