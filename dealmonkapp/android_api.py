import datetime as dt
import json
import math
import smtplib
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.core.context_processors import csrf
from django.core import serializers
import pdb
from django.contrib.auth.models import User
#from django.contrib.auth.models import consumer
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.template import RequestContext

from django.views.generic import TemplateView
from django.core.mail import send_mail
#import sendgrid
from deal_monk_project import settings

# importing mysqldb and system packages
import MySQLdb, sys
import datetime
import time
from django.db.models import Q
import csv
#importing exceptions
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

# HTTP Response
from django.http import HttpResponse
from django.http import HttpResponseRedirect

# Generate random password
import string
import random
import urllib 
# importing models
#from django_countries.fields import CountryField

#from dealmonkapp.models import RestaurantAdmin
from dealmonkapp.models import Consumer
from dealmonkapp.models import ConsumerPaymentCredentials
#from dealmonkapp.models import RestaurantBranchOwner
from dealmonkapp.models import Restaurant
from dealmonkapp.models import RestaurantBranch
from dealmonkapp.models import AreaFactTable
from dealmonkapp.models import RestaurantRating
from dealmonkapp.models import RestaurantOffer
from dealmonkapp.models import RestaurantBooking
from dealmonkapp.models import Invoice
from dealmonkapp.models import Offer_map
from dealmonkapp.models import CuisineFactTable
from dealmonkapp.models import CuisineRestaurentMap
from dealmonkapp.models import CuisineRestaurentBranchMap
from constants import ExceptionMessages, ExceptionLabel
from django.db import transaction
from geopy.distance import vincenty
from datetime import datetime


import datetime as dt

# foe image feild 
from base64 import b64decode
from django.core.files.base import ContentFile

#SERVER_URL = "http://192.168.0.122:8005"
SERVER_URL = "http://54.148.82.251/"

#Reset URL
#RESET_URL = 'http://ec2-52-2-239-162.compute-1.amazonaws.com/reset-password/?rpcid='

# Constants
earth_radius = 6371.0  # for kms
degrees_to_radians = math.pi/180.0
radians_to_degrees = 180.0/math.pi


#API for login
@csrf_exempt
def android_consumer_login(request):
    #pdb.set_trace()
    try:
        print request.POST 
        json_obj= json.loads(request.body)
        print 'JSON OBJECT : ',json_obj
        if request.method == 'POST':
            user = authenticate(username=json_obj['username'], password= json_obj['password'])
            #user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
            consumer = Consumer.objects.get(user_ptr_id = user.id)
            print '-------user id---------',consumer.consumer_id

            if consumer is not None:
                if user.is_active:
                    data= {'success' : 'true', 'message' :'Successful Login', 'user_info' : get_profile_info(consumer.consumer_id)}

                else:
                    data= {'success' : 'false', 'message':'User Is Not Active'}
            else:
                data= {'success' : 'false', 'error_message' :'Invalid Username or Password'}
        else:
            data= {'success' : 'false', 'error_message':'Invalid Request'}
    except User.DoesNotExist:
        print 'usr'
        data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'User Not Exist'}
    except MySQLdb.OperationalError, e:
        print e
        data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'Internal server '}
    except Exception, e:
        print e
        data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'Invalid Username or Password'}
    return HttpResponse(json.dumps(data), content_type='application/json')


#API for sign up
@csrf_exempt
def android_consumer_register(request):
#    pdb.set_trace()
    try:
        print '---request--------------------',request
        json_obj= json.loads(request.body)
        print 'JSON OBJECT : ',json_obj
        consumer_obj = Consumer(
            username=json_obj['email'],
            consumer_first_name=json_obj['first_name'],
            consumer_last_name=json_obj['last_name'],
            consumer_email=json_obj['email'],
            consumer_contactno=json_obj['phone'],
            apns_token=json_obj['apns_token'],
            sign_up_via=json_obj['sign_up_via'],
            sign_up_source=json_obj['sign_up_source'],
            consumer_image=save_image(json_obj['user_profile_image']),
            #username=json_obj['email']
            )
        consumer_obj.set_password(json_obj['pass_word'])
        consumer_obj.save()

        if consumer_obj:
            data= {'success' : 'true', 'message':'Successful Sign Up' }
        else:
            data= {'success' : 'false', 'message':'Sign Up not Successful'}
    except Consumer.DoesNotExist,e:
        # print "in the main flow"
        data= {'success' : 'false', 'message':str(e)}
    except Exception, e:
        print e
        data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'User Already Exist'}
    return HttpResponse(json.dumps(data), content_type='application/json')
#-------------------------------------------------------

#Sign Up via Gmail and Facebook 
@csrf_exempt
def android_consumer_register_facebook_gmail(request):
#    pdb.set_trace()
    try:
        print '---request--------------------',request
        json_obj= json.loads(request.body)
        print 'JSON OBJECT : ',json_obj
        consumer_obj = Consumer(
            username=json_obj['email'],
            consumer_first_name=json_obj['first_name'],
            consumer_last_name=json_obj['last_name'],
            consumer_email=json_obj['email'],
            consumer_contactno=json_obj['phone'],
            apns_token=json_obj['apns_token'],
            sign_up_via=json_obj['sign_up_via'],
            sign_up_source=json_obj['sign_up_source'],
            consumer_image=json_obj['user_profile_image']

            #username=json_obj['email']
            )
        consumer_obj.set_password(json_obj['pass_word'])
        consumer_obj.save()


        filename = "IMG_%s_%s.jpg" % (consumer_obj.username, str(datetime.now()).replace('.','_')) # For giving filename to Image
        resource = urllib.urlopen(json_obj['user_profile_image'])

        consumer_obj.consumer_image = ContentFile(resource.read(), filename) # assign image to model
        consumer_obj.save()

        if consumer_obj:
            data= {'success' : 'true', 'message':'Successful Sign Up', 'user_info' : get_updated_profile_info(consumer_obj.id)}
        else:
            data= {'success' : 'false', 'message':'Sign Up not Successful'}
    except Consumer.DoesNotExist,e:
        # print "in the main flow"
        data= {'success' : 'false', 'message':str(e)}
    except Exception, e:
        print e
        data= {'success' : 'login', 'message': 'User Already Exist'}
    return HttpResponse(json.dumps(data), content_type='application/json')

