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

#--------------------
from django.core.mail import send_mail

SERVER_URL = "http://54.148.82.251"
#SERVER_URL = "http://192.168.0.123:9999"
#SERVER_URL = "http://ec2-52-4-20-173.compute-1.amazonaws.com"

#Reset URL
#RESET_URL = 'http://ec2-52-2-239-162.compute-1.amazonaws.com/reset-password/?rpcid='

# Constants
earth_radius = 6371.0  # for kms
degrees_to_radians = math.pi/180.0
radians_to_degrees = 180.0/math.pi


#API for login
@csrf_exempt
def consumer_login(request):
    #pdb.set_trace()
    try:
        print request.POST 
        json_obj= json.loads(request.body)
        print 'JSON OBJECT : ',json_obj
        if request.method == 'POST':
            user = authenticate(username=json_obj['username'], password= json_obj['password'])
            #user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
            consumer = Consumer.objects.get(username=user)
            print '-------user id---------',consumer.consumer_id

            if consumer is not None:
                if user.is_active:
                    print '================',consumer.consumer_id
                    data= {'success' : 'true', 'message' :'Successful Login', 'user_info' : get_profile_info(consumer.consumer_id)}

                else:
                    data= {'success' : 'false', 'message':'User Is Not Active'}
            else:
                data= {'success' : 'false', 'error_message' :'Invalid Username or Password'}
        else:
            data= {'success' : 'false', 'error_message':'Invalid Request'}
    except User.DoesNotExist:
        print 'usr'
        data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'User Does Not Exist'}
    except MySQLdb.OperationalError, e:
        print e
        data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'Internal server '}
    except Exception, e:
        print e
        data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'Invalid Username or Password'}
    return HttpResponse(json.dumps(data), content_type='application/json')


#API for sign up
@csrf_exempt
def consumer_register(request):
#    pdb.set_trace()
    try:
        print '---request--------------------',request
        json_obj= json.loads(request.body)
        print 'JSON OBJECT : ',json_obj
        consumer_obj = Consumer(
            username=json_obj['email_id'],
            consumer_first_name=json_obj['first_name'],
            consumer_last_name=json_obj['last_name'],
            consumer_email=json_obj['email_id'],
            consumer_contactno=json_obj['phone'],
            apns_token=json_obj['apns_token'],
            sign_up_via=json_obj['sign_up_via'],
            sign_up_source=json_obj['sign_up_source'],
            consumer_image=save_image(json_obj['user_profile_image']),
            consumer_create_by = json_obj['email_id'],
            consumer_create_date = datetime.now(),
            consumer_update_by = json_obj['email_id'],
            consumer_update_date = datetime.now(),
            is_consumer_email_alert='1',
            is_consumer_sms_alert = '1'
            #username=json_obj['email']
            )
        consumer_obj.set_password(json_obj['pass_word'])
        consumer_obj.save()

        if consumer_obj:
            data= {'success' : 'true', 'message':'Successful Sign Up' }
            send_welcome_mail(consumer_obj.username)
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
@csrf_exempt
def customer_login_android(request):
    try:
        print request.POST 
        json_obj= json.loads(request.body)
        print '----------in function--------------'
        print 'JSON OBJECT : ',json_obj
        if request.method == 'POST':
            customer = Consumer.objects.get(consumer_email=json_obj['username'])
            print '-------user id---------',customer.consumer_email

            if customer is not None:
                    data= {'success' : 'true', 'message' :'Successful Login', 'user_info' : get_updated_profile_info_android(customer.consumer_id )}
            else:
                data= {'success' : 'false', 'error_message' :'Invalid Username'}
    except MySQLdb.OperationalError, e:
        print e
        data= {'success' : 'false', 'error_message':'Internal server '}
    except Exception, e:
        print e
        data= {'success' : 'false', 'error_message':'Invalid Username'}
    return HttpResponse(json.dumps(data), content_type='application/json')



#Sign Up via Gmail and Facebook 
@csrf_exempt
def consumer_register_facebook_gmail(request):
#    pdb.set_trace()
    try:
        print '---request--------------------',request
        json_obj= json.loads(request.body)
        print 'JSON OBJECT : ',json_obj
        consumer_obj = Consumer(
            username=json_obj['email_id'],
            consumer_first_name=json_obj['first_name'],
            consumer_last_name=json_obj['last_name'],
            consumer_email=json_obj['email_id'],
            consumer_contactno=json_obj['phone'],
            apns_token=json_obj['apns_token'],
            sign_up_via=json_obj['sign_up_via'],
            sign_up_source=json_obj['sign_up_source'],
            consumer_image=json_obj['user_profile_image'],
            is_consumer_email_alert='0',
            is_consumer_sms_alert = '0'
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
            email= json_obj['email_id']
            print '=========email================',email
            send_welcome_mail(email_id)
        else:
            data= {'success' : 'false', 'message':'Sign Up not Successful'}
    except Consumer.DoesNotExist,e:
        # print "in the main flow"
        data= {'success' : 'false', 'message':str(e)}

    except Exception, e:
        print e
        json_obj= json.loads(request.body)
        email_id=json_obj['email_id']
        data= {'success' : 'login', 'message': 'User Already Exist'}
    return HttpResponse(json.dumps(data), content_type='application/json')


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
            consumer_email=json_obj['email'],
            sign_up_via=json_obj['sign_up_via'],
            sign_up_source=json_obj['sign_up_source'],
            consumer_image=json_obj['user_profile_image'],
            is_consumer_email_alert='1',
            is_consumer_sms_alert = '0'
            )
        consumer_obj.save()


        filename = "IMG_%s_%s.jpg" % (consumer_obj.username, str(datetime.now()).replace('.','_')) # For giving filename to Image
        resource = urllib.urlopen(json_obj['user_profile_image'])

        consumer_obj.consumer_image = ContentFile(resource.read(), filename) # assign image to model
        consumer_obj.save()

        if consumer_obj:
            data= {'success' : 'true', 'message':'Successful Sign Up', 'user_info' : get_updated_profile_info_android(consumer_obj.consumer_id)}
            email= consumer_obj.username
            print '=========email================',email
            send_welcome_mail(email)
        else:
            data= {'success' : 'false', 'message':'Sign Up not Successful'}
    except Consumer.DoesNotExist,e:
        # print "in the main flow"
	print 'customer de\oest nt exist', e
        data= {'success' : 'false', 'message':str(e)}
    except IntegrityError as err:
        print 'Duplicate Record ', err
        json_obj= json.loads(request.body)
        email_id=json_obj['email']
	print 'MB -- > email :',email_id
        data= {'success' : 'true', 'message': 'User Already Sign Up', 'user_info' : get_existing_profile_info_android(email_id)}
	print '-----> for double sing up',data
        return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception, e:
        print e
        json_obj= json.loads(request.body)
        email_id=json_obj['email']
        data= {'success' : 'false', 'message':'Server Error'}
    return HttpResponse(json.dumps(data), content_type='application/json')

# function to get detail if user already exist
def get_existing_profile_info_android(email_id):
    try:
	print 'In Get Profile Function : ',email_id
	consumer_object = Consumer.objects.get(username=email_id)
	data = {
            'user_id'    : str(consumer_object.consumer_id),
            'first_name' : consumer_object.consumer_first_name,
            'user_profile_image' : SERVER_URL + consumer_object.consumer_image.url,
            'email'   : consumer_object.consumer_email,
            'email_alert' : consumer_object.is_consumer_email_alert,
            'sms_alert' : consumer_object.is_consumer_sms_alert
                }
    except Exception,e:
	print 'exception ',e
	data = {}
    return data 
