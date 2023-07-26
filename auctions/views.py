from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Listing

from .models import User, Category


def index(request):
    listings = Listing.objects.all()
    print(listings)
    return render(request, "auctions/index.html", {'listings': listings})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('/login')
    return _wrapped_view

@login_required
def create_listing(request):
    categories = Category.objects.all()
    print(categories)
    if request.method == 'POST':

        title = request.POST.get('title')
        description = request.POST.get('description')
        starting_price = request.POST.get('starting_price')
        image_url = request.POST.get('image_url')
        category_id = request.POST.get('category')

        listing = Listing(
            title=title,
            description=description,
            starting_price=starting_price,
            current_price=starting_price,
            image_url=image_url,
        )
        listing.save()

        if category_id:
            listing.categories.add(category_id)

        return redirect('/')

    return render(request, 'create_listing.html', {'categories': categories})