#-----------------------------------------------
#API for update profile
@csrf_exempt
def android_update_consumer_profile(request):
    print request
    try:
        json_obj= json.loads(request.body)
        print 'JSON OBJECT : ',json_obj
        if request.method == 'POST':

            consumer_object = Consumer.objects.get(consumer_id=json_obj['user_id'])
           
            consumer_object.consumer_first_name = json_obj['first_name']
            consumer_object.consumer_last_name = json_obj['last_name']

            consumer_object.consumer_image=save_image(json_obj['user_profile_image'])
            consumer_object.consumer_contactno = json_obj['phone']

            print '---------------------------------------',consumer_object.consumer_contactno
            consumer_object.consumer_email = json_obj['email']

            consumer_object.save()
            data = {'success':'true', 'message':'Profile Update successfully', 'user_info' : get_updated_profile_info(consumer_object.id) }
        else:
            data = {'success':'false', 'error_message':'Profile Update Failed'}
    except Consumer.DoesNotExist, e:
        print e
        data = {'success':'false', 'error_message':'Invalid Request'}
    except Exception, e:
        print e
        data = {'success':'false', 'error_message': 'Server Internal Error'}
    return HttpResponse(json.dumps(data), content_type='application/json')

#API for change password
@csrf_exempt
def android_change_password(request):
    try:
        if request.method == 'POST':
            data ={}
        json_obj=json.loads(request.body)
        print 'JSON OBJECT : ',json_obj
        email=json_obj['email']


        user = authenticate(username=json_obj['email'], password= json_obj['pass_word'])
        print '-consumer------',user

        if user is not None:
            if user.is_active:
                user.set_password(json_obj['change_password'])
                user.save()
                print 'succeess'
                data= {'success' : 'true', 'message':'Password changed successfully'}
            else:
                data= {'success' : 'false', 'error_message':'User Is Not Active'}
        else:
            data= {'success' : 'false', 'error_message':'Invalid Username or Password'}
##        else:
##            data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'Invalid Request'}
    except User.DoesNotExist:
        print 'usr'
        data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'User Not Exit'}
    except MySQLdb.OperationalError, e:
        print e
        data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'Internal Server Error '}
    except Exception, e:
        print e
        data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'Internal Server Error '}
    return HttpResponse(json.dumps(data), content_type='application/json')

#API for sms alert
@csrf_exempt
def android_sms_alert_activation(request):
    try:

        if request.method == 'POST':
            json_obj=json.loads(request.body)
            print '-----------json---------------',json_obj
            user_id = json_obj['user_id']
            consumer = Consumer.objects.get(consumer_id = user_id)
            consumer.is_consumer_sms_alert = json_obj['sms_alert']
            consumer.save()
            data = {'success': 'true', 'message' : "SMS alert sent" }

    except Consumer.DoesNotExist, e:
        data = {'success': 'false', 'message':"SMS alert not sent"}
        print "failed to sent mail", e
    except Exception, e:
        print e
        data = {'success': 'false', 'message':"Server Error, Please try again!"}
    return HttpResponse(json.dumps(data), content_type='application/json')

#API for email alert
@csrf_exempt
def android_email_alert_activation(request):
    try:
        if request.method == 'POST':
            json_obj=json.loads(request.body)
            print '-----------json---------------',json_obj
            user_id = json_obj['user_id']
            consumer = Consumer.objects.get(consumer_id = user_id)
            consumer.is_consumer_email_alert = json_obj['email_alert']
            consumer.save()
            data = {'success': 'true', 'message' : "Email alert sent" }

    except Consumer.DoesNotExist, e:
        data = {'success': 'false', 'message':"Email alert not sent"}
        print "failed to sent mail", e
    except Exception, e:
        print e
        data = {'success': 'false', 'message':"Server Error, Please try again!"}
    return HttpResponse(json.dumps(data), content_type='application/json')

#save consumer feedback
@csrf_exempt
def android_consumer_feedback(request):
    try:
        if request.method == 'POST':
            json_obj=json.loads(request.body)
            user_id = json_obj['user_id']
            consumer = Consumer.objects.get(consumer_id = user_id)
            consumer.consumer_feedback = json_obj['feedback']
            consumer.save()
            data = {'success': 'true', 'message' : "Feedback send" }

    except Consumer.DoesNotExist, e:
        data = {'success': 'false', 'message':"feedback not send"}
        print "failed to send mail", e
    except Exception, e:
        print e
        data = {'success': 'false', 'message':"Server Error, Please try again!"}
    return HttpResponse(json.dumps(data), content_type='application/json')



# Getting customer profile info
def get_profile_info(user_id):
    consumer_object = Consumer.objects.get(consumer_id=user_id)
    data = {
        'basic': {
            'user_id'    : str(consumer_object.consumer_id),
            'first_name' : consumer_object.consumer_first_name,
            'last_name'  : consumer_object.consumer_last_name,
            'phone'  : consumer_object.consumer_contactno,
            'user_profile_image'      : SERVER_URL + consumer_object.consumer_image.url,
            'email_id'   : consumer_object.username
                }
    }
    return data #HttpResponse(json.dumps(data), content_type='application/json')

