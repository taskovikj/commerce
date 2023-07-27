from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create_listing/', views.create_listing, name='create_listing'),
    path('add_to_watchlist/<int:listing_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('remove_from_watchlist/<int:listing_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('listing_detail/<int:listing_id>/', views.listing_detail, name='listing_detail'),
    path("watchlist/", views.list_watchlist, name="list_watchlist"),
    path('my_listings/', views.my_listings, name='my_listings'),
    path('delete_listing/<int:listing_id>/', views.delete_listing, name='delete_listing'),
]