#HttpResponse(json.dumps(data), content_type='application/json')



#-----------------------------------------------
#API for update profile
@csrf_exempt
def update_consumer_profile(request):
    print request
    try:
        json_obj= json.loads(request.body)
        print 'JSON OBJECT : ',json_obj
        if request.method == 'POST':
            consumer_object = Consumer.objects.get(consumer_id=json_obj['user_id'])
            print '======================',consumer_object
            consumer_object.consumer_first_name = json_obj['first_name']
            consumer_object.consumer_last_name = json_obj['last_name']
            consumer_object.consumer_image=save_image(json_obj['user_profile_image'])
            consumer_object.consumer_contactno = json_obj['phone']
            consumer_object.consumer_email = json_obj['email_id']
            consumer_object.consumer_update_by = json_obj['email_id']
            consumer_object.consumer_update_date = datetime.now()
            print '============here=================='
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
def change_password(request):
    try:
        if request.method == 'POST':
            data ={}
        json_obj=json.loads(request.body)
        print 'JSON OBJECT : ',json_obj
        #email=json_obj['email_id']


        user = authenticate(username=json_obj['email_id'], password= json_obj['pass_word'])
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
        data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'User Does Not Exit'}
    except MySQLdb.OperationalError, e:
        print e
        data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'Internal Server Error '}
    except Exception, e:
        print e
        data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'Internal Server Error '}
    return HttpResponse(json.dumps(data), content_type='application/json')

#API for sms alert
@csrf_exempt
def sms_alert_activation(request):
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
def email_alert_activation(request):
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
def consumer_feedback(request):
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
            'email_id'   : consumer_object.username,
            'sign_up_via' : consumer_object.sign_up_via,
            'email_alert' : consumer_object.is_consumer_email_alert,
            'sms_alert' : consumer_object.is_consumer_sms_alert
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

def get_updated_profile_info_android(user_id):
    consumer_object = Consumer.objects.get(consumer_id=user_id)
    data = {
            'user_id'    : str(consumer_object.consumer_id),
            'first_name' : consumer_object.consumer_first_name,
            'user_profile_image' : SERVER_URL + consumer_object.consumer_image.url,
            'email'   : consumer_object.consumer_email,
            'email_alert' : consumer_object.is_consumer_email_alert,
            'sms_alert' : consumer_object.is_consumer_sms_alert
                }
    return data 



@csrf_exempt
def restaurant_list(request):
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

            lon_max, lon_min, lat_max, lat_min = bounding_box(float(consumer_latitude),float(consumer_longitude),40)
            #==============for restaurant=============
            restaurant=Restaurant.objects.filter(restaurant_lat__range=[lat_min,lat_max], restaurant_lon__range=[lon_min,lon_max])
            print '========restaurant================',restaurant
       
            restaurant_offer = Offer_map.objects.filter(restaurant_id__in=restaurant,offer_map_date=date,offer_map_time_from__lt=offfer_time,offer_map_time_to__gt=offfer_time,offer_map_status="1")
            print '==============res offer===============',restaurant_offer

            current_date = datetime.now()

            for offer in restaurant_offer:
                print '=================offer=====================',offer

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

                final_dist = ("%.3f" % final_dist)                 
                restaurant_distance = "{0:0.1f}".format(float(final_dist)) + " " + "km"

		restaurant_image = SERVER_URL + str(offer.restaurant_id.restaurant_image.url)
                restaurant_offer_detail = offer.restaurant_offer_id.restaurant_offer_detail
                
                # function to get restaurant cuisine
                cuisine_object = CuisineRestaurentMap.objects.filter(restaurant_id=offer.restaurant_id)
                print '========    hi ===========',cuisine_object
                if(len(str(cuisine_object))>0):   
                    cuisine_type_list = []
                    for cuisine_obj in cuisine_object:
                        cuisine_type = cuisine_obj.cuisine_id.fact_cuisine
                        print '============type================',cuisine_type
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

            restaurant_offer1 = Offer_map.objects.filter(restaurant_id__in=restaurant_id_list1,offer_map_date=date, offer_map_time_from__lt= offfer_time,offer_map_time_to__gt= offfer_time,offer_map_status="1")

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

                    restaurant_id = "RestaurantBranch " + str(branch1.restaurant_branch_id)
                    
                    cuisine_object = CuisineRestaurentBranchMap.objects.filter(restaurant_branch_id=branch1.restaurant_branch_id)
                    print '==========cuisine===========',cuisine_object
                    if(len(cuisine_object)>0):   
                        cuisine_type_list = []
                        for cuisine_obj in cuisine_object:
                            cuisine_type = cuisine_obj.cuisine_id.fact_cuisine
                            cuisine_type_list.append(str(cuisine_type))
                    else:
                        cuisine_type_list = []

                    consumer_position = (consumer_latitude,consumer_longitude)
                    restaurant_position = (branch1.restaurant_branch_lat,branch1.restaurant_branch_lon)
                    dist = vincenty(consumer_position, restaurant_position).meters
                    final_dist = dist/1000
                    final_dist = ("%.3f" % final_dist)
		    restaurant_distance = "{0:0.1f}".format(float(final_dist)) + " " + "km"

                    tpl={ 'restaurantId' :restaurant_id, 'offer' : restaurant_offer_detail, 'restaurantname' : restaurant_name,  'location' : restaurant_area, 'cuisine' : cuisine_type_list, 'distance' : restaurant_distance, 'image' : restaurant_image, 'longitude' : restaurant_longitude, 'latitude' : restaurant_latitude}
                tpl1.append(tpl)
        print '===============tpl1========================',tpl1        
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
def forgot_password(request):
    #pdb.set_trace()
    #gmail_user = "admin@deal-monk.com"
    #gmail_pwd = "info9910128745"
    
    gmail_user = "training.tungsten@gmail.com"
    gmail_pwd = "team@tungsten74#"
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
            TEXT = """Dear Customer,  
                    Your account information is :
                    Sign In Email Address: %s
                    Password: %s

                If you did not request this, you can safely ignore this email. Rest
                assured your customer account is safe.

                DealMonk will never e-mail you and ask you to disclose or verify your
                DealMonk password, credit card, or banking account number. If you
                receive a suspicious e-mail with a link to update your account
                information, do not click on the link--instead, report the e-mail to
                DealMonk for investigation. Greetings from DealMonk.
                """ % (user, password)
            
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
# API for my deal
@csrf_exempt
def upcoming_deal(request):
#    pdb.set_trace()
    try:
        if request.method == 'POST':
            json_obj=json.loads(request.body)
            tpl1 =[]
            tpl = []
            print 'JSON OBJECT : ',json_obj

            user_id=json_obj['user_id']
            date = json_obj['date']

            booking_object = RestaurantBooking.objects.filter(consumer_id = user_id,restaurant_booking_date__gte = date).order_by('-restaurant_booking_time_from')
            print '---------------- booking_object-------------',booking_object

            for booking in booking_object:
                id = booking.restaurant_id
                print '===============id=============',id
                if(id!=None):
                    status = booking.restaurant_booking_status
                    print '====status================',status
                    if(status=="Confirmed"):
                        id = "Restaurant " + str(booking.restaurant_id)
                        name = booking.restaurant_id.restaurant_name
                        date = booking.restaurant_booking_date
                        start_time = booking.restaurant_booking_time_from.strftime("%I:%M %p")
                        end_time = booking.restaurant_booking_time_to.strftime("%I:%M %p")
                        booking_status = booking.restaurant_booking_status
                        location = booking.restaurant_id.restaurant_area
                        booking_id = str(booking.restaurant_booking_id)
                        offer_id = str(booking.restaurant_offerMap_id)[3:]
                        image = SERVER_URL + str(booking.restaurant_id.restaurant_image.url)
                        coupon = " " 
                        status = booking.restaurant_booking_status
                        print '============in function================='
                        
                        offer = booking.restaurant_offerMap_id.restaurant_offer_id.restaurant_offer_detail
                        print '============in function 11111111================='

                        contact = booking.restaurant_id.restaurant_contactno
                        print '===============tpl============================='
                        tpl={ 'contact' : contact,'couponCode' : coupon,'status' : status,'offerStartTime' : str(start_time), 'offerEndTime' : str(end_time),'restaurantName' : name, 'restaurantId' : str(id), 'offerID' : offer_id,  'offerName' : offer, 'restaurantArea' : location, 'bookingDate' : str(date), 'restaurantImage' : image, 'booking_id' : booking_id }
                        print '==========tpl====================',tpl
                        i = 0
                        print '=======================',i+1
                        tpl1.append(tpl)
                    #print '=================tpl1==================',tpl1
                    
       
                else:
                    status = booking.restaurant_booking_status
                    "==============hi i am here======================"
                    if(status=="Confirmed"):   
                        id = "RestaurantBranch " + str(booking.restaurant_branch_id)
                        name = booking.restaurant_branch_id.restaurant_branch_name
                        date = booking.restaurant_booking_date
                        start_time = booking.restaurant_booking_time_from.strftime("%I:%M %p")
                        end_time = booking.restaurant_booking_time_to.strftime("%I:%M %p")
                        status = booking.restaurant_booking_status
                        location = booking.restaurant_branch_id.restaurant_branch_area
                        booking_id = str(booking.restaurant_booking_id)

                        offer_id = str(booking.restaurant_offerMap_id)[3:]
                        image = SERVER_URL + str(booking.restaurant_branch_id.restaurant_id.restaurant_image.url)
                        status = booking.restaurant_booking_status
                        coupon = " "  
                        offer = booking.restaurant_offerMap_id.restaurant_offer_id.restaurant_offer_detail
                        contact = booking.restaurant_branch_id.restaurant_branch_contact

                        tpl={ 'contact' : contact,'couponCode' : coupon, 'status' : status,'offerStartTime' : str(start_time), 'offerEndTime' : str(end_time), 'restaurantName' : name, 'restaurantId' : str(id), 'offerID' : offer_id, 'offerName' : offer, 'restaurantArea' : location, 'bookingDate' : str(date), 'restaurantImage' : image, 'booking_id' : booking_id }
                        tpl1.append(tpl)
                print '======================hi ====================',tpl1
            data = {'nameList': tpl1, 'success':'true'}
   
    except:
        data = {'BranchList': 'none', 'error_message':'Deals not available'}
    return HttpResponse(json.dumps(data), content_type='application/json')