# Getting profile info for facebook
def get_info(consumer_id):
    consumer_object = Consumer.objects.get(id=consumer_id)
    data = {
        'basic': {
            'user_id'    : str(consumer_object.id),
            'first_name' : consumer_object.consumer_first_name,
            'last_name'  : consumer_object.consumer_last_name,
            'phone'  : consumer_object.consumer_contactno,
            'user_profile_image'      : SERVER_URL + consumer_object.consumer_image.url,
            'email_id'   : consumer_object.username
                }
    }
    consumer_object.save()
    return data #HttpResponse(json.dumps(data), content_type='application/json')


# Getting updated customer profile info
def get_updated_profile_info(user_id):
    consumer_object = Consumer.objects.get(id=user_id)
    data = {
        'basic': {
            'user_id'    : str(consumer_object.id),
            'first_name' : consumer_object.consumer_first_name,
            'last_name'  : consumer_object.consumer_last_name,
            'phone'  : consumer_object.consumer_contactno,
            'user_profile_image' : SERVER_URL + consumer_object.consumer_image.url,
            'email_id'   : consumer_object.consumer_email
                }
    }
    return data #HttpResponse(json.dumps(data), content_type='application/json')

#API to get restaurant list
@csrf_exempt
def android_restaurant_list(request):
#    pdb.set_trace()

    nameList=[]
    tpl1 = []
    cuisine_type_list = []
    try:
        if request.method == 'POST':
            json_obj= json.loads(request.body)

            print 'JSON OBJECT : ',json_obj
            consumer_latitude=json_obj['latitude']
            consumer_longitude=json_obj['longitude']
            offfer_time = json_obj['time']
            date = json_obj['date']

            lon_max, lon_min, lat_max, lat_min = bounding_box(float(consumer_latitude),float(consumer_longitude),5)
            #==============for restaurant=============
            restaurant=Restaurant.objects.filter(restaurant_lat__range=[lat_min,lat_max], restaurant_lon__range=[lon_min,lon_max])
            print '========restaurant================',restaurant
       
            restaurant_offer = Offer_map.objects.filter(restaurant_id__in=restaurant,offer_map_date=date,offer_map_time_from__lt=offfer_time,offer_map_time_to__gt=offfer_time)
            print '==============res offer===============',restaurant_offer

            current_date = datetime.now()

            for offer in restaurant_offer:

                restaurant_id = "Restaurant "+str(offer.restaurant_id)

                restaurant_name = offer.restaurant_id.restaurant_name

                restaurant_area = offer.restaurant_id.restaurant_area

                #restaurant_cuisine = offer.restaurant_id.restaurant_cuisine_type

                restaurant_latitude = offer.restaurant_id.restaurant_lat

                restaurant_longitude = offer.restaurant_id.restaurant_lon

                consumer_position = (consumer_latitude,consumer_longitude)
                restaurant_position = (offer.restaurant_id.restaurant_lat,offer.restaurant_id.restaurant_lon)
                dist = vincenty(consumer_position, restaurant_position).meters
                final_dist = dist/1000
                final_dist = ("%.3f" % final_dist) + " " + "km"

                restaurant_distance = final_dist

            	restaurant_image = SERVER_URL + str(offer.restaurant_id.restaurant_image.url)

                restaurant_offer_detail = offer.restaurant_offer_id.restaurant_offer_detail
                
                # function to get restaurant cuisine
                cuisine_object = CuisineRestaurentMap.objects.filter(restaurant_id=offer.restaurant_id)
                print '==========cuisine===========',cuisine_object
                if(len(cuisine_object)>0):   
                    cuisine_type_list = []
                    for cuisine_obj in cuisine_object:
                        cuisine_type = cuisine_obj.cuisine_id.fact_cuisine
                        cuisine_type_list.append(str(cuisine_type))
                else:
                    cuisine_type_list = []

                tpl={ 'restaurantId' : restaurant_id, 'offer' : restaurant_offer_detail, 'restaurantname' : restaurant_name,  'location' : restaurant_area, 'cuisine' : cuisine_type_list ,'distance' : restaurant_distance, 'image' : restaurant_image, 'longitude' : restaurant_longitude, 'latitude' : restaurant_latitude}            
                tpl1.append(tpl)

		#===================================for restaurant branch=================
            restaurant_branch=RestaurantBranch.objects.filter(restaurant_branch_lat__range=[lat_min,lat_max], restaurant_branch_lon__range=[lon_min,lon_max])

            restaurant_id_list1 = []
            for branch in restaurant_branch:
                restaurant_id = str(branch.restaurant_id)
                restaurant_id_list1.append(str(restaurant_id))

            restaurant_offer1 = Offer_map.objects.filter(restaurant_id__in=restaurant_id_list1,offer_map_date=date, offer_map_time_from__lt= offfer_time,offer_map_time_to__gt= offfer_time)

            for offer in restaurant_offer1:

                branch_object1 = RestaurantBranch.objects.filter(restaurant_id=offer.restaurant_id,restaurant_branch_id__in=restaurant_branch)

                for branch1 in branch_object1:
                    restaurant_area = branch1.restaurant_branch_area

                    restaurant_latitude = branch1.restaurant_branch_lat

                    restaurant_longitude = branch1.restaurant_branch_lon

                    restaurant_name = branch1.restaurant_branch_name

                    #restaurant_cuisine = offer.restaurant_id.restaurant_cuisine_type

                    restaurant_offer_detail = offer.restaurant_offer_id.restaurant_offer_detail

                    restaurant_image = SERVER_URL + str(offer.restaurant_id.restaurant_image.url)

                    restaurant_id = "Restaurant " + str(branch1.restaurant_branch_id)

                    consumer_position = (consumer_latitude,consumer_longitude)
                    restaurant_position = (branch1.restaurant_branch_lat,branch1.restaurant_branch_lon)
                    dist = vincenty(consumer_position, restaurant_position).meters
                    final_dist = dist/1000
                    final_dist = ("%.3f" % final_dist) + " " + "km"

                    restaurant_distance = final_dist

                    tpl={ 'restaurantId' : restaurant_id, 'offer' : restaurant_offer_detail, 'restaurantname' : restaurant_name,  'location' : restaurant_area, 'cuisine' : ' ' ,'distance' : restaurant_distance, 'image' : restaurant_image, 'longitude' : restaurant_longitude, 'latitude' : restaurant_latitude}
                tpl1.append(tpl)
        data = {'nameList': tpl1, 'success':'true'}
    except MySQLdb.OperationalError, e:
        data = {'BranchList': 'none', 'error_message':'Restaurant list Fail'}
    return HttpResponse(json.dumps(data), content_type='application/json')



