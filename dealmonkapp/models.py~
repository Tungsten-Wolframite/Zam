from django.db import models
from django.contrib.auth.models import User
from django.template import RequestContext
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_control
from django.contrib import auth
from dealmonkapp.models import *

from constants import AppUserConstants, ExceptionLabel
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf

# importing mysqldb and system packages
import MySQLdb, sys
from django.db.models import Q
from django.db.models import F
from django.db import transaction

import csv
import json
#importing exceptions
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError

from datetime import datetime
import uuid
from django.db.models.signals import class_prepared


#for image
CONSUMER_IMAGES_PATH ='images/'
RESTAURANT_IMAGES_PATH = 'restaurant/'
ADMIN_IMAGES_PATH ='Admin_images/'
 

SIGNUP_VIA = (
    ('FB','FB'),
    ('GP','GP'),
    ('TW','TW'),
    ('APP','APP'),
)

RATING = (
    ('0.5','0.5'),
    ('1','1'),
    ('1.5','1.5'),
    ('2','2'),
    ('2.5','2.5'),
    ('3','3'),
    ('3.5','3.5'),
    ('4','4'),
    ('4.5','4.5'),
    ('5','5'),
)

BOOKING_STATUS = (
    ('Requested','Requested'),
    ('Waiting','Waiting'),
    ('Confirmed','Confirmed'),
    ('Completed','Completed'),
    ('No Show','No Show'),
)

MENU_TYPE = (
    ('VEG','VEG'),
    ('GLUTEN FREE','GLUTEN FREE'),
    ('NON-VEG','NON-VEG'),
)

class RestaurantAdmin(User):
    restaurant_admin_id= models.AutoField(primary_key=True, editable=False)        
    restaurant_admin_first_name=models.CharField(max_length=45,default=None)
    restaurant_admin_last_name=models.CharField(max_length=45,default=None)
    restaurant_admin_email=models.CharField(max_length=45,default=None)
    restaurant_admin_contactno=models.CharField(max_length=45,default=None)    
    is_restaurant_admin_email_alert_on=models.CharField(max_length=1,default=1)
    is_restaurant_admin_sms_alert_on=models.CharField(max_length=1,default=1)
    restaurant_admin_status=models.CharField(max_length=1,default=1)    
    restaurant_admin_has_restaurant=models.IntegerField(default=0)
    restaurant_admin_profile_pic= models.ImageField("Image",upload_to=ADMIN_IMAGES_PATH,max_length=500, default=None)
    restaurant_admin_create_date=models.DateTimeField(default=datetime.now,blank=True,editable=False)
    restaurant_admin_create_by=models.CharField(max_length=45,default=None,blank=True,null=True)
    restaurant_admin_update_date=models.DateTimeField(default=datetime.now,blank=True)
    restaurant_admin_update_by=models.CharField(max_length=45,default=None,blank=True,null=True)
            
    def __unicode__(self):
        return unicode(self.restaurant_admin_id)
    
    
class Consumer(User):
    consumer_id= models.AutoField(primary_key=True)
    consumer_email=models.CharField(max_length=45)
    consumer_contactno = models.CharField(max_length=45,null=True,blank=True)
    consumer_first_name = models.CharField(max_length=45)
    consumer_last_name = models.CharField(max_length=45)
    sign_up_via = models.CharField(max_length=10,null=True,blank=True)
    sign_up_source = models.CharField(max_length=10,null=True,blank=True)
    apns_token = models.CharField(max_length=10,null=True,blank=True)
    consumer_image = models.ImageField("Image",upload_to=CONSUMER_IMAGES_PATH,max_length=255, default=None)    
    consumer_city= models.CharField(max_length=45,null=True,blank=True)
    consumer_state= models.CharField(max_length=45,null=True,blank=True)
    consumer_country= models.CharField(max_length=45,null=True,blank=True)
    consumer_gender= models.CharField(max_length=1,null=True,blank=True)
    consumer_age = models.IntegerField(null=True,blank=True)
    consumer_location = models.CharField(max_length=45,null=True,blank=True)
    consumer_feedback = models.CharField(max_length=200,null=True,blank=True)
    consumer_brownypoint = models.IntegerField(null=True,blank=True)
    is_consumer_email_alert = models.CharField(max_length=1,null=True,blank=True)
    is_consumer_sms_alert = models.CharField(max_length=1,null=True,blank=True)
    consumer_create_by = models.CharField(max_length=45,null=True,blank=True)
    consumer_create_date = models.DateTimeField(null=True,blank=True)
    consumer_update_by=models.CharField(max_length=45,null=True,blank= True)
    consumer_update_date= models.DateTimeField(null=True,blank=True)
    consumer_status = models.CharField(max_length=1,null=True,blank=True)
    
    #def save(self, force_insert=False, force_update=False):
    #    self.code = 'DMC%08d' % self.consumer_id
    #    super(consumer, self).save(force_insert, force_update)
        
    def __unicode__(self):
        return unicode('DMC%08d'%self.consumer_id)    
    
    