# API for all deals
@csrf_exempt
def all_deal(request):
#    pdb.set_trace()
    try:
        if request.method == 'POST':
            json_obj=json.loads(request.body)
            tpl1 =[]
            print 'JSON OBJECT : ',json_obj

            user_id=json_obj['user_id']

            booking_object = RestaurantBooking.objects.filter(consumer_id = user_id).order_by('-restaurant_booking_date')
            print '---------------- booking_object-------------',booking_object

            for booking in booking_object:
                id = booking.restaurant_id
                if(id!=None):
                    print "===============here=======================" 
                    id = "Restaurant " + str(booking.restaurant_id)
                    name = booking.restaurant_id.restaurant_name
                    print "===============here=======================" 
                    booking_id = str(booking.restaurant_booking_id)

                    date = booking.restaurant_booking_date
                    start_time = booking.restaurant_booking_time_from.strftime("%I:%M %p")
                    print "===============here=======================" 

                    end_time = booking.restaurant_booking_time_to.strftime("%I:%M %p")
                    booking_status = booking.restaurant_booking_status
                    location = booking.restaurant_id.restaurant_area
                    print "===============here=======================" 

                    offer_id = str(booking.restaurant_offerMap_id)[3:]
                    print "===============here=======================" 

                    image = SERVER_URL + str(booking.restaurant_id.restaurant_image.url)
                    status = booking.restaurant_booking_status
                    print '=========status===============',status
                    if(status=="Confirmed"):
                        coupon = ""
                    else:
                        coupon = booking.consumer_coupon_code    
                    offer = booking.restaurant_offerMap_id.restaurant_offer_id.restaurant_offer_detail
                    print "===============here12=======================",offer 

                    contact = booking.restaurant_id.restaurant_contactno
                    #tpl={ 'contact' : contact,'couponCode' : coupon, 'status' : status,'offerStartTime' : str(start_time), 'offerEndTime' : str(end_time), 'restaurantName' : name, 'restaurantId' : str(id), 'offerID' : str(offer_id), 'offerName' : offer, 'restaurantArea' : location, 'bookingDate' : str(date), 'restaurantImage' : image }
                   # print '=================tpl=========================',tpl

                else:
                    id = "RestaurantBranch " + str(booking.restaurant_branch_id)
                    name = booking.restaurant_branch_id.restaurant_branch_name
                    date = booking.restaurant_booking_date
                    start_time = booking.restaurant_booking_time_from
                    end_time = booking.restaurant_booking_time_to
                    booking_status = booking.restaurant_booking_status
                    location = booking.restaurant_branch_id.restaurant_branch_area
                    booking_id = str(booking.restaurant_booking_id)

                    offer_id = str(booking.restaurant_offerMap_id)[3:]
                    image = SERVER_URL + str(booking.restaurant_branch_id.restaurant_id.restaurant_image.url)
                    status = booking.restaurant_booking_status
                    if(status=="Confirmed"):
                        coupon = ""
                    else:
                        coupon = booking.consumer_coupon_code    
                    offer = booking.restaurant_offerMap_id.restaurant_offer_id.restaurant_offer_detail
                    contact = booking.restaurant_branch_id.restaurant_branch_contact

                    
                tpl={ 'contact' : contact,'couponCode' : coupon, 'status' : status,'offerStartTime' : str(start_time), 'offerEndTime' : str(end_time), 'restaurantName' : name, 'restaurantId' : str(id), 'offerID' : offer_id, 'offerName' : offer, 'restaurantArea' : location, 'bookingDate' : str(date), 'restaurantImage' : image, 'booking_id' : booking_id }
                print '=====================tpl======================',tpl
                tpl1.append(tpl)
            data = {'nameList': tpl1, 'success':'true'}
   
    except:
        data = {'BranchList': 'none', 'error_message':'Deals not available'}
    return HttpResponse(json.dumps(data), content_type='application/json')





