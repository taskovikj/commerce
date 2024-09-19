from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import IntegrityError
from django.db.models import Count, Max, Sum
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
import json
from decimal import Decimal, InvalidOperation
from .models import Listing, Watchlist, Comment, BiddingLogg, User, Category

def frontend_view(request):
    csrf_token = get_token(request)
    return render(request, 'index.html', {'csrf_token': csrf_token})

def index(request):
    query = request.GET.get('query')
    listings = Listing.objects.filter(closed=False).annotate(bids_count=Count('biddinglogg')).prefetch_related('categories')
    if query:
        listings = listings.filter(title__icontains=query)

    paginator = Paginator(listings, 9)
    page = request.GET.get('page')
    try:
        listings_page = paginator.page(page)
    except PageNotAnInteger:
        listings_page = paginator.page(1)
    except EmptyPage:
        listings_page = paginator.page(paginator.num_pages)

    data = {
        'listings': list(listings_page.object_list.values(
            'id', 'title', 'description', 'current_price', 'bids_count', 'created_at', 'image_url',
            'categories__id', 'categories__name'
        )),
        'total_pages': paginator.num_pages
    }
    return JsonResponse(data)

def login_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            return JsonResponse({'status': 'error', 'message': 'Both username and password are required.'}, status=400)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'success', 'user': user.username})
        return JsonResponse({'status': 'error', 'message': 'Invalid username or password.'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def user_status(request):
    if request.user.is_authenticated:
        return JsonResponse({'isAuthenticated': True, 'username': request.user.username})
    return JsonResponse({'isAuthenticated': False, 'username': ''})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'status': 'success', 'message': 'Logged out successfully'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            confirmation = data.get('confirmation')

            if not username or not email or not password or not confirmation:
                return JsonResponse({'status': 'error', 'message': 'All fields are required'}, status=400)
            if password != confirmation:
                return JsonResponse({'status': 'error', 'message': 'Passwords must match'}, status=400)

            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                login(request, user)
                return JsonResponse({'status': 'success', 'user': user.username})
            except IntegrityError:
                return JsonResponse({'status': 'error', 'message': 'Username already taken'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'Internal Server Error'}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        return redirect('/login')
    return _wrapped_view

@csrf_exempt
def create_listing(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title')
            description = data.get('description', '')
            starting_price = data.get('starting_price')
            image_url = data.get('image_url', '')
            category_id = data.get('category')

            if not title or not starting_price:
                return JsonResponse({'status': 'error', 'message': 'Title and Starting Price are required'}, status=400)

            listing = Listing.objects.create(
                title=title,
                description=description,
                starting_price=starting_price,
                current_price=starting_price,
                image_url=image_url,
                creator=request.user
            )

            if category_id:
                category = get_object_or_404(Category, id=category_id)
                listing.categories.add(category)

            return JsonResponse({'status': 'success', 'listing_id': listing.id})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def add_to_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user_watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    user_watchlist.listings.add(listing)
    return JsonResponse({'status': 'success', 'message': 'Listing added to watchlist'})

def remove_from_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user_watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    user_watchlist.listings.remove(listing)
    return JsonResponse({'status': 'success', 'message': 'Listing removed from watchlist'})

def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.method == 'GET':
        is_owner = request.user == listing.creator
        is_authenticated = request.user.is_authenticated
        comments = list(listing.comments.values('id', 'text', 'user__username', 'created_at'))
        created_at = listing.created_at.strftime('%Y-%m-%d %H:%M:%S')
        category_names = ', '.join([category.name for category in listing.categories.all()]) if listing.categories.exists() else "N/A"

        data = {
            'listing': {
                'id': listing.id,
                'title': listing.title,
                'description': listing.description,
                'starting_price': str(listing.starting_price),
                'current_price': str(listing.current_price),
                'image_url': listing.image_url,
                'highest_bidder': listing.highest_bidder.username if listing.highest_bidder else None,
                'creator': listing.creator.username,
                'category_name': category_names,
                'created_at': created_at,
                'closed': listing.closed
            },
            'comments': comments,
            'isAuthenticated': is_authenticated,
            'isOwner': is_owner,
        }
        return JsonResponse(data)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)

        if 'text' in data:
            text = data.get('text')
            if not text or text.strip() == '':
                return JsonResponse({'status': 'error', 'message': 'Comment text cannot be empty.'}, status=400)

            Comment.objects.create(listing=listing, user=request.user, text=text)
            return JsonResponse({'status': 'success', 'message': 'Comment added successfully'})

        elif 'bid_amount' in data:
            bid_amount_str = data.get('bid_amount')
            if not bid_amount_str:
                return JsonResponse({'status': 'error', 'message': 'Bid amount is required.'}, status=400)

            try:
                bid_amount = Decimal(bid_amount_str)
            except InvalidOperation:
                return JsonResponse({'status': 'error', 'message': 'Invalid bid amount.'}, status=400)

            if bid_amount > listing.current_price:
                listing.current_price = bid_amount
                listing.highest_bidder = request.user
                listing.save()

                BiddingLogg.objects.create(
                    user=request.user,
                    listing1=listing,
                    bid_amount=bid_amount,
                    timestamp=timezone.now()
                )

                return JsonResponse({
                    'status': 'success',
                    'current_price': str(listing.current_price),
                    'message': 'Bid placed successfully'
                })
            return JsonResponse({'status': 'error', 'message': 'Bid must be higher than the current price.'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def close_auction(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.user == listing.creator:
        listing.closed = True
        listing.save()
        return JsonResponse({'status': 'success', 'message': 'Auction closed successfully'})
    return JsonResponse({'status': 'error', 'message': 'Unauthorized access'}, status=403)

def my_listings(request):
    user_listings = Listing.objects.filter(creator=request.user)
    listings_data = list(user_listings.values('id', 'title', 'description', 'current_price', 'closed'))
    return JsonResponse({'listings': listings_data})

def user_bids(request):
    user = request.user
    bid_listings = Listing.objects.filter(biddinglogg__user=user).annotate(
        highest_bid=Max('biddinglogg__bid_amount')
    ).distinct()

    bid_data = []
    for listing in bid_listings:
        if listing.closed and listing.highest_bidder == user:
            status = "Won"
        elif listing.closed:
            status = "Lost"
        elif listing.highest_bidder == user:
            status = "Winning"
        else:
            status = "Outbid"

        bid_data.append({
            'id': listing.id,
            'title': listing.title,
            'current_price': listing.current_price,
            'status': status,
            'image_url': listing.image_url,
            'closed': listing.closed,
        })

    return JsonResponse({'bid_listings': bid_data})

def list_watchlist(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'User not authenticated'}, status=403)

    user_watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    watchlist_listings = list(user_watchlist.listings.values('id', 'title', 'description', 'current_price', 'image_url'))

    return JsonResponse({'status': 'success', 'watchlist': watchlist_listings})

def delete_listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if listing.creator == request.user:
        listing.delete()
        return JsonResponse({'status': 'success', 'message': 'Listing deleted successfully'})
    return JsonResponse({'status': 'error', 'message': 'Unauthorized access'}, status=403)

def create_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category = Category.objects.create(name=name)
        return JsonResponse({'status': 'success', 'category_id': category.id})

    categories = list(Category.objects.values())
    return JsonResponse({'categories': categories})

def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    category.delete()
    return JsonResponse({'status': 'success', 'message': 'Category deleted successfully'})

def add_comment_to_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.method == 'POST':
        text = request.POST.get('text')
        if text and text.strip():
            comment = Comment.objects.create(listing=listing, user=request.user, text=text)
            comment.save()
            return JsonResponse({'status': 'success', 'comment': text})
        return JsonResponse({'status': 'error', 'message': 'Comment text cannot be empty.'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

def list_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    listings = Listing.objects.filter(categories__id=category_id).values(
        'id', 'title', 'description', 'current_price', 'image_url', 'creator__username', 'created_at', 'bids_count'
    )
    return JsonResponse({'category': {'id': category.id, 'name': category.name}, 'listings': list(listings)})

def list_categories(request):
    categories = list(Category.objects.values('id', 'name'))
    return JsonResponse({'categories': categories})

@require_http_methods(["GET", "PUT"])
def my_profile(request):
    user = request.user
    if request.method == 'GET':
        won_auctions = Listing.objects.filter(highest_bidder=user, closed=True)
        total_money_spent = won_auctions.aggregate(total_spent=Sum('current_price'))['total_spent'] or 0
        total_won_auctions = won_auctions.count()

        sold_listings = Listing.objects.filter(creator=user, closed=True)
        total_money_earned = sold_listings.aggregate(total_earned=Sum('current_price'))['total_earned'] or 0
        total_sold_items = sold_listings.count()

        return JsonResponse({
            'user': {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            },
            'total_won_auctions': total_won_auctions,
            'total_money_spent': total_money_spent,
            'total_sold_items': total_sold_items,
            'total_money_earned': total_money_earned
        })

    elif request.method == 'PUT':
        data = json.loads(request.body)
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.save()

        return JsonResponse({'status': 'success', 'message': 'Profile updated successfully'})

@require_http_methods(["PUT"])
def update_password(request):
    user = request.user
    data = json.loads(request.body)
    new_password = data.get('password')
    if not new_password:
        return JsonResponse({'status': 'error', 'message': 'Password is required'}, status=400)

    user.set_password(new_password)
    user.save()
    return JsonResponse({'status': 'success', 'message': 'Password updated successfully'})

@require_http_methods(["PUT", "DELETE"])
def comment_edit_or_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.user:
        return HttpResponseForbidden('You are not allowed to modify this comment.')

    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            text = data.get('text')
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

        if text and text.strip():
            comment.text = text
            comment.save()
            return JsonResponse({'status': 'success', 'message': 'Comment updated successfully'})
        return JsonResponse({'status': 'error', 'message': 'Comment text cannot be empty'}, status=400)

    elif request.method == 'DELETE':
        comment.delete()
        return JsonResponse({'status': 'success', 'message': 'Comment deleted successfully'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
@require_http_methods(["PUT"])
def edit_listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.user != listing.creator:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized access'}, status=403)

    try:
        data = json.loads(request.body)
        listing.title = data.get('title', listing.title)
        listing.description = data.get('description', listing.description)
        listing.starting_price = data.get('starting_price', listing.starting_price)
        listing.image_url = data.get('image_url', listing.image_url)

        category_id = data.get('category')
        if category_id:
            category = get_object_or_404(Category, pk=category_id)
            listing.categories.clear()
            listing.categories.add(category)

        listing.save()
        return JsonResponse({'status': 'success', 'message': 'Listing updated successfully'})
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