#functions to calculate min-max lat-long range

def change_in_latitude(distance):
    "Given a distance north, return the change in latitude."
    return (distance/earth_radius)*radians_to_degrees

def change_in_longitude(latitude, distance):
    "Given a latitude and a distance west, return the change in longitude."
    # Find the radius of a circle around the earth at given latitude.
    r = earth_radius*math.cos(latitude*degrees_to_radians)
    return (distance/r)*radians_to_degrees

def bounding_box(latitude, longitude, distance):
    lat_change = change_in_latitude(distance)
    lat_max = latitude + lat_change
    lat_min = latitude - lat_change
    lon_change = change_in_longitude(latitude, distance)
    lon_max = longitude + lon_change
    lon_min = longitude - lon_change
    return (lon_max, lon_min, lat_max, lat_min)


# forgot password api
@csrf_exempt
def android_forgot_password(request):
    #pdb.set_trace()
    gmail_user = "training.tungsten@gmail.com"
    gmail_pwd = "team@tungsten74$"
    FROM = 'Dealmonk App Admin'
    TO = []
    chars = string.letters + string.digits
    pwdSize = 8
    password = ''.join((random.choice(chars)) for x in range(pwdSize))
    #password = "password1"	

    try:
        if request.method == 'POST':
            json_obj=json.loads(request.body)
            user_name = json_obj['email']
            TO.append(user_name)

            consumer_obj = Consumer.objects.get(username = user_name) 

            user = User.objects.get(username = json_obj['email'])
            user.set_password(password)
            user.save()
            TEXT = "Your new password is" + " " + password
            SUBJECT = "New Password"
            server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!

            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_pwd)
            message = """From: %s\nTo: %s\nSubject: %s\n\n%s """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
            server.sendmail(FROM, TO, message)
            server.close()			
            data = {'success': 'true', 'message' : "Forgot Password Send Successfully" }

    except User.DoesNotExist, e:
        data = {'success': 'false', 'message':"Forgot Password Failed"}
        print "failed to send mail", e
    except Exception, e:
        print e
        data = {'success': 'false', 'message':"Server Error, Please try again!"}
    return HttpResponse(json.dumps(data), content_type='application/json')

# API for my deal
#@csrf_exempt
def android_my_deal(request):
    nameList=[]
    restaurant_branch_id_list = []
    restaurant_branch_name_list = []
    restaurant_booking_date_list = []
    restaurant_booking_time_list = []
    restaurant_branch_location_list = []
    restaurant_booking_status_list = []
    restaurant_contact_no_list = []
    restaurant_branch_image_list = []
    restaurant_branch_coupon_list = []
    restaurant_branch_offer_list = []
    restaurant_branch_contact_list = []

    print 'request : ',request