class ConsumerPaymentCredentials(models.Model):
    consumer_payment_id = models.AutoField(primary_key=True)
    consumer_id = models.ForeignKey(Consumer)
    consumer_payment_bankname= models.CharField(max_length=45)
    consumer_payment_cardno = models.CharField(max_length=45)
    consumer_payment_cardtype=models.CharField(max_length=45)
    consumer_payment_cvv = models.CharField(max_length=45)
    consumer_payment_expdate = models.DateField()
    consumer_payment_datetime = models.DateTimeField('payment datetime')
    consumer_payment_create_by= models.CharField(max_length=45)
    consumer_payment_create_date= models.DateTimeField('payment create')
    consumer_payment_update_date= models.DateTimeField('payment update')
    consumer_payment_update_by= models.CharField(max_length=45)
    consumer_payment_status= models.CharField(max_length=1)
        
    def __unicode__(self):
        return unicode('DMP%08d'%self.consumer_payment_id) 
    

class Restaurant(models.Model):
    restaurant_id=models.AutoField(primary_key=True, editable=False)    
    restaurant_admin_id=models.ForeignKey(RestaurantAdmin,blank=True)        
    restaurant_name=models.CharField(max_length=45)
    restaurant_owner_firstname=models.CharField(max_length=45,blank=True,null=True)
    restaurant_owner_lastname=models.CharField(max_length=45,blank=True,null=True)
    restaurant_owner_contact=models.CharField(max_length=45,blank=True,null=True)
    restaurant_owner_email=models.CharField(max_length=45,blank=True,null=True)
    restaurant_image=models.ImageField(upload_to=RESTAURANT_IMAGES_PATH,default='default_icon_restaurant.png')    
    restaurant_contactno=models.CharField(max_length=45)
    restaurant_addr1=models.CharField(max_length=45)
    restaurant_addr2=models.CharField(max_length=45)
    restaurant_area=models.CharField(max_length=45)
    restaurant_city=models.CharField(max_length=45)
    restaurant_state=models.CharField(max_length=45)
    restaurant_zipcode=models.CharField(max_length=45)
    restaurant_description=models.CharField(max_length=45)
    restaurant_opentime_day=models.TimeField(blank=True,null=True)
    restaurant_closetime_day=models.TimeField(blank=True,null=True)
    restaurant_opentime_eve=models.TimeField(blank=True,null=True)
    restaurant_closetime_eve=models.TimeField(blank=True,null=True)    
    restaurant_status=models.CharField(max_length=1,default=1)
    restaurant_has_branch=models.IntegerField(default=0,blank=True)    
    restaurant_lat=models.CharField(max_length=45,default=None,null=True,blank=True)
    restaurant_lon=models.CharField(max_length=45,default=None,null=True,blank=True)
    restaurant_create_date=models.DateField(null=True,blank=True)
    restaurant_create_by=models.CharField(max_length=45)
    restaurant_update_date=models.DateField(default=datetime.now,null=True,blank=True)
    restaurant_update_by=models.CharField(max_length=45)
    
    def __unicode__(self):
        return unicode(self.restaurant_id)    
        
    def get_restaurant_info(self):
        return {'restaurant_id' : self.restaurant_id, 'restaurant_name': self.restaurant_name,
         'restaurant_contactno': self.restaurant_contactno, 'restaurant_image': self.restaurant_image.url, 
         'restaurant_addr1': self.restaurant_addr1,'restaurant_city': self.restaurant_city, 
         'restaurant_opentime_day': self.check_val(self.restaurant_opentime_day), 'restaurant_closetime_day': self.check_val(self.restaurant_closetime_day), 
         'restaurant_opentime_eve': self.check_val(self.restaurant_opentime_eve), 'restaurant_closetime_eve': self.check_val(self.restaurant_closetime_eve),
         'restaurant_owner_firstname' : self.restaurant_owner_firstname,'restaurant_owner_lastname' : self.restaurant_owner_lastname,
         'restaurant_owner_email' : self.restaurant_owner_email,'restaurant_owner_contact' : self.restaurant_owner_contact,
         'restaurant_zipcode':self.restaurant_zipcode,'restaurant_state':self.restaurant_state,
         'restaurant_area':self.restaurant_area,'restaurant_addr2':self.restaurant_addr2,
        'restaurant_description':self.restaurant_description,'restaurant_has_branch':self.restaurant_has_branch,
        'restaurant_lat':self.restaurant_lat,'restaurant_lon':self.restaurant_lon}
        
    def get_rest_info(self):
        print self.restaurant_image.url
        return {'restaurant_id' : self.restaurant_id, 'restaurant_name': self.restaurant_name,
         'restaurant_contactno': self.restaurant_contactno, 'restaurant_image': self.restaurant_image.url, 
         'restaurant_addr1': self.restaurant_addr1,'restaurant_city': self.restaurant_city,
         'restaurant_opentime_day': self.check_vals(self.restaurant_opentime_day), 'restaurant_closetime_day': self.check_vals(self.restaurant_closetime_day), 
         'restaurant_opentime_eve': self.check_vals(self.restaurant_opentime_eve), 'restaurant_closetime_eve': self.check_vals(self.restaurant_closetime_eve),
         'restaurant_owner_email' : self.restaurant_owner_email,'restaurant_owner_contact' : self.restaurant_owner_contact,
         'restaurant_zipcode':self.restaurant_zipcode,'restaurant_state':self.restaurant_state,
         'restaurant_area':self.restaurant_area,'restaurant_addr2':self.restaurant_addr2,
        'restaurant_description':self.restaurant_description,'restaurant_has_branch':self.restaurant_has_branch,
        'restaurant_lat':self.restaurant_lat,'restaurant_lon':self.restaurant_lon}    
    
    def check_val(self,date_val):
        if(date_val):
            return date_val.strftime("%H:%M")
        else:
            return '00:00'
        
    def check_vals(self,date_val):
        if(date_val):
            return date_val.strftime('%I:%M %p')
        else:
            return '00:00'
    
    