# This method is for filtering the product details shown in catalog page.
@csrf_exempt
def searchRestaurantBranch(request):
    try:
        json_obj= json.loads(request.body)
        consumer_latitude=json_obj['latitude']
        consumer_longitude=json_obj['longitude']
        date=json_obj['Date']
        tpl1 = []
        filter_args={}
        filter_restaurant_args_name={}
        filter_restaurant_branch_args={}
        filter_offer_start_time_args={}
        filter_offer_end_time_args={}
        filter_restaurant_args1={}
        filter_restaurant_branch_args={}
        filter_cuisine_args={}
        filter_branch_cuisine_args={}
        filter_restaurant_args_city={}
        filter_restaurant_args_area={}
        filter_restaurant_args_address={}
        

        vNameStatus=0
        vname=""
        test = ''

        #pdb.set_trace()
        if json_obj.get('Location') and len(consumer_longitude)>0:
            print '=========here==================='
            filter_restaurant_args_area['restaurant_area__icontains'] = json_obj['Location'].strip()
           # filter_restaurant_args['restaurant_city__icontains'] = json_obj['Location']
            test = '0'

        if json_obj.get('Location') and len(consumer_longitude)>0:
            print '=========here==================='
            filter_restaurant_args_address['restaurant_addr1__icontains'] = json_obj['Location'].strip()
           # filter_restaurant_args['restaurant_city__icontains'] = json_obj['Location']
            test = '0'



        if json_obj.get('Location') and len(consumer_longitude)>0:
            filter_restaurant_args_city['restaurant_city__icontains'] = json_obj['Location'].strip()
            test = '0'

        if json_obj.get('RestaurantName'):
            restaurant_name = json_obj['RestaurantName'].strip()
            filter_restaurant_args_name['restaurant_name__icontains'] = json_obj['RestaurantName'].strip()
            test = test+'1'
        
        restaurant_id_list1 = []
        if json_obj.get('Cuisine') and len(consumer_longitude)>0:
            test = test+'2'
            filter_cuisine_args['fact_cuisine__icontains']=json_obj['Cuisine'].strip()


            #cuisine_obj = CuisineFactTable.objects.filter(Q(**filter_cuisine_args))
            cuisine_obj = CuisineFactTable.objects.filter((Q(fact_id__in=CuisineFactTable.objects.filter(Q(**filter_cuisine_args)))))
            print '-----------cuisine_obj-----------------------------',cuisine_obj
            cuisine_map_obj = CuisineRestaurentMap.objects.filter((Q(cuisine_id__in=cuisine_obj)))
            print '=====cuisine_map_obj======',cuisine_map_obj

            #print '=========cuisine_map_obj========',cuisine_map_obj
            if(len(cuisine_map_obj)>0):
                for map_obj in cuisine_map_obj:
                    restaurant_id = str(map_obj.restaurant_id)

                    restaurant_id_list1.append(restaurant_id)
             
        #pdb.set_trace()
        if test == '0':
            print '============0====================='
            restaurant_offer_search = Restaurant.objects.filter( Q(restaurant_id__in= Restaurant.objects.filter(Q(**filter_restaurant_args_area) | Q(**filter_restaurant_args_city) | Q(**filter_restaurant_args_address))))

        if test == '1':
            print '============1====================='
            restaurant_offer_search = Restaurant.objects.filter( Q(restaurant_id__in= Restaurant.objects.filter(Q(**filter_restaurant_args_name))))


        if test == '2':
            print '============2====================='
            restaurant_offer_search = Restaurant.objects.filter( Q(restaurant_id__in = restaurant_id_list1))


        if test == '01':
            print '============01====================='
            restaurant_offer_search = Restaurant.objects.filter( Q(restaurant_id__in= Restaurant.objects.filter(Q(**filter_restaurant_args_area) | Q(**filter_restaurant_args_address) | Q(**filter_restaurant_args_city))) & Q(restaurant_id__in= Restaurant.objects.filter(Q(**filter_restaurant_args_name)) ))

        if test == '02':
            print '============02====================='
            restaurant_offer_search = Restaurant.objects.filter( Q(restaurant_id__in= Restaurant.objects.filter(Q(**filter_restaurant_args_area) | Q(**filter_restaurant_args_address) | Q(**filter_restaurant_args_city))) & Q(restaurant_id__in = restaurant_id_list1))

        
        if test == '12':
            print '============12====================='
            restaurant_offer_search = Restaurant.objects.filter( Q(restaurant_id__in= Restaurant.objects.filter(Q(**filter_restaurant_args_name) )) & Q(restaurant_id__in = restaurant_id_list1))
 
        
        elif test == '012':
            print '============012====================='
            restaurant_offer_search = Restaurant.objects.filter( Q(restaurant_id__in= Restaurant.objects.filter(Q(**filter_restaurant_args_area) | Q(**filter_restaurant_args_address) | Q(**filter_restaurant_args_city))) & Q(restaurant_id__in= Restaurant.objects.filter(Q(**filter_restaurant_args_name))) & Q(restaurant_id__in = restaurant_id_list1))

        for offer in restaurant_offer_search:

            restaurant_id = "Restaurant " + str(offer.restaurant_id)

            restaurant_name = offer.restaurant_name

            restaurant_area = offer.restaurant_area

            cuisine_object = CuisineRestaurentMap.objects.filter(restaurant_id=offer.restaurant_id)

            cuisine_type_list = []
            for cuisine_obj in cuisine_object:
                cuisine_type = cuisine_obj.cuisine_id.fact_cuisine
                cuisine_type_list.append(str(cuisine_type))

            restaurant_image = SERVER_URL + str(offer.restaurant_image.url)

            restaurant_latitude = str(offer.restaurant_lat)[:8]

            restaurant_longitude = str(offer.restaurant_lon)[:8]


            if(len(consumer_latitude)>0):
                consumer_position = (consumer_latitude,consumer_longitude)
                restaurant_position = (offer.restaurant_lat,offer.restaurant_lon)
                dist = vincenty(consumer_position, restaurant_position).meters
                final_dist = dist/1000
                final_dist = ("%.3f" % final_dist) 
                restaurant_distance = "{0:0.1f}".format(float(final_dist)) + " " + "km"
            
	    else:
                restaurant_distance = "Distance not available"


            #restaurant_offer_detail = offer.restaurant_offer_id.restaurant_offer_detail

            
            offer_obj = Offer_map.objects.filter(restaurant_id=offer.restaurant_id,offer_map_date=json_obj['Date'],offer_map_time_from__lt=json_obj['current_time'],offer_map_time_to__gt=json_obj['current_time'],offer_map_status="1")
            print '=================offer_obj=============================',offer_obj

            current_time = json_obj['current_time']
            print '=================offer_obj=============================',offer_obj
            if(len(offer_obj)>0):
                for obj in offer_obj:
                    time = str(obj.offer_map_time_to)
                    duration = (dt.datetime.strptime(time, '%H:%M:%S')-dt.datetime.strptime(current_time, '%H:%M:%S')).seconds/60
                    if(duration>=15):                    
                        restaurant_offer_detail = obj.restaurant_offer_id.restaurant_offer_detail
                    else:
                        restaurant_offer_detail = "No Live Deals"
    
            else:
                restaurant_offer_detail = "No Live Deals"

            tpl={ 'restaurantId' : restaurant_id, 'offer' : restaurant_offer_detail, 'restaurantname' : restaurant_name, 'location' : restaurant_area, 'cuisine' : cuisine_type_list,'image' : restaurant_image, 'distance' : restaurant_distance, 'longitude' : restaurant_longitude, 'latitude' : restaurant_latitude}
            tpl1.append(tpl)
        data = {'nameList': tpl1, 'success':'true'}
    except MySQLdb.OperationalError, e:
        data = {'BranchList': 'none', 'error_message':'Mydeals list Fail'}
    return HttpResponse(json.dumps(data), content_type='application/json')


 # This method is for filtering the product details shown in catalog page.

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
@csrf_exempt
def restaurant_view_list(request):
#    pdb.set_trace()
    nameList=[]
    try:
        data = []
        json_obj= json.loads(request.body)
        restaurant_id=json_obj['restaurant_id']
        identifier = restaurant_id.split( )[0]
        id = restaurant_id.split( )[1]

        offer_time=json_obj['time']
        print '=========offer time================',offer_time
        offer_date=json_obj['date']
        print '=========offer_date================',offer_date
        if (identifier=="Restaurant"):
            print '=============in function1=============='
            tpl = restaurant_offer(id,offer_time,offer_date)
            restaurant_object = Restaurant.objects.get(restaurant_id=id)
            data = {     
               'restaurant_address1' : str(restaurant_object.restaurant_addr1), 
                'restaurant_address2' : str(restaurant_object.restaurant_addr2),
                'restaurant_area' : str(restaurant_object.restaurant_area) + "," + str(restaurant_object.restaurant_city),
                'restaurant_image' : SERVER_URL + str(restaurant_object.restaurant_image.url),
                'restaurant_name' : restaurant_object.restaurant_name,
                'restaurant_contact_detail' : restaurant_object.restaurant_contactno, 
                'restaurantOfferList': tpl, 
                'success':'true'}

        else:
            print '=============in function2=============='
            tpl = restaurant_branch_offer(id,offer_time,offer_date)
            restaurant_object = RestaurantBranch.objects.get(restaurant_branch_id=id)

            data = {     
            'restaurant_address1' : str(restaurant_object.restaurant_branch_address1), 
            'restaurant_address2' : str(restaurant_object.restaurant_branch_address2),
            'restaurant_area' : str(restaurant_object.restaurant_branch_area) + "," + str(restaurant_object.restaurant_branch_city),
            'restaurant_image' : SERVER_URL + str(restaurant_object.restaurant_id.restaurant_image.url),
            'restaurant_name' : restaurant_object.restaurant_branch_name,
            'restaurant_contact_detail' : restaurant_object.restaurant_branch_contact,
            'restaurantOfferList': tpl, 
            'success':'true'
            }
                            
    except MySQLdb.OperationalError, e:
        data = {'nameList': tpl, 'success':'true'}
    return HttpResponse(json.dumps(data), content_type='application/json')