#    pdb.set_trace()
    try:
        #json_obj= json.loads(request.GET)

        #print 'JSON OBJECT : ',json_obj

        user_id=request.GET.get('user_id')

        booking_object = RestaurantBooking.objects.filter(consumer_id = user_id).order_by('-restaurant_booking_date')
        print '---------------- booking_object-------------',booking_object

        for booking in booking_object:
            print '=====booking====',booking
            id = booking.restaurant_branch_id
            print '-id----------',id
            if(id!=None):    
                branch_obj = RestaurantBranch.objects.filter(restaurant_branch_id = str(id))
                print '==========here=================',branch_obj
                restaurant_branch_id = booking.restaurant_branch_id
                restaurant_branch_id_list.append(str(restaurant_branch_id))	

                restaurant_branch_name = booking.restaurant_branch_id.restaurant_branch_name
                restaurant_branch_name_list.append(str(restaurant_branch_name))	

                restaurant_booking_date = booking.restaurant_booking_date
                restaurant_booking_date_list.append(str(restaurant_booking_date))	

                restaurant_booking_time = booking.restaurant_booking_time
                restaurant_booking_time_list.append(str(restaurant_booking_time))

                restaurant_branch_location = booking.restaurant_branch_id.restaurant_branch_area
                restaurant_branch_location_list.append(str(restaurant_branch_location))

                restaurant_branch_image = SERVER_URL + str(booking.restaurant_branch_id.restaurant_id.restaurant_image.url)
                restaurant_branch_image_list.append(str(restaurant_branch_image))

                restaurant_branch_contact = booking.restaurant_branch_id.restaurant_branch_contact
                restaurant_branch_contact_list.append(str(restaurant_branch_contact))	

                restaurant_branch_coupon = booking.consumer_coupon_code
                restaurant_branch_coupon_list.append(str(restaurant_branch_coupon))

                restaurant_branch_offer = booking.restaurant_offer_id.restaurant_offer_detail
                restaurant_branch_offer_list.append(str(restaurant_branch_offer))
                
            else:
                restaurant_id = booking.restaurant_id
                restaurant_branch_id_list.append(str(restaurant_id))	

                restaurant_name = booking.restaurant_id.restaurant_name
                restaurant_branch_name_list.append(str(restaurant_name))	

                restaurant_booking_date = booking.restaurant_booking_date
                restaurant_booking_date_list.append(str(restaurant_booking_date))	

                restaurant_booking_time = booking.restaurant_booking_time
                restaurant_booking_time_list.append(str(restaurant_booking_time))

                restaurant_location = booking.restaurant_id.restaurant_area
                restaurant_branch_location_list.append(str(restaurant_location))

                restaurant_image = SERVER_URL + str(booking.restaurant_id.restaurant_image.url)
                restaurant_branch_image_list.append(str(restaurant_image))

                restaurant_contact = booking.restaurant_id.restaurant_contactno
                restaurant_branch_contact_list.append(str(restaurant_contact))	

                restaurant_branch_coupon = booking.consumer_coupon_code
                restaurant_branch_coupon_list.append(str(restaurant_branch_coupon))

                restaurant_branch_offer = booking.restaurant_offer_id.restaurant_offer_detail
                restaurant_branch_offer_list.append(str(restaurant_branch_offer))
                	

            tpl={ 'restaurantId' : restaurant_branch_id_list,'restaurantname' : restaurant_branch_name_list, 'date' : restaurant_booking_date_list, 'time' : restaurant_booking_time_list, 'location' : restaurant_branch_location_list, 'status' : restaurant_booking_status_list, 'image' : restaurant_branch_image_list, 'coupon' : restaurant_branch_coupon_list, 'offer' : restaurant_branch_offer_list, 'offer' : restaurant_branch_offer_list }
            print '----------tpl-------------------',tpl
        data = {'nameList': tpl, 'success':'true'}
   
    except:
        data = {'BranchList': 'none', 'error_message':'Deals not available'}
    return HttpResponse(json.dumps(data), content_type='application/json')



# This method is for filtering the product details shown in catalog page.
def android_searchRestaurantBranch(request):
    try:
        consumer_latitude=request.GET.get('currentLatitude')
        consumer_longitude=request.GET.get('currentLongitude')
        date=request.GET.get('date')

        filter_args={}
        filter_restaurant_args={}
        filter_offer_start_time_args={}
        filter_offer_end_time_args={}
        filter_restaurant_args1={}
        filter_restaurant_branch_args={}
        vNameStatus=0
        vname=""
        tpl1=[]

		#============= for restaurant ===========================
        if request.GET.get('Location'):
            filter_restaurant_args['restaurant_area__icontains'] = request.GET.get('Location')

        if request.GET.get('Cuisine'):
			filter_restaurant_args['restaurant_cuisine_type__icontains']=request.GET.get('Cuisine')

        if request.GET.get('Time'):

			filter_offer_start_time_args['offer_map_time_from__lt'] = request.GET.get('Time')

        if request.GET.get('Time'):

			filter_offer_end_time_args['offer_map_time_to__gt'] = request.GET.get('Time')

        restaurant_offer_search = Offer_map.objects.filter(Q(**filter_offer_start_time_args) | Q(**filter_offer_end_time_args) | Q(restaurant_id= Restaurant.objects.filter(Q(**filter_restaurant_args))),offer_map_date=request.GET.get('Date'))        

        for offer in restaurant_offer_search:
            restaurant_id = offer.restaurant_id

            restaurant_name = offer.restaurant_id.restaurant_name

            restaurant_area = offer.restaurant_id.restaurant_area

            restaurant_cuisine = offer.restaurant_id.restaurant_cuisine_type

            restaurant_image = SERVER_URL + str(offer.restaurant_id.restaurant_image.url)

            restaurant_latitude = offer.restaurant_id.restaurant_lat

            restaurant_longitude = offer.restaurant_id.restaurant_lon

            consumer_position = (consumer_latitude,consumer_longitude)
            restaurant_position = (offer.restaurant_id.restaurant_lat,offer.restaurant_id.restaurant_lon)
            dist = vincenty(consumer_position, restaurant_position).meters
            final_dist = dist/1000
            final_dist = ("%.3f" % final_dist) + " " + "km"

            restaurant_distance = final_dist

            restaurant_offer_detail = offer.restaurant_offer_id.restaurant_offer_detail

			# ==============for restaurant branch ========================

        if request.GET.get('Location'):
            filter_restaurant_branch_args['restaurant_branch_area__icontains'] = request.GET.get('Location')

        if request.GET.get('Cuisine'):
            filter_restaurant_branch_args['restaurant_branch_cuisine_type__icontains']=request.GET.get('Cuisine')

        restaurant_branch_obj = RestaurantBranch.objects.filter(Q(**filter_restaurant_branch_args)) 

        restaurant_id_list2 = []
        for branch in restaurant_branch_obj:
            restaurant_id = branch.restaurant_id
            restaurant_id_list2.append(str(restaurant_id))

        filter_restaurant_args1['restaurant_id__in'] = restaurant_id_list2

        restaurant_offer_search1 = Offer_map.objects.filter(Q(**filter_offer_start_time_args) | Q(**filter_offer_end_time_args) | Q(restaurant_id= Restaurant.objects.filter(Q(**filter_restaurant_args1))),offer_map_date=request.GET.get('Date')) 



        for branch_offer1 in restaurant_offer_search1:

            branch_object2 = RestaurantBranch.objects.filter(restaurant_id=branch_offer1.restaurant_id,restaurant_branch_id__in=restaurant_branch_obj)

            for branch1 in branch_object2:
                restaurant_area = branch1.restaurant_branch_area

                restaurant_offer = branch_offer1.restaurant_offer_id.restaurant_offer_detail

                restaurant_cuisine = branch_offer1.restaurant_id.restaurant_cuisine_type

                restaurant_image = SERVER_URL + str(branch_offer1.restaurant_id.restaurant_image.url)

                restaurant_name = branch1.restaurant_branch_name

                restaurant_latitude = branch1.restaurant_branch_lat

                restaurant_longitude = branch1.restaurant_branch_lon

                restaurant_id = branch1.restaurant_branch_id

                consumer_position = (consumer_latitude,consumer_longitude)
                restaurant_position = (branch1.restaurant_branch_lat,branch1.restaurant_branch_lon)
                dist = vincenty(consumer_position, restaurant_position).meters
                final_dist = dist/1000
                final_dist = ("%.3f" % final_dist) + " " + "km"

                restaurant_distance = final_dist                     
 
        tpl={ 'restaurantId' : restaurant_id_list, 'offer' : restaurant_offer_detail_list, 'restaurantname' : restaurant_name_list, 'location' : restaurant_area_list, 'cuisine' : restaurant_cuisine_list,'image' : restaurant_image_list, 'distance' : restaurant_distance_list, 'longitude' : restaurant_longitude_list, 'latitude' : restaurant_latitude_list}
        print '====================',tpl
      
        data = {'nameList': tpl, 'success':'true'}
    except MySQLdb.OperationalError, e:
        data = {'BranchList': 'none', 'error_message':'Mydeals list Fail'}
    return HttpResponse(json.dumps(data), content_type='application/json')