class RestaurantBranch(models.Model):
    restaurant_branch_id=models.AutoField(primary_key=True,default=None,blank=True)
    restaurant_id=models.ForeignKey(Restaurant,blank=True)
    restaurant_admin_id=models.ForeignKey(RestaurantAdmin,default=None)
    restaurant_branch_name=models.CharField(max_length=45,default=None,blank=True)
    #restaurant_branch_image=models.ImageField(upload_to=RESTAURANT_IMAGES_PATH,default='default_icon_restaurant.png')
    restaurant_branch_contact=models.CharField(max_length=45,default=None,blank=True)
    restaurant_branch_address1=models.CharField(max_length=45,default=None,blank=True)
    restaurant_branch_address2=models.CharField(max_length=45,default=None,blank=True)
    restaurant_branch_area=models.CharField(max_length=45,default=None,blank=True)
    restaurant_branch_city=models.CharField(max_length=45,default=None,blank=True)
    restaurant_branch_state=models.CharField(max_length=45,default=None,blank=True)
    restaurant_branch_pincode=models.CharField(max_length=6,default=None,blank=True)
    restaurant_branch_lat=models.CharField(max_length=45,default=None,blank=True)
    restaurant_branch_lon=models.CharField(max_length=45,default=None,blank=True)
    restaurant_branch_opentime_day=models.TimeField(default=None,blank=True,null=True)
    restaurant_branch_closetime_day=models.TimeField(default=None,blank=True,null=True)
    restaurant_branch_opentime_eve=models.TimeField(default=None,blank=True,null=True)
    restaurant_branch_closetime_eve=models.TimeField(default=None,blank=True,null=True)  
    #restaurant_branch_create_date=models.DateTimeField(default=datetime.now(), blank=True)
    restaurant_branch_create_date=models.DateTimeField(default=datetime.now,null=True,blank=True)
    #restaurant_branch_create_by=models.CharField(max_length=45,default=request.session['login_user'])
    restaurant_branch_create_by=models.CharField(max_length=45,default=None,blank=True)
    #restaurant_branch_update_date=models.DateTimeField(default=datetime.now(), blank=True)
    restaurant_branch_update_date=models.DateTimeField(default=datetime.now,null=True,blank=True)
    #restaurant_branch_update_by=models.CharField(max_length=45,default=request.session['login_user'])
    restaurant_branch_update_by=models.CharField(max_length=45,default=None,blank=True)
    restaurant_branch_status=models.CharField(max_length=1,default=1)	

