from django.urls import path, re_path, include
from . import views
from django.contrib import admin

urlpatterns = [

    # Admin route
    path('admin/', admin.site.urls),

    # API routes
    path('api/listings/', views.index, name='listings'),
    path('api/login/', views.login_view, name='login'),
    path('api/user-status/', views.user_status, name='user_status'),
    path('api/logout/', views.logout_view, name='logout'),
    path('api/register/', views.register, name='register'),
    path('api/create_listing/', views.create_listing, name='create_listing'),
    path('api/add_to_watchlist/<int:listing_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('api/remove_from_watchlist/<int:listing_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('api/listing_detail/<int:listing_id>/', views.listing_detail, name='listing_detail'),
    path('api/watchlist/', views.list_watchlist, name='list_watchlist'),
    path('api/my_listings/', views.my_listings, name='my_listings'),
    path('api/delete_listing/<int:listing_id>/', views.delete_listing, name='delete_listing'),
    path('api/create_category/', views.create_category, name='create_category'),
    path('api/delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('api/add-comment/<int:listing_id>/', views.add_comment_to_listing, name='add_comment_to_listing'),
    path('api/close_auction/<int:listing_id>/', views.close_auction, name='close_auction'),
    path('api/comment/<int:comment_id>/', views.comment_edit_or_delete, name='comment_edit_or_delete'),
    path('api/edit_listing/<int:listing_id>/', views.edit_listing, name='edit_listing'),
    path('api/category_listings/<int:category_id>/', views.list_category, name='category_listings'),
    path('api/categories/', views.list_categories, name='list_categories'),
    path('api/my_profile/', views.my_profile, name='my_profile'),
    path('api/user_bids/', views.user_bids, name='user_bids'),
    path('api/update_password/', views.update_password, name='update_password'),




    re_path(r'^.*$', views.frontend_view),
]