def save_image(imgdata):
    import os
    print "save_image"
    # pdb.set_trace()
    try:
        # imgdata = json_obj['imgstr']
        print imgdata
        filename = "uploaded_image%s.png" % str(datetime.now()).replace('.','_')
        decoded_image = imgdata.decode('base64')
        return ContentFile(decoded_image, filename)

    except Exception, e:
        print e
        data = {'data': None, ExceptionLabel.ERROR_MESSAGE:'Server Error - Please Try Again'}
        return False


# API for restaurant views
def android_restaurant_view_list(request):
#    pdb.set_trace()

    nameList=[]
    try:
        data = {}
        restaurant_id=request.GET.get('restaurant_id')
        identifier = restaurant_id.split( )[0]
        id = restaurant_id.split( )[1]

        offer_time=request.GET.get('time')
        print '=========offer time================',offer_time
        offer_date=request.GET.get('date')
        print '=========offer_date================',offer_date
        if (identifier=="Restaurant"):
			tpl = restaurant_offer(id,offer_time,offer_date)
			print '=============in function1==============',tpl

        else:
			tpl = restaurant_branch_offer(id,offer_time,offer_date)
			print '=============in function2==============',tpl
        data = {'restaurantOfferList': tpl, 'success':'true'}
    except MySQLdb.OperationalError, e:
        data = {'nameList': tpl, 'success':'true'}
    return HttpResponse(json.dumps(data), content_type='application/json')

# function for restaurant offer view
def restaurant_offer(id,offer_time,offer_date):
    
    restaurant_name_list = []
    restaurant_offer_start_time_list = []
    restaurant_offer_end_time_list = []
    restaurant_area_list = []
    restaurant_offer_detail_list = []
    restaurant_image_detail_list = []
    restaurant_contact_detail_list = []
    restaurant_offer_id_list = []
    restaurant_area = []
    restaurant_offer = Offer_map.objects.filter(restaurant_id=id,offer_map_time_to__gt= offer_time,offer_map_date=offer_date).order_by('offer_map_time_from')
    print '------res offer---',restaurant_offer
    if(restaurant_offer>0):
        for offer in restaurant_offer:
            print '-offer---------',offer
            time = str(offer. offer_map_time_to)
            duration = (dt.datetime.strptime(time, '%H:%M:%S')-dt.datetime.strptime(offer_time, '%H:%M:%S')).seconds/60
            if(duration>=15):

                print '=========duration=====',duration

                restaurant_area.append(str(offer.restaurant_id.restaurant_addr1)) 
                restaurant_area.append(str(offer.restaurant_id.restaurant_addr2)) 
                restaurant_area.append(str(offer.restaurant_id.restaurant_area)) 
                restaurant_area.append(str(offer.restaurant_id.restaurant_city))  

                #restaurant_branch_image = SERVER_URL + str(offer.restaurant_branch_id.restaurant_branch_image.url)


                restaurant_offer_detail = offer.restaurant_offer_id.restaurant_offer_detail
                restaurant_offer_detail_list.append(str(restaurant_offer_detail))

                restaurant_offer_id = offer.restaurant_offer_id
                restaurant_offer_id_list.append(str(restaurant_offer_id)[4:])

                restaurant_name = offer.restaurant_id.restaurant_name

                restaurant_contact_detail = offer.restaurant_id.restaurant_contactno

                restaurant_offer_start_time = offer.offer_map_time_from.strftime("%I:%M %p")
                restaurant_offer_start_time_list.append(str(restaurant_offer_start_time))

                restaurant_offer_end_time = offer.offer_map_time_to.strftime("%I:%M %p")
            
                converted_time = offer.offer_map_time_to.hour
        restaurant_offer_start_time_list.append(str(restaurant_offer_end_time))
        
        tpl={'restaurant_offer_list' : restaurant_offer_detail_list, 'offer_id' : restaurant_offer_id_list,'restaurant_address' : restaurant_area, 'restaurant_phone' : str(restaurant_contact_detail), 'restaurant_offertimeperiod' : restaurant_offer_start_time_list, 'restaurant_name' : restaurant_name}
        return tpl
    else:
        tpl = {}
        return tpl