##    def save(self, *args, **kwargs):
##        ''' On save, update timestamps '''
##        if not self.restaurant_branch_id:
##            self.restaurant_branch_create_date = datetime.datetime.today()
##        self.restaurant_branch_update_date = datetime.datetime.today()
##        return super(RestaurantBranch, self).save(*args, **kwargs)
    
    def unicode__(self):
        return unicode(self.restaurant_branch_id)
    
    def get_restaurantbranch_info(self):
        return {'restaurant_branch_id' : self.restaurant_branch_id, 'restaurant_branch_name': self.restaurant_branch_name,
         'restaurant_branch_contactno': self.restaurant_branch_contact, 
         'restaurant_branch_addr1': self.restaurant_branch_address1,'restaurant_branch_city': self.restaurant_branch_city, 
         'restaurant_branch_opentime_day': self.check_val(self.restaurant_branch_opentime_day), 'restaurant_branch_closetime_day': self.check_val(self.restaurant_branch_closetime_day), 
         'restaurant_branch_opentime_eve': self.check_val(self.restaurant_branch_opentime_eve), 'restaurant_branch_closetime_eve': self.check_val(self.restaurant_branch_closetime_eve),
         'restaurant_branch_zipcode':self.restaurant_branch_pincode,'restaurant_branch_state':self.restaurant_branch_state,
         'restaurant_branch_area':self.restaurant_branch_area,'restaurant_branch_addr2':self.restaurant_branch_address2,
        'restaurant_branch_lat':self.restaurant_branch_lat,'restaurant_branch_lon':self.restaurant_branch_lon}
        
    def get_rest_branch_info(self):
        return {'restaurant_branch_id' : self.restaurant_branch_id, 'restaurant_branch_name': self.restaurant_branch_name,
         'restaurant_branch_contactno': self.restaurant_branch_contact, 
         'restaurant_branch_addr1': self.restaurant_branch_address1,'restaurant_branch_city': self.restaurant_branch_city, 
         'restaurant_branch_opentime_day': self.check_vals(self.restaurant_branch_opentime_day), 'restaurant_branch_closetime_day': self.check_vals(self.restaurant_branch_closetime_day), 
         'restaurant_branch_opentime_eve': self.check_vals(self.restaurant_branch_opentime_eve), 'restaurant_branch_closetime_eve': self.check_vals(self.restaurant_branch_closetime_eve),
         'restaurant_branch_zipcode':self.restaurant_branch_pincode,'restaurant_branch_state':self.restaurant_branch_state,
         'restaurant_branch_area':self.restaurant_branch_area,'restaurant_branch_addr2':self.restaurant_branch_address2,
        'restaurant_branch_lat':self.restaurant_branch_lat,'restaurant_branch_lon':self.restaurant_branch_lon}
    
    def check_val(self,date_val):
        if(date_val):
            return date_val.strftime("%H:%M")
        else:
            return '00:00'  
            
    def check_vals(self,date_val):
        if(date_val):
            return date_val.strftime("%I:%M %p")
        else:
            return '00:00'   

class AreaFactTable(models.Model):
    fact_id=models.AutoField(primary_key=True)
    fact_city=models.CharField(max_length=45)
    fact_state=models.CharField(max_length=45)    
    
    def __unicode__(self):
        return unicode('FT%08d'%self.fact_id)
    
class RestaurantRating(models.Model):
    restaurant_rating_id=models.AutoField(primary_key=True)
    restaurant_branch_id=models.ForeignKey(RestaurantBranch,default=None,blank=True)
    restaurant_id=models.ForeignKey(Restaurant,default=None,blank=True)
    consumer_id=models.ForeignKey(Consumer)
    restaurant_rating=models.IntegerField()
    restaurant_feedback=models.CharField(max_length=45)
    restaurant_issues=models.CharField(max_length=45)
    restaurant_rating_create_by=models.CharField(max_length=45)
    restaurant_rating_create_date=models.DateTimeField('rating create')
    restaurant_update_by=models.CharField(max_length=45)
    restaurant_update_date=models.DateTimeField(max_length=45)
    
    def __unicode__(self):
        return unicode('DMRR%08d'%self.restaurant_branch_id)
    