# function for restaurant offer view
def restaurant_offer(id,offer_time,offer_date):
    
    tpl1 = []
    
    restaurant_offer = Offer_map.objects.filter(restaurant_id=id,offer_map_time_to__gt= offer_time,offer_map_date=offer_date,offer_map_status="1").order_by('offer_map_time_from')
    print '------res offer---',restaurant_offer
    if(len(restaurant_offer)>0):
        for offer in restaurant_offer:
            print '-in function res--------',offer
            time = str(offer. offer_map_time_to)
            duration = (dt.datetime.strptime(time, '%H:%M:%S')-dt.datetime.strptime(offer_time, '%H:%M:%S')).seconds/60
            print '=========duration=====',duration
            if(duration>=15):

                restaurant_offer_detail = offer.restaurant_offer_id.restaurant_offer_detail

                restaurant_offer_id = str(offer.offer_map_id)
                
                restaurant_offer_start_time = offer.offer_map_time_from.strftime("%I:%M %p")

                restaurant_offer_end_time = offer.offer_map_time_to.strftime("%I:%M %p")
            
                #converted_time = offer.offer_map_time_to.hour
                time = str(restaurant_offer_start_time) + " - " + str(restaurant_offer_end_time)
        
                tpl={'restaurant_offer' : restaurant_offer_detail, 'offer_id' : restaurant_offer_id, 'start_time' : restaurant_offer_start_time, 'end_time' : restaurant_offer_end_time }
                print '=======================',tpl
        
                tpl1.append(tpl)
        return tpl1
    else:
        tpl = {}
        return tpl

# function for restaurant branch offer view
def restaurant_branch_offer(id,offer_time,offer_date):
    tpl1 = []
    print '============here==================='
    restaurant_branch = RestaurantBranch.objects.filter(restaurant_branch_id = id)
    print '------------in function res branch----------',restaurant_branch
    for branch in restaurant_branch:
        res_id = branch.restaurant_id


    restaurant_offer = Offer_map.objects.filter(restaurant_id=res_id,offer_map_time_to__gt= offer_time,offer_map_date=offer_date,offer_map_status="1").order_by('offer_map_time_from')
    print '------------offer1----------',restaurant_offer

    if(len(restaurant_offer)>0):
        for offer in restaurant_offer:
            print '-offer---------',offer
            time = str(offer.offer_map_time_to)
            duration = (dt.datetime.strptime(time, '%H:%M:%S')-dt.datetime.strptime(offer_time, '%H:%M:%S')).seconds/60
            if(duration>=15):
                print '-----------in function 2---------------'
                branch_object = RestaurantBranch.objects.filter(restaurant_id=offer.restaurant_id,restaurant_branch_id__in=restaurant_branch)
                print '---------obj------',branch_object 
                for branch in branch_object:

                    restaurant_offer_detail = offer.restaurant_offer_id.restaurant_offer_detail
                    
                    restaurant_offer_id = str(offer.restaurant_offer_id)
                    
                    restaurant_offer_start_time = offer.offer_map_time_from.strftime("%I:%M %p")
                    
                    restaurant_offer_end_time = offer.offer_map_time_to.strftime("%I:%M %p")
                
                    #converted_time = offer.offer_map_time_to.hour
                    time = str(restaurant_offer_start_time) + "-" + str(restaurant_offer_end_time)
                    
                    tpl={'restaurant_offer' : restaurant_offer_detail, 'offer_id' : restaurant_offer_id, 'start_time' : restaurant_offer_start_time, 'end_time' : restaurant_offer_end_time }
                    tpl1.append(tpl)
        return tpl1
    else:
            tpl = {}
            return tpl