# function for restaurant branch offer view
def restaurant_branch_offer(id,offer_time,offer_date):
    
    restaurant_name_list = []
    restaurant_offer_start_time_list = []
    restaurant_offer_end_time_list = []
    restaurant_offer_detail_list = []
    restaurant_image_detail_list = []
    restaurant_contact_detail_list = []
    restaurant_offer_id_list = []
    restaurant_branch_area = []

    restaurant_branch = RestaurantBranch.objects.filter(restaurant_branch_id = id)
    print '------------1----------',restaurant_branch
    for branch in restaurant_branch:
		res_id = branch.restaurant_id


    restaurant_offer = Offer_map.objects.filter(restaurant_id=res_id,offer_map_time_to__gt= offer_time,offer_map_date=offer_date).order_by('offer_map_time_from')
    print '------------offer1----------',restaurant_offer

    if(restaurant_offer>0):
        for offer in restaurant_offer:
            print '-offer---------',offer
            time = str(offer.offer_map_time_to)
            duration = (dt.datetime.strptime(time, '%H:%M:%S')-dt.datetime.strptime(offer_time, '%H:%M:%S')).seconds/60
            if(duration>=15):
                print '-----------in function 2---------------'
                branch_object = RestaurantBranch.objects.filter(restaurant_id=offer.restaurant_id,restaurant_branch_id__in=restaurant_branch)
                print '---------obj------',branch_object 
            	for branch in branch_object:

                    restaurant_branch_area.append(str(branch.restaurant_branch_area)) 
                    restaurant_branch_area.append(str(branch.restaurant_branch_address1)) 
                    restaurant_branch_area.append(str(branch.restaurant_branch_address2)) 
                    restaurant_branch_area.append(str(branch.restaurant_branch_city))

		            #restaurant_branch_image = SERVER_URL + str(offer.restaurant_branch_id.restaurant_branch_image.url)


                    restaurant_offer_detail = offer.restaurant_offer_id.restaurant_offer_detail
                    restaurant_offer_detail_list.append(str(restaurant_offer_detail))

                    restaurant_offer_id = offer.restaurant_offer_id
                    restaurant_offer_id_list.append(str(restaurant_offer_id)[4:])

                    restaurant_contact_detail = branch.restaurant_branch_contact

                    restaurant_branch_name = branch.restaurant_id.restaurant_name

                    restaurant_offer_start_time = offer.offer_map_time_from.strftime("%I:%M %p")
                    restaurant_offer_start_time_list.append(str(restaurant_offer_start_time))

                    restaurant_offer_end_time = offer.offer_map_time_to.strftime("%I:%M %p")
		        
                    converted_time = offer.offer_map_time_to.hour
        restaurant_offer_start_time_list.append(str(restaurant_offer_end_time))
        tpl={'restaurant_offer_list' : restaurant_offer_detail_list, 'offer_id' : restaurant_offer_id_list,'restaurant_address' : restaurant_branch_area, 'restaurant_phone' : str(restaurant_contact_detail), 'restaurant_offertimeperiod' : restaurant_offer_start_time_list, 'restaurant_name' :restaurant_branch_name }
        print tpl

        return tpl
    else:
		    tpl = {}
		    return tpl


@csrf_exempt
def android_book_restaurant(request):
#    pdb.set_trace()

    nameList=[]
    try:
        print '===========in function ==='
        json_obj=json.loads(request.body)
        data = {}
        restaurant_id=json_obj['restaurantId']
        identifier = restaurant_id.split( )[0]
        id = restaurant_id.split( )[1]
        print '======================',id
        if(identifier=="Restaurant"):
            print '==========inside the function================'
            consumer=Consumer.objects.get(consumer_id=json_obj['user_id'])
            restaurant = Restaurant.objects.get(restaurant_id=id)
            booking_obj = RestaurantBooking(
            restaurant_booking_date=json_obj['booking_date'],
            restaurant_booking_time=json_obj['booking_time'],
            restaurant_booking_create_date=json_obj['booking_date'],
            restaurant_booking_covers=json_obj['covers'],	
            restaurant_booking_create_by	= consumer.consumer_email,
            restaurant_booking_update_by=consumer.consumer_email,
            restaurant_booking_status = "Confirmed",
            restaurant_checkin_status = "0"
            )
            chars = string.digits
            size = 4
            checkin_no = "DM" +''.join((random.choice(chars)) for x in range(size))
            print '=============check_in============',checkin_no    
            booking_obj.consumer_id=Consumer.objects.get(consumer_id=json_obj['user_id'])
            booking_obj.restaurant_id=Restaurant.objects.get(restaurant_id=id)
            #booking_obj.owner_id=RestaurantAdmin.objects.get(owner_id="1")
            booking_obj.restaurant_offer_id=RestaurantOffer.objects.get(restaurant_offer_id=json_obj['offer_id'])  
            booking_obj.consumer_coupon_code=checkin_no
            booking_obj.save()
            print '=======',booking_obj
            if booking_obj:
                data= {'success' : 'true', 'message':'Booking Saved Successfully'}
            else:
                data= {'success' : 'false', 'message':'Booking Not Saved Successfully'}
        else:
                print '===================in second function====================='
                consumer=Consumer.objects.get(consumer_id=json_obj['user_id'])
                restaurant_branch = RestaurantBranch.objects.get(restaurant_branch_id=id)
                booking_obj = RestaurantBooking(
                    restaurant_booking_date=json_obj['booking_date'],
                    restaurant_booking_time=json_obj['booking_time'],
                    restaurant_booking_create_date=json_obj['booking_date'],
                    restaurant_booking_covers=json_obj['covers'],	
                    restaurant_booking_create_by	= consumer.consumer_email,
                    restaurant_booking_update_by=consumer.consumer_email,
                    restaurant_booking_status = "Confirmed",
                    restaurant_checkin_status = "0"
                    )
                chars = string.digits
                size = 4
                checkin_no = "DM" +''.join((random.choice(chars)) for x in range(size))
                print '=============check_in============',checkin_no    
                booking_obj.consumer_id=Consumer.objects.get(consumer_id=json_obj['user_id'])
                booking_obj.restaurant_branch_id=RestaurantBranch.objects.get(restaurant_branch_id=id)
                #booking_obj.owner_id=RestaurantAdmin.objects.get(owner_id="1")
                booking_obj.restaurant_offer_id=RestaurantOffer.objects.get(restaurant_offer_id=json_obj['offer_id'])  
                booking_obj.consumer_coupon_code=checkin_no
                booking_obj.save()
                if booking_obj:
                    data= {'success' : 'true', 'message':'Booking Saved Successfully'}
                else:
                    data= {'success' : 'false', 'message':'Booking Not Saved Successfully'}

    except MySQLdb.OperationalError, e:
        data = {'nameList': data, 'success':'true'}
    return HttpResponse(json.dumps(data), content_type='application/json')