class RestaurantOffer(models.Model):
    restaurant_offer_id=models.AutoField(primary_key=True)
    #restaurant_branch_id=models.ForeignKey(RestaurantBranch,related_name='branch_offers',default=None,blank=True,null=True)
    restaurant_id=models.ForeignKey(Restaurant,default=None,blank=True)
    restaurant_offer_detail=models.CharField(max_length=45,default=None,blank=True)     
    restaurant_offer_creation_date=models.DateTimeField(default=datetime.now,null=True,blank=True)
    restaurant_offer_created_by=models.CharField(max_length=45,default=None,blank=True)
    restaurant_offer_update_date=models.DateTimeField(default=datetime.now,null=True,blank=True)
    restaurant_offer_update_by=models.CharField(max_length=45,default=None,blank=True)
    restaurant_offer_status=models.CharField(max_length=1,default=1)    
   
    def __unicode__(self):
        #return unicode('DMRO%08d'%self.restaurant_offer_id)           
        return unicode(self.restaurant_offer_id)           
     

class Offer_map(models.Model):
    offer_map_id=models.AutoField(primary_key=True)
    restaurant_offer_id=models.ForeignKey(RestaurantOffer)    
    restaurant_id=models.ForeignKey(Restaurant,default=None,blank=True,null=True)    
    offer_map_time_from=models.TimeField(default=None,blank=True,null=True)
    offer_map_time_to=models.TimeField(default=None,blank=True,null=True)
    offer_map_date=models.DateField(default=None,blank=True,null=True)    
    offer_map_creation_date=models.DateTimeField(default=datetime.now,null=True,blank=True)
    offer_map_created_by=models.CharField(max_length=45,default=None,blank=True)
    offer_map_update_date=models.DateTimeField(default=datetime.now,null=True,blank=True)
    offer_map_update_by=models.CharField(max_length=45,default=None,blank=True)
    offer_map_status=models.CharField(max_length=1,default=1)    
    
    def __unicode__(self):
        return unicode('DMI%08d'%self.offer_map_id) 


    
class RestaurantBooking(models.Model):                                                                          
    restaurant_booking_id=models.AutoField(primary_key=True)
    consumer_id=models.ForeignKey(Consumer,default=None,blank=True)
    restaurant_id=models.ForeignKey(Restaurant,default=None,null=True,blank=True)
    restaurant_branch_id=models.ForeignKey(RestaurantBranch,default=None,blank=True,null=True)
    restaurant_booking_date=models.DateField(default=None,blank=True)
    restaurant_booking_time_to=models.TimeField(default=None,blank=True)
    restaurant_booking_time_from=models.TimeField(default=None,blank=True)
##    restaurant_offer_id=models.ForeignKey(RestaurantOffer,default=None,blank=True)
    restaurant_offerMap_id=models.ForeignKey(Offer_map,default=None,blank=True)
    consumer_coupon_code=models.CharField(max_length=45,default=None,blank=True)                  
    restaurant_booking_covers=models.IntegerField(default=None,blank=True)  
    restaurant_booking_create_date=models.DateTimeField(default=datetime.now,null=True,blank=True)
    restaurant_booking_create_by=models.CharField(max_length=45,default=None,blank=True)
    restaurant_booking_update_date=models.DateTimeField(default=datetime.now,null=True,blank=True)
    restaurant_booking_update_by=models.CharField(max_length=45,default=None,blank=True)    
    restaurant_booking_status=models.CharField(max_length=45,default=None,choices=BOOKING_STATUS)
    restaurant_checkin_status=models.IntegerField(default=None,blank=True)
	
    
    def __unicode__(self):
        return unicode('DMBK%08d'%self.restaurant_booking_id) 
    