@csrf_exempt
def book_restaurant(request):
#    pdb.set_trace()

    nameList=[]
    try:
        json_obj=json.loads(request.body)
        print '==========json_obj===============',json_obj
        data = {}
        restaurant_id=json_obj['restaurantId']
        identifier = restaurant_id.split( )[0]
        id = restaurant_id.split( )[1]
        if(identifier=="Restaurant"):
            offer_obj = Offer_map.objects.get(offer_map_id=json_obj['offer_id'])
            start_time = offer_obj.offer_map_time_from
            end_time = offer_obj.offer_map_time_to                
            consumer=Consumer.objects.get(consumer_id=json_obj['user_id'])
            restaurant = Restaurant.objects.get(restaurant_id=id)
            booking_obj = RestaurantBooking(
            restaurant_booking_date=json_obj['booking_date'],
            restaurant_booking_time_from=start_time,
            restaurant_booking_time_to=end_time,
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
            booking_obj.consumer_id=Consumer.objects.get(consumer_id=json_obj['user_id'])
            booking_obj.restaurant_id=Restaurant.objects.get(restaurant_id=id)
            #booking_obj.restaurant_offer_id=RestaurantOffer.objects.get(restaurant_offer_id=json_obj['offer_id'])  

            booking_obj.restaurant_offerMap_id=offer_obj

            booking_obj.consumer_coupon_code=checkin_no
            print '=========hi=========================='

            booking_obj.save()
            # define parameters for email

            email = consumer.consumer_email

            offer = offer_obj.restaurant_offer_id.restaurant_offer_detail

            restaurantname = restaurant.restaurant_name
            time = str(start_time) + " to " +str(end_time)
            #if(consumer.is_consumer_email_alert==1):
                #send_booking_confirmation_mail(email,offer,restaurantname,time)

            if(consumer.is_consumer_email_alert=="1"):
                print '===========call maikl sending function==============='
                send_booking_confirmation_mail(email,offer,restaurantname,time)

            # define parameters for res email
            #res_email = restaurant.owner_id.owner_email
            # name = str(consumer.consumer_first_name) + str(consumer.consumer_last_name)
            #contact = consumer.consumer_contactno
            #covers = str(json_obj['covers'])
            #send_booking_confirmation_mail_restaurant(res_email,offer, name, contact, covers, time)
            res_email = restaurant.restaurant_admin_id.restaurant_admin_email
            name = str(consumer.consumer_first_name) + str(consumer.consumer_last_name)
            contact = consumer.consumer_contactno
            covers = str(json_obj['covers'])
            send_booking_confirmation_mail_restaurant(res_email,offer, name, contact, covers, time)

            if booking_obj:
                data= {'success' : 'true', 'message':'Booking Saved Successfully','booking_id' : str(booking_obj.restaurant_booking_id)}
            else:
                data= {'success' : 'false', 'message':'Booking Not Saved Successfully'}
        else:
                offer_obj = Offer_map.objects.get(offer_map_id=json_obj['offer_id'])
                start_time = offer_obj.offer_map_time_from
                end_time = offer_obj.offer_map_time_to
                consumer=Consumer.objects.get(consumer_id=json_obj['user_id'])
                restaurant_branch = RestaurantBranch.objects.get(restaurant_branch_id=id)
                booking_obj = RestaurantBooking(
                    restaurant_booking_date=json_obj['booking_date'],
                    restaurant_booking_time_from=start_time,
                    restaurant_booking_time_to=end_time,
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
                #booking_obj.restaurant_offer_id=RestaurantOffer.objects.get(restaurant_offer_id=json_obj['offer_id'])  
                booking_obj.consumer_coupon_code=checkin_no
                booking_obj.restaurant_offerMap_id=offer_obj

                # define parameters for email
                email = consumer.consumer_email
                offer = offer_obj.restaurant_offer_id.restaurant_offer_detail
                restaurantname = restaurant_branch.restaurant_branch_name
                time = str(start_time) + " to " +str(end_time)
                if(consumer.is_consumer_email_alert==1):
                    send_booking_confirmation_mail(email,offer,restaurantname,time)
                
                #res_email = restaurant_branch.owner_id.owner_email
                name = str(consumer.consumer_first_name) + str(consumer.consumer_last_name)
                contact = consumer.consumer_contactno
                covers = json_obj['covers']
                #send_booking_confirmation_mail_restaurant(res_email,offer, name, contact, covers, time)                
                    

                booking_obj.save()
                if booking_obj:
                    data= {'success' : 'true', 'message':'Booking Saved Successfully','booking_id' : booking_obj.restaurant_booking_id}
                else:
                    data= {'success' : 'false', 'message':'Booking Not Saved Successfully'}

    except MySQLdb.OperationalError, e:
        data = {'nameList': data, 'success':'true'}
    return HttpResponse(json.dumps(data), content_type='application/json')

# API for checkin
@csrf_exempt
def booking_list(request):
#    pdb.set_trace()
    data = {}

    nameList=[]
    try:
        if request.method == 'POST':
            print '===========',request
            json_obj=json.loads(request.body)
            print '=============json_obj================',json_obj
            data1 = []
            consumer_latitude=json_obj['latitude']
            consumer_longitude=json_obj['longitude']
            current_time = json_obj['time']
            date = json_obj['date']
            user_id = json_obj['user_id']

            #lon_max, lon_min, lat_max, lat_min = bounding_box(float(consumer_latitude),float(consumer_longitude),0.5)
            #restaurant_booking_obj = RestaurantBooking.objects.filter(consumer_id=user_id,restaurant_booking_date=date,restaurant_booking_time_from__lt=current_time,restaurant_booking_time_to__gt=current_time)
            #res_obj = Restaurant.objects.filter(restaurant_lat__range=[lat_min,lat_max], restaurant_lon__range=[lon_min,lon_max])
            #restaurant_id_list = []
            #for obj in res_obj:
                #restaurant_id = obj.restaurant_id
                #restaurant_id_list.append(str(restaurant_id))
                        
            restaurant_booking_obj = RestaurantBooking.objects.filter(consumer_id=user_id,restaurant_booking_date=date,restaurant_booking_time_from__lt=current_time,restaurant_booking_time_to__gt=current_time)
                        
            if(len(restaurant_booking_obj)>0):
                for obj in restaurant_booking_obj:
                    status = obj.restaurant_booking_status
                    if(status=="Confirmed"):
                        restaurant_id = "Restaurant " + str(obj.restaurant_id)
                        restaurant_name = obj.restaurant_id.restaurant_name
                        booking_id = str(obj.restaurant_booking_id)
                        offer_id = str(obj.restaurant_offerMap_id)[3:]
                        data = {'restaurant_id' : restaurant_id,'restaurant_name' : restaurant_name, 'offer_id' : offer_id, 'booking_id' : booking_id}
                        data1.append(data)
                        
            # ==================for restaurant branch =========================  
            
            #res_branch_obj = RestaurantBranch.objects.filter(restaurant_branch_lat__range=[lat_min,lat_max], restaurant_branch_lon__range=[lon_min,lon_max])
            #restaurant_branch_id_list = []
            #print '====================res_branch_obj====================',res_branch_obj
            #for obj in res_branch_obj:
                #restaurant_id = obj.restaurant_branch_id
                #restaurant_branch_id_list.append(str(restaurant_id))
            
            #restaurant_branch_booking_obj = RestaurantBooking.objects.filter(restaurant_branch_id__in=restaurant_branch_id_list,consumer_id=user_id,restaurant_booking_date=date,restaurant_booking_time_from__lt=current_time,restaurant_booking_time_to__gt=current_time)
#            restaurant_branch_booking_obj = RestaurantBooking.objects.filter(consumer_id=user_id,restaurant_booking_date=date,restaurant_booking_time_from__lt=current_time,restaurant_booking_time_to__gt=current_time)            
#            print '====================restaurant_branch_booking_obj==================',restaurant_branch_booking_obj
#
#                        
#            if(len(restaurant_branch_booking_obj)>0):
#                print '============here================='
#
#                for obj in restaurant_branch_booking_obj:
#                    status = obj.restaurant_booking_status
#                    if(status=="Confirmed"):
#                        restaurant_id = "RestaurantBranch " + str(obj.restaurant_branch_id)
#                        restaurant_name = obj.restaurant_branch_id.restaurant_id.restaurant_name
#                        booking_id = obj.restaurant_booking_id
#
#                        offer_id = str(obj.restaurant_offerMap_id)[3:]
#                        data = {'restaurant_id' : restaurant_id, 'restaurant_name' : restaurant_name, 'offer_id' : offer_id, 'booking_id' : booking_id}
#                        print '================hiiiiiiiiiiiiiii===================',data
#                        data1.append(data)
            if(len(data)>0):
                data = {'data': data1, 'success':'true'}
            else:
               data = {'data': "Please book a deal first", 'success':'false'}    
            print '===================data==========================',data       
                
    except MySQLdb.OperationalError, e:
            data = {'message': 'Checkin Fail', 'success':'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')



# API for checkin
@csrf_exempt
def checkin(request):
#    pdb.set_trace()

    nameList=[]
    try:   
        if request.method == 'POST':
            json_obj=json.loads(request.body)
            print '========================',json_obj
            user_id = json_obj['user_id']
            restaurant_id = json_obj['restaurantId']
            offer_id = json_obj['offer_id']
            consumer_latitude = json_obj['latitude']
            consumer_longitude = json_obj['longitude']
            identifier = restaurant_id.split( )[0]
            id = restaurant_id.split( )[1]
            lon_max, lon_min, lat_max, lat_min = bounding_box(float(consumer_latitude),float(consumer_longitude),0.5)

            if(identifier=="Restaurant"):  
                
                restaurant_booking_obj = RestaurantBooking.objects.get(restaurant_offerMap_id=offer_id,consumer_id=user_id,restaurant_id=id)  
                print '===============restaurant_booking_obj===================',restaurant_booking_obj
              
                res_obj = Restaurant.objects.filter(restaurant_id=id,restaurant_lat__range=[lat_min,lat_max], restaurant_lon__range=[lon_min,lon_max])          
                print '=============res_obj===============',len(res_obj)
                if(len(res_obj)>0):                
                    restaurant_booking_obj.restaurant_booking_status="Fulfilled"
                    restaurant_booking_obj.restaurant_checkin_status="1"
                    coupone_code = restaurant_booking_obj.consumer_coupon_code
                    print '=======coupone_code=====',coupone_code        
                    coupon_number = str(coupone_code)
                    restaurant_name = restaurant_booking_obj.restaurant_id.restaurant_name
                    time = str(restaurant_booking_obj.restaurant_booking_time_from.strftime("%I:%M %p")) + " to " + str(restaurant_booking_obj.restaurant_booking_time_to.strftime("%I:%M %p"))  
                    offer_detail = restaurant_booking_obj.restaurant_offerMap_id.restaurant_offer_id.restaurant_offer_detail
                    data = {'message':{'restaurantname' : restaurant_name, 'time' : time, 'offer' : offer_detail, 'coupon_number' : coupon_number}, 'success' : 'true'}
                    restaurant_booking_obj.save()
                    consumer = Consumer.objects.get(consumer_id=json_obj['user_id'])

                    # if(consumer.is_consumer_email_alert==1):
                       # send_checkin_mail(user_id)
                    if(consumer.is_consumer_email_alert=="1"):
                        print '=======send mail=============='
                        send_checkin_mail(user_id)


                    res_email = restaurant_booking_obj.restaurant_id.restaurant_admin_id.restaurant_admin_email
                    name = str(consumer.consumer_first_name) + str(consumer.consumer_last_name)
                    contact = consumer.consumer_contactno
                    covers = restaurant_booking_obj.restaurant_booking_covers
                    send_checkin_mail_restaurant(res_email,offer_detail, name, contact, covers, time)


                else :
                    data = {'message': 'For checkin you should be in range of 500 meters', 'success':'false'}
            else:    
                restaurant_booking_obj = RestaurantBooking.objects.get(restaurant_offer_id=offer_id,consumer_id=user_id,restaurant_branch_id=id)
                branch_obj = RestaurantBranch.objects.filter(restaurant_branch_id=id,restaurant_branch_lat__range=[lat_min,lat_max], restaurant_branch_lon__range=[lon_min,lon_max])          
                if(len(res_obj)>0):                

                    restaurant_booking_obj.restaurant_booking_status="Fullfilled"
                    coupone_code = restaurant_booking_obj.consumer_coupon_code
                    restaurant_booking_obj.restaurant_checkin_status="1"
                    coupon_number = str(coupone_code)
                    restaurant_name = restaurant_booking_obj.restaurant_branch_name
                    time = str(restaurant_booking_obj.restaurant_booking_time_from.strftime("%I:%M %p")) + " to " + str(restaurant_booking_obj.restaurant_booking_time_to.strftime("%I:%M %p"))  
                   
                    offer_detail = restaurant_booking_obj.restaurant_offerMap_id.restaurant_offer_id.restaurant_offer_detail

                    data = {'message':{'restaurantname' : restaurant_name, 'time' : time, 'offer' : offer_detail, 'coupon_number' : coupon_number}, 'success' : 'true'}
                    restaurant_booking_obj.save()
                    send_checkin_mail(user_id)
                    # define parameters for checkin
                    consumer = Consumer.objects.get(consumer_id=json_obj['user_id'])

                    if(consumer.is_consumer_email_alert==1):
                        send_checkin_mail(user_id)

                    #res_email = restaurant_booking_obj.restaurant_branch_id.owner_id.owner_email
                    name = str(consumer.consumer_first_name) + str(consumer.consumer_last_name)
                    contact = consumer.consumer_contactno
                    covers = restaurant_booking_obj.restaurant_booking_covers                   
                    #send_checkin_mail_restaurant(res_email,offer_detail, name, contact, covers, time)
                else :
                    data = {'message': 'For GPS Check-IN, you should be within 500m of the restaurant', 'success':'false'}    


    except MySQLdb.OperationalError, e:
            data = {'message': 'Checkin Fail', 'success':'false'}
            print '=error=========================='
    return HttpResponse(json.dumps(data), content_type='application/json')


# function to send welcome mail
def send_welcome_mail(email):
    #pdb.set_trace()
    #gmail_user = "admin@deal-monk.com"
    #gmail_pwd = "info9910128745"
    
    #gmail_user = "admin@deal-monk.com"
    #gmail_pwd = "dealmonkapp"
    
    gmail_user = "training.tungsten@gmail.com"
    gmail_pwd = "team@tungsten74#"
    
    FROM = 'Dealmonk App Admin'
    TO = []
    TO.append(email)
    print '=============in mail ====================='
    TEXT = "Congratulations! \n"
    TEXT = TEXT + "\nYou've successfully signed up for DealMonk App." 
    TEXT = TEXT + "\nWelcome to the Monk's world of Real-Time Deals. The Monk will roll out the best Deals in Real-time for you. So now, you'll never have to spare a second for planning.\n"  

    TEXT = TEXT + "\nJust a few taps and you'll get the best live deals on checking into a restaurant! Please feel free to email us at support@deal-monk.com or call us @ +9199479344 or +918527238292 for any questions, feedback or issues. We will be more than happy to assist you. \n"

    TEXT = TEXT + "\nMonk's blessings," 
    TEXT = TEXT + "\nDealMonk"
      
    SUBJECT = "Welcome to DealMonk"
    server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
    #server = smtplib.SMTP_SSL()
    #server.connect("203.129.203.243", 465)
    server.starttls()
    server.ehlo()
    server.login(gmail_user, gmail_pwd)

    message = """From: %s\nTo: %s\nSubject: %s\n\n%s """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    server.sendmail(FROM, TO, message)
    server.close()			    
    print '===========mail sent==================='
    
# function to send booking confirmation mail    
def send_booking_confirmation_mail(email,offer,restaurantname,time):
    #pdb.set_trace()
    #gmail_user = "admin@deal-monk.com"
    #gmail_pwd = "info9910128745"
    print '===========in mail function================='
    gmail_user = "training.tungsten@gmail.com"
    gmail_pwd = "team@tungsten74#"
    FROM = 'Dealmonk App Admin'
    TO = []
    TO.append(email)
    
    TEXT = "Congratulations!" 
    TEXT = TEXT + "\nYour Deal has been confirmed!" 
    
    TEXT = TEXT + "\nYour Deal details:"
    TEXT = TEXT + "\nOffer: " + offer
    TEXT = TEXT + "\nRestaurant Name: " + restaurantname  
    TEXT = TEXT + "\nValidity: " + time
    
      
    SUBJECT = "Deal Confirmed!"
    server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!

    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)

    message = """From: %s\nTo: %s\nSubject: %s\n\n%s """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    server.sendmail(FROM, TO, message)
    print '==========mail send to customer======================'
    server.close()	
    
# function to send booking confirmation mail    
def send_booking_confirmation_mail_restaurant(res_email,offer, name, contact, covers, time):
    #pdb.set_trace()
    #gmail_user = "admin@deal-monk.com"
    #gmail_pwd = "info9910128745"
    
    gmail_user = "training.tungsten@gmail.com"
    gmail_pwd = "team@tungsten74#"
    FROM = 'Dealmonk App Admin'
    TO = []
    TO.append('admin@deal-monk.com')
    TO.append(res_email)
    
    TEXT = "Congratulations! You've got new guests!\n" 
    TEXT = TEXT + "\nDetails : "
    TEXT = TEXT + "\nName of Guest : " + str(name) 
    TEXT = TEXT + "\nContact No : " + str(contact)
    TEXT = TEXT + "\nCovers : " + str(covers)
    TEXT = TEXT + "\nOffer : " + str(offer)
    TEXT = TEXT + "\nValidity : " + str(time)
    
    TEXT = TEXT + "\n\nPlease feel free to email us at support@deal-monk.com or call us @ +9199479344 or +918527238292 for any questions or issues you face. We will be more than happy to assist you!"

    TEXT = TEXT + "\n\nRegards," 
    TEXT = TEXT + "\nDealMonk Team"    
    
    SUBJECT = "New upcoming guests!"
    server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!

    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)

    server.login(gmail_user, gmail_pwd)
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    server.sendmail(FROM, TO, message)
    server.close()	    
    
    		    

