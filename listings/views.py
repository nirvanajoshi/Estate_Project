from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Listing, ListingImage, Inquiry, Agent, PropertyType, Favorite
from .forms import ListingForm, ListingImageForm, InquiryForm


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('listing_list')
    else:
        form = UserCreationForm()
    return render(request, 'listings/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('listing_list')
    else:
        form = AuthenticationForm()
    return render(request, 'listings/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('listing_list')


def listing_list(request):
    listings = Listing.objects.all()

    location = request.GET.get('location')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    bedrooms = request.GET.get('bedrooms')

    if location:
        listings = listings.filter(city__icontains=location)
    if min_price:
        listings = listings.filter(price__gte=min_price)
    if max_price:
        listings = listings.filter(price__lte=max_price)
    if bedrooms:
        listings = listings.filter(bedrooms=bedrooms)

    return render(request, 'listings/listing_list.html', {'listings': listings})

@login_required
def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    images = listing.listingimage_set.all()

    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.listing = listing
            inquiry.user = request.user
            inquiry.save()
            messages.success(request, 'Your inquiry has been sent.')
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = InquiryForm()

    return render(request, 'listings/listing_detail.html', {
        'listing': listing,
        'images': images,
        'form': form,
    })


@login_required
def create_listing(request):
    agent = get_object_or_404(Agent, user=request.user)
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.agent = agent
            listing.save()
            messages.success(request, 'Listing created successfully.')
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = ListingForm()
    return render(request, 'listings/create_listing.html', {'form': form})


@login_required
def add_listing_image(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.method == 'POST':
        form = ListingImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.listing = listing
            image.save()
            messages.success(request, 'Image added successfully.')
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = ListingImageForm()
    return render(request, 'listings/add_listing_image.html', {'form': form, 'listing': listing})


@login_required
def toggle_favorite(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    favorite = Favorite.objects.filter(user=request.user, listing=listing)
    if favorite.exists():
        favorite.delete()
        messages.success(request, 'Removed from favorites.')
    else:
        Favorite.objects.create(user=request.user, listing=listing)
        messages.success(request, 'Added to favorites.')
    return redirect('listing_detail', pk=listing.pk)


@login_required
def my_favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'listings/my_favorites.html', {'favorites': favorites})