class Invoice(models.Model):
    invoice_id=models.AutoField(primary_key=True)
    restaurant_booking_id=models.ForeignKey(RestaurantBooking)
    consumer_id=models.ForeignKey(Consumer)
    invoice_datetime=models.DateTimeField('invoice datetime')
    invoice_amount=models.IntegerField()
    restaurant_offer_amount=models.IntegerField()
    restaurant_id=models.ForeignKey(Restaurant)
    invoice_create_datetime=models.DateTimeField('invoice create')
    invoice_create_by=models.CharField(max_length=45)
    invoice_update_date=models.DateTimeField('invoice update')
    invoice_update_by=models.CharField(max_length=45)
    invoice_status=models.CharField(max_length=1)    
    
    def __unicode__(self):
        return unicode('DMI%08d'%self.invoice_id)    
            
    


class CuisineFactTable(models.Model):
    fact_id=models.AutoField(primary_key=True)
    fact_cuisine=models.CharField(max_length=70)
    fact_cuisine_create_date=models.DateTimeField(null=True,blank=True)
    fact_cuisine_create_by=models.CharField(max_length=45,default=None,blank=True)
    fact_cuisine_update_date=models.DateTimeField(default=datetime.now,null=True,blank=True)
    fact_cuisine_update_by=models.CharField(max_length=45,default=None,blank=True)
    
    def __unicode__(self):
        return unicode(self.fact_id)
    
class CuisineRestaurentMap(models.Model):
    cuisine_rest_id=models.AutoField(primary_key=True)
    cuisine_id=models.ForeignKey(CuisineFactTable,default=None,blank=True,null=True)
    restaurant_id=models.ForeignKey(Restaurant,default=None,blank=True,null=True)
    cuisine_rest_create_date=models.DateTimeField(null=True,blank=True)
    cuisine_rest_create_by=models.CharField(max_length=45,default=None,blank=True)
    cuisine_rest_update_date=models.DateTimeField(default=datetime.now,null=True,blank=True)
    cuisine_rest_update_by=models.CharField(max_length=45,default=None,blank=True)
    
    def __unicode__(self):
        return unicode('CRM%08d'%self.cuisine_rest_id)
    
    
class CuisineRestaurentBranchMap(models.Model):
    cuisine_rest_branch_id=models.AutoField(primary_key=True)
    cuisine_id=models.ForeignKey(CuisineFactTable,default=None,blank=True,null=True)
    restaurant_branch_id=models.ForeignKey(RestaurantBranch,default=None,blank=True,null=True)
    cuisine_rest_branch_create_date=models.DateTimeField(null=True,blank=True)
    cuisine_rest_branch_create_by=models.CharField(max_length=45,default=None,blank=True)
    cuisine_rest_branch_update_date=models.DateTimeField(default=datetime.now,null=True,blank=True)
    cuisine_rest_branch_update_by=models.CharField(max_length=45,default=None,blank=True)    
    
    def __unicode__(self):
        return unicode('CRBM%08d'%self.cuisine_rest_branch_id)
    
class CategoriesFactTable(models.Model):
    category_id=models.AutoField(primary_key=True)
    category_name=models.CharField(max_length=45,default=None,blank=True)     
    category_create_date=models.DateTimeField(null=True,blank=True)
    category_create_by=models.CharField(max_length=45,default=None,blank=True)
    category_update_date=models.DateTimeField(default=datetime.now,null=True,blank=True)
    category_update_by=models.CharField(max_length=45,default=None,blank=True)
    
    def __unicode__(self):
        return unicode('MC%08d'%self.category_id)
    
    
class MenuItemTable(models.Model):
    menu_item_id=models.AutoField(primary_key=True)
    category_id=models.ForeignKey(CategoriesFactTable,default=None,blank=True,null=True)
    restaurant_id=models.ForeignKey(Restaurant,default=None,blank=True,null=True)
    category_name=models.CharField(CategoriesFactTable,max_length=45,default=None,blank=True)     
    menu_item_name=models.CharField(max_length=45,default=None,blank=True)     
    menu_item_price=models.IntegerField(default=None,blank=True)
    menu_item_type=models.CharField(max_length=45,default=None,choices=MENU_TYPE)
    menu_item_create_date=models.DateTimeField(null=True,blank=True)
    menu_item_create_by=models.CharField(max_length=45,default=None,blank=True)
    menu_item_update_date=models.DateTimeField(default=datetime.now,null=True,blank=True)
    menu_item_update_by=models.CharField(max_length=45,default=None,blank=True)
    menu_item_status=models.CharField(max_length=1,default=1)    
    
    def __unicode__(self):
        return unicode('MI%08d'%self.menu_item_id)