#function to send checking confirmation mail
def send_checkin_mail(user_id):
#pdb.set_trace()
    #gmail_user = "admin@deal-monk.com"
    #gmail_pwd = "info9910128745"
    print '===========in mail functin================'
    consumer = Consumer.objects.get(consumer_id=user_id)
    email = consumer. consumer_email
    gmail_user = "training.tungsten@gmail.com"
    gmail_pwd = "team@tungsten74#"
    FROM = 'Dealmonk App Admin'
    TO = []
    TO.append(email)
    
    TEXT = "Cheers!" 
    TEXT = TEXT + "\nYou have successfully checked-in!" 
    TEXT = TEXT + "\nYour DEAL PASS must have popped up. Please present the Deal Pass at the restaurant to get the deal!"

    TEXT = TEXT + "\nHave a great time!"  

    TEXT = TEXT + "\n\nMonk's blessings," 
    TEXT = TEXT + "\nDealMonk"
    
    SUBJECT = "Check-in successful!"
    server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!

    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    server.sendmail(FROM, TO, message)
    print '==============mail send successfully========================'
    server.close()	

def send_checkin_mail_restaurant(res_email,offer_detail, name, contact, covers, time):
    #pdb.set_trace()
    #gmail_user = "admin@deal-monk.com"
    #gmail_pwd = "info9910128745"
    print '==============mail send admin========================'

    gmail_user = "training.tungsten@gmail.com"
    gmail_pwd = "team@tungsten74#"
    FROM = 'Dealmonk App Admin'
    TO = []
    TO.append('admin@deal-monk.com')
    TO.append(res_email)
    
    TEXT = " Congratulations! A guest has checked in!"
    TEXT = TEXT + "\n\n Details:" 
    TEXT = TEXT + "\n Name of Guest:" + str(name) 
    TEXT = TEXT + "\n Contact No:" + str(contact)
    TEXT = TEXT + "\n Covers:" + str(covers)
    TEXT = TEXT + "\n Offer:" + str(offer_detail)
    TEXT = TEXT + "\n Validity:" + str(time)
    
    TEXT = TEXT + "\n\n We will be looking forward to giving you more business!"

    TEXT = TEXT + "\n Please feel free to email us at support@deal-monk.com or call us @ +9199479344 or +918527238292 for any questions or issues you face. We will be more than happy to assist you!"

    TEXT = TEXT + "\n\n Regards," 
    TEXT = TEXT + "\n DealMonk Team"

      
    SUBJECT = "New Check-in!"
    server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!

    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    server.sendmail(FROM, TO, message)
    print '==============mail send successfully admin========================'

    server.close()	    

 
    
