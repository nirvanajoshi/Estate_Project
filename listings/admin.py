from django.contrib import admin
from .models import Agent, PropertyType, Listing, Favorite, Inquiry, ListingImage

admin.site.register(Agent)
admin.site.register(PropertyType)
admin.site.register(Listing)
admin.site.register(Favorite)
admin.site.register(Inquiry)
admin.site.register(ListingImage)