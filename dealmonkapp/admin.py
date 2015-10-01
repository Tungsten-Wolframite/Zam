from django.contrib import admin
from dealmonkapp.models import *

admin.site.register(RestaurantAdmin);
admin.site.register(Consumer);
admin.site.register(Restaurant);
admin.site.register(RestaurantBranch);
admin.site.register(RestaurantRating);
admin.site.register(RestaurantOffer);
admin.site.register(RestaurantBooking);
admin.site.register(ConsumerPaymentCredentials);
admin.site.register(Invoice);
admin.site.register(AreaFactTable);
admin.site.register(Offer_map);
admin.site.register(CuisineFactTable);
admin.site.register(CuisineRestaurentMap);
admin.site.register(CuisineRestaurentBranchMap);
admin.site.register(CategoriesFactTable);
admin.site.register(MenuItemTable);