# API to check existing booking

@csrf_exempt
def check_booking(request):
    try:
        if request.method == 'POST':
            print '====================================',request
	    json_obj=json.loads(request.body)
            user_id=json_obj['user_id']
            offer_id=json_obj['offer_id']
            res_id=json_obj['restaurantId']
            identifier = res_id.split( )[0]
            id = res_id.split( )[1]
            print '======================',id
            if(identifier=="Restaurant"):
                restaurant_booking_obj = RestaurantBooking.objects.filter(restaurant_id=id,consumer_id=json_obj['user_id'],restaurant_offerMap_id=json_obj['offer_id'])
                print '===================',restaurant_booking_obj

                if(len(restaurant_booking_obj)>0):
                    for obj in restaurant_booking_obj:
                        dinner = obj.restaurant_booking_covers
                        booking_status = obj.restaurant_booking_status
                        booking_id = str(obj.restaurant_booking_id)
                        print '========booking_status=',
                    data = {'message': "Already booked", 'success':'true', 'dinner' : dinner, 'status' : booking_status, 'booking_id' : booking_id}
                else:
                    data = {'message': "Not booked", 'success':'false'}
            else:
                restaurant_booking_obj = RestaurantBooking.objects.filter(restaurant_branch_id=id,consumer_id=json_obj['user_id'],restaurant_offer_id=json_obj['offer_id'])
                print '===================',restaurant_booking_obj

                if(len(restaurant_booking_obj)>0):
                    for obj in restaurant_booking_obj:
                        dinner = obj.restaurant_booking_covers
                        booking_status = obj.restaurant_booking_status
                        booking_id = str(obj.restaurant_booking_id)

                    data = {'message': "Already booked", 'success':'true','dinner' : dinner, 'status' : booking_status, 'booking_id' : booking_id}
                else:
                    data = {'message': "Not booked", 'success':'false'}

    except MySQLdb.OperationalError, e:
        data = {'message': 'none', 'error_message':'Fail'}
    return HttpResponse(json.dumps(data), content_type='application/json')
    		    
 
    