# API for checkin

def android_checkin(request):
#    pdb.set_trace()

    nameList=[]
    try:
            consumer_location=request.GET.get('location')
            consumer_latitude=request.GET.get('latitude')
            consumer_longitude=request.GET.get('longitude')
            offfer_time = request.GET.get('time')
            date = request.GET.get('date')
            user_id = request.GET.get('user_id')

	
            lon_max, lon_min, lat_max, lat_min = bounding_box(float(consumer_latitude),float(consumer_longitude),0.5)
            print '=========== in function=============',lon_max, lon_min, lat_max, lat_min
            restaurant_booking_obj = RestaurantBooking.objects.filter(consumer_id=user_id,restaurant_booking_date=date)
            print '------restaurant_booking_obj---------',restaurant_booking_obj
            if(len(restaurant_booking_obj)>0):
                for obj in restaurant_booking_obj:
                    id = obj.restaurant_id
                    print '======here============',id
                        
                if(id!=None):
                    id = obj.restaurant_id

                    print '============hiiiii ankita============='

                    restaurant_obj = RestaurantBooking.objects.filter(restaurant_booking_id=restaurant_booking_obj,restaurant_id=id)
                    print '==========obj======',restaurant_obj
                    for obj in restaurant_obj:
                        id = obj.restaurant_id
                        branch_obj = RestaurantBranch.objects.filter(restaurant_branch_lat__range=[lat_min,lat_max], restaurant_branch_lon__range=[lon_min,lon_max])
                        print '----------branch obj----------------',branch_obj
                        if(len(branch_obj)>0):
                            status = obj.restaurant_booking_status
                            print '-status===',status
                            if(status=="Confirmed"):
                                obj.restaurant_booking_status="Completed"
                                coupone_code = obj.consumer_coupon_code
                                obj.restaurant_checkin_status="1"
                                message = str(coupone_code)
                            else:
                                message = "Already checked in"
                            obj.save()
                        else:
                            print '------- meteres----'
                            message = "For GPS checkin please be within 500 meters from the restaurant"    
                else:
                    id = obj.restaurant_branch_id

                    print '============hiiiiiiiiiiiii============='

                    restaurant_obj = RestaurantBooking.objects.filter(restaurant_booking_id=restaurant_booking_obj,restaurant_branch_id=id)
                    print '==========obj======',restaurant_obj
                    for obj in restaurant_obj:
                        id = obj.restaurant_branch_id
                        branch_obj = RestaurantBranch.objects.filter(restaurant_branch_lat__range=[lat_min,lat_max], restaurant_branch_lon__range=[lon_min,lon_max])
                        print '----------branch obj----------------',branch_obj
                        if(len(branch_obj)>0):
                            print '---------control is here-------------',id
                            status = obj.restaurant_booking_status
                            print '-status===',status
                            if(status=="Confirmed"):
                                obj.restaurant_booking_status="Completed"
                                coupone_code = obj.consumer_coupon_code
                                obj.restaurant_checkin_status="1"
                                message = str(coupone_code)
                            else:
                                message = "Already checked in"
                            obj.save()
                        else:
                            print '------- meteres----'
                            message = "For GPS checkin please be within 500 meters from the restaurant"
            else:
                message = "No bookings available"
            data = {'message': message, 'success':'true'}
    except MySQLdb.OperationalError, e:
        data = {'message': 'none', 'error_message':'Checkin Fail'}
    return HttpResponse(json.dumps(data), content_type='application/json')

# API to check existing booking
def android_check_booking(request):
    try:
            user_id=request.GET.get('user_id')
            offer_id=request.GET.get('offer_id')
	
            restaurant_booking_obj = RestaurantBooking.objects.filter(consumer_id=user_id,restaurant_offer_id=offer_id)
            print '===================',restaurant_booking_obj

            if(len(restaurant_booking_obj)>0):
				data = {'message': "Already booked", 'success':'true'}
            else:
				data = {'message': "Not booked", 'success':'false'}

    except MySQLdb.OperationalError, e:
        data = {'message': 'none', 'error_message':'Fail'}
    return HttpResponse(json.dumps(data), content_type='application/json')


        

