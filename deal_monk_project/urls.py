"""deal_monk_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin
from dealmonkapp import views
from dealmonkapp import user_apis
from dealmonkapp import mobile_api
from dealmonkapp import android_api
from dealmonkapp import restaurant
from django.conf.urls.static import static
from deal_monk_project import settings
from dealmonkapp import menu


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home, name='home'),
    url(r'^register/', views.open_register, name='register'),	
    url(r'^dashboard/', views.open_dashboard, name='dashboard'),
    url(r'^bookings/', views.open_bookings, name='bookings'),
    url(r'^promotions/', views.open_promotions, name='promotions'),
    url(r'^myrestaurant/', views.open_myrestaurant, name='myrestaurant'),
    url(r'^addbooking/', views.open_addbooking, name='addbooking'),
    url(r'^change_booking_status/', restaurant.save_status, name='view_booking_details'),
    url(r'^booking-confirmation/', views.open_booking_confirm, name='bookingconfirm'),
    url(r'^old-bookings/', views.open_old_bookings, name='oldbookings'),
    url(r'^forgot-password/', views.open_forgot_password, name='forgotpassword'),
    url(r'^admin-register/', views.admin_register, name='admin_login'),
    url(r'^adlogin/', views.admin_login, name='admin_login'),
    url(r'^sign-out-admin/', views.signOutAdmin, name='signOutAdmin'),
    url(r'^consumer_logout/', user_apis.consumer_logout, name='consumer_logout'),
    url(r'^my-restaurantform/', views.open_my_restaurantform, name='addbooking'),
    url(r'^disp-restaurant/', restaurant.view_restaurant_details, name='disp_restaurant'),
    url(r'^add-restaurant/', restaurant.add_restaurant_details, name='add_restaurant'),
    url(r'^update_restaurant_details/', restaurant.update_restaurant_details, name='add_restaurant'),
    url(r'^update_owner_details/', restaurant.update_owner_details, name='add_restaurant'),
    url(r'^open-restaurant-branch/', views.open_restaurant_branch, name='open_restaurant_branch'),
    url(r'^new-restaurant-branch/', restaurant.add_restaurant_branch, name='add_restaurant_branch'),
    url(r'^view-upcoming-guests/', restaurant.view_upcoming_guests, name='view-upcoming-guests_today'),
    url(r'^view-old-guests/', restaurant.view_old_guests, name='view-old-guests'),
    url(r'^old-bookings/', views.open_old_bookings, name='oldbookings'),
    url(r'^view_booking_details/', restaurant.view_booking_details, name='view_booking_details'),
    url(r'^load-upcoming-guests/', views.load_upcoming_guests, name='load-upcoming-guests'),
    url(r'^view-upcoming-guests-tom/', restaurant.view_upcoming_guests_tomorrow, name='view-upcoming-guests-tomorrow'),    
    url(r'^view-calendar-events/', restaurant.view_calendar_events, name='view-calendar-events'),    
    url(r'^map-state/', restaurant.map_state, name='map-state'),
    url(r'^get_branch_details/', restaurant.get_branch_details, name='get_branch_details'),
    url(r'^update_branch_details/', restaurant.update_branch_details, name='update_branch_details'),
    url(r'^insert_offer/', restaurant.insert_offer, name='insert_offer'),
    url(r'^delete_offer/', restaurant.delete_offer, name='delete_offer'),
    url(r'^add-offer-details/', restaurant.update_offer, name='update_offer'),
    url(r'^save-offer-details/', restaurant.save_offer_details, name='save_offer_details'),
    url(r'^get-offer-schedule-list/', restaurant.get_offer_schedule_list, name='get_offer_schedule_list'),
    url(r'^check-offer-schedule-existence/', restaurant.check_offer_schedule_existence, name='check_offer_schedule_existence'),
    url(r'^delete-offer-sechedule/', restaurant.delete_offer_sechedule, name='delete_offer_sechedule'),
    url(r'^open-change-password/', views.open_change_password, name='open_change_password'),
    url(r'^change-password/', views.change_password, name='change_password'),
    url(r'^send-password/', views.forgot_password, name='forgot_password'),    
    url(r'^edit-restaurant/', views.edit_my_restaurantform, name='edit_restaurant'),
    url(r'^edit-restaurant-branch/', views.edit_my_restaurant_branch, name='edit_restaurant_branch'),
    url(r'^upload-admin-image/', views.upload_admin_image, name='upload_admin_image'),
    url(r'^check-operations-hours/',restaurant.check_operations_hours,name='check_operations_hours'), 



#menu
    url(r'^restaurant_menu/', views.open_restaurant_menu, name='restaurant_menu'),
    url(r'^insert-restaurant-menu/', menu.insert_restaurant_menu, name='insert_restaurant_menu'),
    url(r'^add_menu_details/', menu.add_menu_details, name='add_menu_details'),
    url(r'^get_menu_details/', menu.get_menu_details, name='get_menu_details'),
    url(r'^update_menu_details/', menu.update_menu_details, name='update_menu_details'),
    url(r'^delete_menu_details/', menu.delete_menu_details, name='delete_menu_details'),

    

# ios apis url
    url(r'^consumer_login/', mobile_api.consumer_login, name='consumer_login'),
    url(r'^consumer_register/', mobile_api.consumer_register, name='consumer_register'),
    url(r'^consumer_register_facebook_gmail/', mobile_api.consumer_register_facebook_gmail, name='consumer_register_facebook_gmail'),
    url(r'^update_consumer_profile/', mobile_api.update_consumer_profile, name='update_consumer_profile'),
    url(r'^change_password/', mobile_api.change_password, name='change_password'),
    url(r'^forgot_password/', mobile_api.forgot_password, name='forgot_password'),
    url(r'^sms_alert_activation/', mobile_api.sms_alert_activation, name='sms_alert_activation'),
    url(r'^email_alert_activation/', mobile_api.email_alert_activation, name='email_alert_activation'),
    url(r'^restaurant_list/', mobile_api.restaurant_list, name='restaurant_list'),
    url(r'^consumer_feedback/', mobile_api.consumer_feedback, name='consumer_feedback'),
    url(r'^upcoming_deal/', mobile_api.upcoming_deal, name='upcoming_deal'),
    url(r'^searchRestaurantBranch/', mobile_api.searchRestaurantBranch, name='searchRestaurantBranch'),
    url(r'^restaurant_view_list/', mobile_api.restaurant_view_list, name='restaurant_view_list'),
    url(r'^book_restaurant/', mobile_api.book_restaurant, name='book_restaurant'),
    url(r'^booking_list/', mobile_api.booking_list, name='booking_list'),
    url(r'^checkin/', mobile_api.checkin, name='checkin'),
    url(r'^check_booking/', mobile_api.check_booking, name='check_booking'),
    url(r'^all_deal/', mobile_api.all_deal, name='all_deal'),

    url(r'^android_consumer_register_facebook_gmail/', mobile_api.android_consumer_register_facebook_gmail, name='android_consumer_register_facebook_gmail'),


#android api urls
    #url(r'^android_consumer_login/', android_api.android_consumer_login, name='android_consumer_login'),
    #url(r'^android_consumer_register/', android_api.android_consumer_register, name='android_consumer_register'),
    #url(r'^android_consumer_register_facebook_gmail/', android_api.android_consumer_register_facebook_gmail, name='android_consumer_register_facebook_gmail'),
    #url(r'^android_update_consumer_profile/', android_api.android_update_consumer_profile, name='android_update_consumer_profile'),
    #url(r'^android_change_password/', android_api.android_change_password, name='android_change_password'),
    #url(r'^android_forgot_password/', android_api.android_forgot_password, name='android_forgot_password'),
    #url(r'^android_sms_alert_activation/', android_api.android_sms_alert_activation, name='android_sms_alert_activation'),
    #url(r'^android_email_alert_activation/', android_api.android_email_alert_activation, name='android_email_alert_activation'),
    #url(r'^android_restaurant_list/', android_api.android_restaurant_list, name='android_restaurant_list'),
    #url(r'^android_consumer_feedback/', android_api.android_consumer_feedback, name='android_consumer_feedback'),
    #url(r'^android_my_deal/', android_api.android_my_deal, name='android_my_deal'),
    #url(r'^android_searchRestaurantBranch/', android_api.android_searchRestaurantBranch, name='android_searchRestaurantBranch'),
    #url(r'^android_restaurant_view_list/', android_api.android_restaurant_view_list, name='android_restaurant_view_list'),
    #url(r'^android_book_restaurant/', android_api.android_book_restaurant, name='book_restaurant'),
    #url(r'^android_checkin/', android_api.android_checkin, name='android_checkin'),
    #url(r'^android_check_booking/', android_api.android_check_booking, name='android_check_booking'),



#    url(r'^restaurant_offer_cancelation/', mobile_api.restaurant_offer_cancelation, name='restaurant_offer_cancelation')

)+ static( settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    
