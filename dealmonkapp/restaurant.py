from dealmonkapp.models import Restaurant
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_control
from django.contrib import auth
from dealmonkapp.models import *
from geopy.exc import GeocoderTimedOut

from constants import AppUserConstants, ExceptionLabel
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
import pdb
# importing mysqldb and system packages
import MySQLdb, sys
from django.db.models import Q
from django.db.models import F
from django.db import transaction
from geopy.geocoders import Nominatim
import csv
import json
import datetime
#importing exceptions
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from django.core.serializers.json import DjangoJSONEncoder
from datetime import date, timedelta

@csrf_exempt
def view_restaurant_details(request):    
    #owner object
    owner=RestaurantAdmin.objects.filter(id=request.session['ownerid'])
    #restaurant object
    restaurant = Restaurant.objects.filter(restaurant_admin_id=owner.id)    
    print request.session['login_user']
    #branch object
    branch = RestaurantBranch.objects.filter(branch_id=restaurant.branch_id)
    return render(request,'my-restaurant.html', {'rest_list': restaurant,'owner_list':owner,'branch_list':branch})  
 
@csrf_exempt   
def add_restaurant_branch(request):
    #pdb.set_trace();
    cuisine_list_rb=[]
    login_user=request.session['login_user']
    try: 
        if request.method=='POST': 
            owner_obj=RestaurantAdmin.objects.get(id=request.session['ownerid'])          
            rest_obj=Restaurant.objects.get(restaurant_admin_id=owner_obj)
            
            if request.POST.get('rb-hour-check',False):
                    rb_obj= RestaurantBranch(
                      restaurant_id= rest_obj,
                      restaurant_admin_id=owner_obj,    
                      restaurant_branch_name=request.POST['branch_name'].encode('ascii', 'ignore'),
                      restaurant_branch_contact=request.POST['branch_contact'],
                      restaurant_branch_address1=request.POST['branch_addr1'].encode('ascii', 'ignore'),
                      restaurant_branch_address2=request.POST['branch_addr2'].encode('ascii', 'ignore'),
                      restaurant_branch_area=request.POST['branch_area'].encode('ascii', 'ignore'),
                      restaurant_branch_city=request.POST['branch_city'],
                      restaurant_branch_state=request.POST['branch_state'],
                      restaurant_branch_pincode=request.POST['branch_pincode'],
                      restaurant_branch_lat=request.POST['lat_txt'],
                      restaurant_branch_lon=request.POST['lng_txt'],
                      restaurant_branch_create_by=request.session['login_user'],
                      restaurant_branch_update_by=request.session['login_user'],
                      restaurant_branch_opentime_day="00:00:00",
                      restaurant_branch_closetime_day="00:00:00",
                      restaurant_branch_opentime_eve="00:00:00",
                      restaurant_branch_closetime_eve="00:00:00",                                
                      )                      
            elif request.POST['branch_eve_from']=="":
                rb_obj= RestaurantBranch(
                restaurant_id= rest_obj,
                restaurant_admin_id=owner_obj,     
                restaurant_branch_name=request.POST['branch_name'].encode('ascii', 'ignore'),
                restaurant_branch_contact=request.POST['branch_contact'],
                restaurant_branch_address1=request.POST['branch_addr1'].encode('ascii', 'ignore'),
                restaurant_branch_address2=request.POST['branch_addr2'].encode('ascii', 'ignore'),
                restaurant_branch_area=request.POST['branch_area'].encode('ascii', 'ignore'),
                restaurant_branch_city=request.POST['branch_city'],
                restaurant_branch_state=request.POST['branch_state'],
                restaurant_branch_pincode=request.POST['branch_pincode'],
                restaurant_branch_lat=request.POST['lat_txt'],
                restaurant_branch_lon=request.POST['lng_txt'],                        
                restaurant_branch_opentime_day=request.POST['branch_day_from'],
                restaurant_branch_closetime_day=request.POST['branch_day_to'],
                restaurant_branch_opentime_eve="00:00:00",
                restaurant_branch_closetime_eve="00:00:00",
                restaurant_branch_create_by=request.session['login_user'],
                restaurant_branch_update_by=request.session['login_user'],            
                )
            else:
                rb_obj= RestaurantBranch(
                restaurant_id= rest_obj,
                restaurant_admin_id=owner_obj,     
                restaurant_branch_name=request.POST['branch_name'].encode('ascii', 'ignore'),
                restaurant_branch_contact=request.POST['branch_contact'],
                restaurant_branch_address1=request.POST['branch_addr1'].encode('ascii', 'ignore'),
                restaurant_branch_address2=request.POST['branch_addr2'].encode('ascii', 'ignore'),
                restaurant_branch_area=request.POST['branch_area'].encode('ascii', 'ignore'),
                restaurant_branch_city=request.POST['branch_city'],
                restaurant_branch_state=request.POST['branch_state'],
                restaurant_branch_pincode=request.POST['branch_pincode'],
                restaurant_branch_lat=request.POST['lat_txt'],
                restaurant_branch_lon=request.POST['lng_txt'],                        
                restaurant_branch_opentime_day=request.POST['branch_day_from'],
                restaurant_branch_closetime_day=request.POST['branch_day_to'],
                restaurant_branch_opentime_eve=request.POST['branch_eve_from'],
                restaurant_branch_closetime_eve=request.POST['branch_eve_to'],
                restaurant_branch_create_by=request.session['login_user'],
                restaurant_branch_update_by=request.session['login_user'],            
                )
            print "Inserting Restaurant Branch....."     
            rb_obj.save()            
            
            cuisine_list_rb=dict(request.POST)['select_cuisine_rb']        
            cuisine_rb_save(rb_obj,cuisine_list_rb,login_user)
            
            print "Inserted Restaurant Branch!"
            rest_obj.restaurant_has_branch=1
            rest_obj.save()
            
            
         #   for cuisine in couisine_list_rb:
                
            
            owner_list=RestaurantAdmin.objects.get(id=request.session['ownerid'])   
            restaurant_list = Restaurant.objects.get(restaurant_admin_id=owner_obj)
            print 'Restaurant Object value:', restaurant_list  
            restaurant_branch_list=RestaurantBranch.objects.filter(restaurant_id=rest_obj)
            print 'Restaurant Branch List:',restaurant_branch_list       
                
            area_list = AreaFactTable.objects.all() 
            
            cuisine_result=[]
        
            cusine_count=CuisineFactTable.objects.all().count()
            map_cusine_count=CuisineRestaurentMap.objects.filter(restaurant_id=rest_obj.restaurant_id).count()
            cuisine_result=''
            cuisine_result_id=''
            cuisine_rest=CuisineRestaurentMap.objects.filter(restaurant_id=rest_obj.restaurant_id)
            print cuisine_rest
            print '---------------------------------'
            if(cusine_count==map_cusine_count):
                cuisine_result=',ALL';
                for cuisines in cuisine_rest:
                    cuisines_obj = cuisines.cuisine_id
                    cuisine_result_id= cuisine_result_id+','+str(cuisines_obj.fact_id)          
            else: 
                cuisine_rest=CuisineRestaurentMap.objects.filter(restaurant_id=rest_obj.restaurant_id)
                for cuisines in cuisine_rest:
                #print cuisines.cuisine_id
                #print cuisines.cuisine_id.fact_cuisine
                    cuisines_obj = cuisines.cuisine_id
                    cuisine_result_id= cuisine_result_id+','+str(cuisines_obj.fact_id)
                    cuisine_result=cuisine_result+','+cuisines_obj.fact_cuisine
            cuisine_result=cuisine_result[1:]
            cuisine_result_id=cuisine_result_id[1:]
            print cuisine_result
            print '---------------------------------'        
            print cuisine_result_id            
            data = {'restaurant':restaurant_list.get_restaurant_info(),'rest':restaurant_list.get_rest_info(),'area_list':area_list,'owner_list':owner_list,'branch_list':restaurant_branch_list,'cuisine_result':cuisine_result,'cuisine_result_id':cuisine_result_id}
            return redirect('/my-restaurantform/')
            #return render(request,'my-restaurant.html',data)            
            #return render(request,'my-restaurant.html',{'restaurant': restaurant_list.get_restaurant_info(),'rest':restaurant_list.get_rest_info(),'owner_list':owner_list,'branch_list':restaurant_branch_list})
        else:
            print 'Details Not Inserted!'
            return render(request,'add-restaurant-branch.html')
    except Exception,e:
        print 'Exception:',e
        data = {'error':'Internal Error!'}
        return render(request,'add-restaurant-branch.html',data)    
    
def cuisine_rb_save(rb_obj,cuisine_list_rb,login_user):
    for cuisine in cuisine_list_rb:
        cuisine_obj=CuisineFactTable.objects.get(fact_id=cuisine)
        cuisine_map_obj=CuisineRestaurentBranchMap(
            restaurant_branch_id=rb_obj,
            cuisine_id=cuisine_obj,
            #cuisine_rest_create_date=None,
            cuisine_rest_branch_create_by=login_user,
            cuisine_rest_branch_update_by=login_user,
            #cuisine_rest_update_date=None,
            )
        cuisine_map_obj.save()
    
@csrf_exempt
def add_restaurant_details(request):
    #pdb.set_trace();
    cuisine_list=[]
    login_user=request.session['login_user']
    if request.method=='POST':
        owner_obj=RestaurantAdmin.objects.get(id=request.session['ownerid'])     
        if request.FILES:
            print "RestaurantBranch Image is not null"
            image=request.FILES['file']
        else:
            print "RestaurantBranch Image is null"
            image=request.FILES['file']
            #Restaurant Object    
        print "Saving Restaurant....."
        if request.POST.get('rest-hour-check',False):
            print "Restaurant if condition" 
            rest_obj= Restaurant(
                restaurant_admin_id= owner_obj,    
                restaurant_name=request.POST['rest_name'].encode('ascii', 'ignore'),
                restaurant_contactno=request.POST['rest_contactno'],
                restaurant_image=image,
                restaurant_owner_firstname=request.POST['owner_fname'],
                restaurant_owner_lastname=request.POST['owner_lname'],
                restaurant_owner_contact=request.POST['owner_contactno'],
                restaurant_owner_email=request.POST['owner_email'],
                restaurant_addr1=request.POST['rest_addr1'].encode('ascii', 'ignore'),
                restaurant_addr2=request.POST['rest_addr2'].encode('ascii', 'ignore'),
                restaurant_area=request.POST['rest_area'].encode('ascii', 'ignore'),
                restaurant_city=request.POST['rest_city'],
                restaurant_state=request.POST['rest_state'],
                restaurant_zipcode=request.POST['rest_pincode'],
                restaurant_description=request.POST['rest_desc'],
                restaurant_opentime_day="00:00:00",
                restaurant_closetime_day="00:00:00",
                restaurant_opentime_eve="00:00:00",
                restaurant_closetime_eve="00:00:00",
                restaurant_create_by=request.session['login_user'],
                restaurant_update_by=request.session['login_user'],    
                restaurant_lat=request.POST['lat_txt'],
                restaurant_lon=request.POST['lng_txt'],
                )
        elif request.POST['rest_open_eve']=="":
                rest_obj= Restaurant(
                restaurant_admin_id= owner_obj,    
                restaurant_name=request.POST['rest_name'].encode('ascii', 'ignore'),
                restaurant_contactno=request.POST['rest_contactno'],
                restaurant_image=image,
                restaurant_owner_firstname=request.POST['owner_fname'],
                restaurant_owner_lastname=request.POST['owner_lname'],
                restaurant_owner_contact=request.POST['owner_contactno'],
                restaurant_owner_email=request.POST['owner_email'],
                restaurant_addr1=request.POST['rest_addr1'].encode('ascii', 'ignore'),
                restaurant_addr2=request.POST['rest_addr2'].encode('ascii', 'ignore'),
                restaurant_area=request.POST['rest_area'].encode('ascii', 'ignore'),
                restaurant_city=request.POST['rest_city'],
                restaurant_state=request.POST['rest_state'],
                restaurant_zipcode=request.POST['rest_pincode'],
                restaurant_description=request.POST['rest_desc'],
                restaurant_opentime_day=request.POST['rest_open_day'],
                restaurant_closetime_day=request.POST['rest_close_day'],
                restaurant_opentime_eve="00:00:00",
                restaurant_closetime_eve="00:00:00",
                restaurant_create_by=request.session['login_user'],
                restaurant_update_by=request.session['login_user'],  
                restaurant_lat=request.POST['lat_txt'],
                restaurant_lon=request.POST['lng_txt'],          
                )
        else:
                rest_obj= Restaurant(
                restaurant_admin_id= owner_obj,    
                restaurant_name=request.POST['rest_name'].encode('ascii', 'ignore'),
                restaurant_contactno=request.POST['rest_contactno'],
                restaurant_image=image,
                restaurant_owner_firstname=request.POST['owner_fname'],
                restaurant_owner_lastname=request.POST['owner_lname'],
                restaurant_owner_contact=request.POST['owner_contactno'],
                restaurant_owner_email=request.POST['owner_email'],
                restaurant_addr1=request.POST['rest_addr1'].encode('ascii', 'ignore'),
                restaurant_addr2=request.POST['rest_addr2'].encode('ascii', 'ignore'),
                restaurant_area=request.POST['rest_area'].encode('ascii', 'ignore'),
                restaurant_city=request.POST['rest_city'],
                restaurant_state=request.POST['rest_state'],
                restaurant_zipcode=request.POST['rest_pincode'],
                restaurant_description=request.POST['rest_desc'],
                restaurant_opentime_day=request.POST['rest_open_day'],
                restaurant_closetime_day=request.POST['rest_close_day'],
                restaurant_opentime_eve=request.POST['rest_open_eve'],
                restaurant_closetime_eve=request.POST['rest_close_eve'],
                restaurant_create_by=request.session['login_user'],
                restaurant_update_by=request.session['login_user'],  
                restaurant_lat=request.POST['lat_txt'],
                restaurant_lon=request.POST['lng_txt'],          
                )    
        print 'Inserting Restaurant....'    
        rest_obj.save()
        owner_obj.restaurant_admin_has_restaurant=1
        owner_obj.save()
        
        cuisine_list=dict(request.POST)['select_cuisine']        
        cuisine_save(rest_obj,cuisine_list,login_user)
        
        print 'Restaurant inserted!'
        
        
        #Restaurant Branch Object
        print "Saving Restaurant Branch....."         
        if request.POST['branch_name']:
            if request.POST.get('rb-hour-check',False):	                
                    rb_obj= RestaurantBranch(
                      restaurant_id= rest_obj,
                      restaurant_admin_id=owner_obj,    
                      restaurant_branch_name=request.POST['branch_name'].encode('ascii', 'ignore'),
                      restaurant_branch_contact=request.POST['branch_contact'],
                      restaurant_branch_address1=request.POST['branch_addr1'].encode('ascii', 'ignore'),
                      restaurant_branch_address2=request.POST['branch_addr2'].encode('ascii', 'ignore'),
                      restaurant_branch_area=request.POST['branch_area'].encode('ascii', 'ignore'),
                      restaurant_branch_city=request.POST['branch_city'],
                      restaurant_branch_state=request.POST['branch_state'],
                      restaurant_branch_pincode=request.POST['branch_pincode'],
                      restaurant_branch_lat=request.POST['lat_txt'],
                      restaurant_branch_lon=request.POST['lng_txt'], 
                      restaurant_branch_create_by=request.session['login_user'],
                      restaurant_branch_update_by=request.session['login_user'],
                      restaurant_branch_opentime_day="00:00:00",
                      restaurant_branch_closetime_day="00:00:00",
                      restaurant_branch_opentime_eve="00:00:00",
                      restaurant_branch_closetime_eve="00:00:00",           
                    )
            elif request.POST['branch_eve_from']=="":
                rb_obj= RestaurantBranch(
                restaurant_id= rest_obj,
                restaurant_admin_id=owner_obj,     
                restaurant_branch_name=request.POST['branch_name'].encode('ascii', 'ignore'),
                restaurant_branch_contact=request.POST['branch_contact'],
                restaurant_branch_address1=request.POST['branch_addr1'].encode('ascii', 'ignore'),
                restaurant_branch_address2=request.POST['branch_addr2'].encode('ascii', 'ignore'),
                restaurant_branch_area=request.POST['branch_area'].encode('ascii', 'ignore'),
                restaurant_branch_city=request.POST['branch_city'],
                restaurant_branch_state=request.POST['branch_state'],
                restaurant_branch_pincode=request.POST['branch_pincode'],
                restaurant_branch_lat=request.POST['lat_txt'],
                restaurant_branch_lon=request.POST['lng_txt'],                        
                restaurant_branch_opentime_day=request.POST['branch_day_from'],
                restaurant_branch_closetime_day=request.POST['branch_day_to'],
                restaurant_branch_opentime_eve="00:00:00",
                restaurant_branch_closetime_eve="00:00:00",
                restaurant_branch_create_by=request.session['login_user'],
                restaurant_branch_update_by=request.session['login_user'],            
                )
            else:
                rb_obj= RestaurantBranch(
                    restaurant_id= rest_obj,
                            restaurant_admin_id=owner_obj,    
                            restaurant_branch_name=request.POST['branch_name'].encode('ascii', 'ignore'),
                            restaurant_branch_contact=request.POST['branch_contact'],
                            restaurant_branch_address1=request.POST['branch_addr1'].encode('ascii', 'ignore'),
                            restaurant_branch_address2=request.POST['branch_addr2'].encode('ascii', 'ignore'),
                            restaurant_branch_area=request.POST['branch_area'].encode('ascii', 'ignore'),
                            restaurant_branch_city=request.POST['branch_city'],
                            restaurant_branch_state=request.POST['branch_state'],
                            restaurant_branch_pincode=request.POST['branch_pincode'],
                            restaurant_branch_lat=request.POST['lat_txt'],
                            restaurant_branch_lon=request.POST['lng_txt'], 
                            restaurant_branch_opentime_day=request.POST['branch_day_from'],
                            restaurant_branch_closetime_day=request.POST['branch_day_to'],
                            restaurant_branch_opentime_eve=request.POST['branch_eve_from'],
                            restaurant_branch_closetime_eve=request.POST['branch_eve_to'],
                            restaurant_branch_create_by=request.session['login_user'],
                            restaurant_branch_update_by=request.session['login_user'],             
                    )		      
            print "Inserting Restaurant Branch....."     
            rb_obj.save()
            rest_obj.restaurant_has_branch=1
            rest_obj.save()
            
            cuisine_list_rb=dict(request.POST)['select_cuisine_rb']        
            cuisine_rb_save(rb_obj,cuisine_list_rb,login_user)            
            
            print "Inserted Restaurant Branch!" 
        else:
            print "No Restaurant Branch details!"    
        
        owner_list=RestaurantAdmin.objects.get(id=request.session['ownerid'])   
        #print 'owner_obj',owner_list
        restaurant_list = Restaurant.objects.get(restaurant_admin_id=owner_list)
        #print 'Restaurant_obj',restaurant_list
        #print 'Restaurant Object value:', restaurant_list  
        restaurant_branch_list=RestaurantBranch.objects.filter(restaurant_id=rest_obj)
        #print 'Restaurant Branch List:',restaurant_branch_list 
        area_list = AreaFactTable.objects.all()     
        
        cuisine_result=[]
        
        cusine_count=CuisineFactTable.objects.all().count()
        map_cusine_count=CuisineRestaurentMap.objects.filter(restaurant_id=rest_obj.restaurant_id).count()
        cuisine_result=''
        cuisine_result_id=''
        cuisine_rest=CuisineRestaurentMap.objects.filter(restaurant_id=rest_obj.restaurant_id)
        print cuisine_rest
        print '---------------------------------'
        if(cusine_count==map_cusine_count):
            cuisine_result=',ALL';
            for cuisines in cuisine_rest:
                cuisines_obj = cuisines.cuisine_id
                cuisine_result_id= cuisine_result_id+','+str(cuisines_obj.fact_id)          
        else: 
            cuisine_rest=CuisineRestaurentMap.objects.filter(restaurant_id=rest_obj.restaurant_id)
            for cuisines in cuisine_rest:
                #print cuisines.cuisine_id
                #print cuisines.cuisine_id.fact_cuisine
                cuisines_obj = cuisines.cuisine_id
                cuisine_result_id= cuisine_result_id+','+str(cuisines_obj.fact_id)
                cuisine_result=cuisine_result+','+cuisines_obj.fact_cuisine
        cuisine_result=cuisine_result[1:]
        cuisine_result_id=cuisine_result_id[1:]
        print cuisine_result
        print '---------------------------------'        
        print cuisine_result_id
        
        
        
        data = {'restaurant':restaurant_list.get_restaurant_info(),'rest':restaurant_list.get_rest_info(),'area_list':area_list,'owner_list':owner_list,'branch_list':restaurant_branch_list,'cuisine_result':cuisine_result,'cuisine_result_id':cuisine_result_id}
        return render(request,'my-restaurant.html',data)
      
    else:
        print 'Details Not Inserted!'
        return render(request,'my-restaurantform.html')
        
 
def cuisine_save(rest_obj,cuisine_list,login_user):
    for cuisine in cuisine_list:
        cuisine_obj=CuisineFactTable.objects.get(fact_id=cuisine)
        cuisine_map_obj=CuisineRestaurentMap(
                        restaurant_id=rest_obj,
                        cuisine_id=cuisine_obj,
                        #cuisine_rest_create_date=None,
                        cuisine_rest_create_by=login_user,
                        cuisine_rest_update_by=login_user,
                        #cuisine_rest_update_date=None,
                        )
        cuisine_map_obj.save()

def view_upcoming_guests(request):
    owner_obj=RestaurantAdmin.objects.get(id=request.session['ownerid'])
    rest_obj=Restaurant.objects.get(restaurant_admin_id=owner_obj)    
    #print datetime.datetime.now()
    rest_bk = RestaurantBooking.objects.filter(restaurant_id=rest_obj,restaurant_booking_date=datetime.datetime.now())
    guest_list = []
    for guest in rest_bk:
        if guest.restaurant_branch_id:
            branch_name=guest.restaurant_branch_id.restaurant_branch_name
        else:
            branch_name=guest.restaurant_id.restaurant_name    
        print guest.restaurant_booking_status
        status_btn = '<td><div class="select-style"><select class="bk_status"><option value="'+guest.restaurant_booking_status+'" selected>'+guest.restaurant_booking_status+'</option><option value="Confirmed">Confirmed</option><option value="Completed">Full Filled</option><option value="No Show">No Show</option></select></div></td>'
        guest_name = '<td><a data-toggle="tab" class="client-link" style="text-transform:capitalize;">'+guest.consumer_id.consumer_first_name+' '+guest.consumer_id.consumer_last_name+'</a></td>'
        save_btn = '<td><a onclick="save_status('+str(guest.restaurant_booking_id)+',this);" class="btn btn-primary btn-sm saveBtn"><i class="fa fa-floppy-o"></i></a></td>'
        guestdata = {
            'today_restaurant_booking_id'  :  guest.restaurant_booking_id, 
            'today_restaurant_guest_name'  :  guest_name,
            'today_restaurant_booking_date'  :  str(guest.restaurant_booking_date.strftime('%d-%m-%Y')),
            'today_restaurant_booking_time'  :  str(guest.restaurant_booking_time_from.strftime('%I:%M %p'))+" - "+str(guest.restaurant_booking_time_to.strftime('%I:%M %p')), 
            'today_restaurant_booking_branch_name'  :  branch_name, 
            'today_restaurant_booking_discount'  :  guest.restaurant_offerMap_id.restaurant_offer_id.restaurant_offer_detail,
            'today_restaurant_booking_status'  :  status_btn,
            'today_restaurant_save'  :  save_btn,
        }        
        guest_list.append(guestdata)
    data = {'data':guest_list}
    print data
    return HttpResponse(json.dumps(data),content_type='application/json')


@csrf_exempt
def save_status(request):
    try:
        booking_id = request.POST.get('book_id')
        print 'Booking ID',booking_id
        booking_status = request.POST.get('book_status')
        print 'Booking Status',booking_status
        booking_det = RestaurantBooking.objects.get(restaurant_booking_id=booking_id)
        print booking_det.restaurant_booking_status
        booking_det.restaurant_booking_status = booking_status
        booking_det.save()
        print 'Booking Status updated!' 
        #data={'success':'true'}               
    except Exception,e:
        print e        
        #data={'success':'false'}
    return HttpResponse(json.dumps({'success':'true'}),content_type='application/json')

def view_upcoming_guests_tomorrow(request):
    owner_obj=RestaurantAdmin.objects.get(id=request.session['ownerid'])    
    tomorrow_date = datetime.datetime.today() + datetime.timedelta(days=1)
    #print datetime.date.today()    
    rest_bk = RestaurantBooking.objects.filter(restaurant_admin_id=owner_obj,restaurant_booking_date=tomorrow_date)
    guest_list = []
    for guest in rest_bk:
        status_btn = '<td id="booking_status" class="client-status"><span class="label label-info" style="padding: 3px 16px; text-transform:capitalize">'+guest.restaurant_booking_status+'</span></td>'
        guest_name = '<td><a data-toggle="tab" onclick="return show_guest_details('+str(guest.restaurant_booking_id)+');" class="client-link" style="text-transform:capitalize;">'+guest.consumer_id.consumer_first_name+' '+guest.consumer_id.consumer_last_name+'</a></td>'
        guestdata = {
            'tom_restaurant_booking_id'  :  guest.restaurant_booking_id, 
            'tom_restaurant_guest_name'  :  guest_name,
            'tom_restaurant_booking_datetime'  :  str(guest.restaurant_booking_date)+" "+str(guest.restaurant_booking_time), 
            'tom_restaurant_booking_covers'  :  guest.restaurant_booking_covers, 
            'tom_restaurant_booking_discount'  :  guest.restaurant_offer_id.restaurant_offer_detail,
            'tom_restaurant_booking_status'  :  status_btn,
        }        
        guest_list.append(guestdata)
    data = {'data':guest_list}
    print data
    return HttpResponse(json.dumps(data),content_type='application/json')


def view_booking_details(request):
    try:
        booking_id = request.GET.get('book_id')
        print booking_id
        booking_det = RestaurantBooking.objects.get(restaurant_booking_id=booking_id)
        print booking_det.consumer_id.consumer_first_name
        bk_datetime = str(booking_det.restaurant_booking_date) + " " + str(booking_det.restaurant_booking_time) 
        print bk_datetime
        guest_name = booking_det.consumer_id.consumer_first_name + " " + booking_det.consumer_id.consumer_last_name
        print guest_name
        print booking_det.restaurant_booking_status
        data={  
                'success':'true',
                'bk_id':booking_id,
                'guest_name':guest_name,                
                'guest_email':booking_det.consumer_id.consumer_email,
                'guest_contact':booking_det.consumer_id.consumer_contactno,
                'guest_covers':booking_det.restaurant_booking_covers,
                'guest_offer':booking_det.restaurant_offer_id.restaurant_offer_detail,
                'guest_datetime':bk_datetime,
                'guest_booking_status': booking_det.restaurant_booking_status           
             }
        print data
    except Exception,e:
        print e
        data={'success':'false','booking_detail':booking_det}
    return HttpResponse(json.dumps(data),content_type='application/json')

def view_old_guests(request):
    owner_obj=RestaurantAdmin.objects.get(id=request.session['ownerid'])    
    rest_obj=Restaurant.objects.get(restaurant_admin_id=owner_obj)
    rest_bk = RestaurantBooking.objects.filter(restaurant_id=rest_obj)
    rest_bk = rest_bk.exclude(restaurant_booking_date=datetime.datetime.today())
    guest_list = []
    for guest in rest_bk:
        if guest.restaurant_branch_id:
            branch_name=guest.restaurant_branch_id.restaurant_branch_name
        else:
            branch_name=guest.restaurant_id.restaurant_name
        status_btn = '<td id="booking_status" class="client-status"><span class="label label-info" style="padding: 3px 16px; text-transform:capitalize">'+guest.restaurant_booking_status+'</span></td>'
        guest_name = '<td><a data-toggle="tab" onclick="return show_guest_details('+str(guest.restaurant_booking_id)+');" class="client-link" style="text-transform:capitalize;">'+guest.consumer_id.consumer_first_name+' '+guest.consumer_id.consumer_last_name+'</a></td>'
        guestdata = {
            'old_restaurant_booking_id'  :  guest.restaurant_booking_id, 
            'old_restaurant_guest_name'  :  guest_name,
            'old_restaurant_booking_date'  :  str(guest.restaurant_booking_date.strftime('%d-%m-%Y')),
            'old_restaurant_booking_time'  :  str(guest.restaurant_booking_time_from.strftime('%I:%M %p'))+" - "+str(guest.restaurant_booking_time_to.strftime('%I:%M %p')), 
            'old_restaurant_booking_branch_name'  :  branch_name, 
            'old_restaurant_booking_discount'  :  guest.restaurant_offerMap_id.restaurant_offer_id.restaurant_offer_detail,
            'old_restaurant_booking_status'  :  status_btn,
        }        
        guest_list.append(guestdata)
    data = {'data':guest_list}
    print data
    return HttpResponse(json.dumps(data),content_type='application/json')


def view_calendar_events(request):
    offerList = RestaurantOffer.objects.all()    
    try:
        offers = []
        for offer in offerList:
            print offer.restaurant_offer_detail
            print offer.restaurant_offer_date # + " " + offer.restaurant_offer_time_from
            start_var = str(offer.restaurant_offer_date)+" "+str(offer.restaurant_offer_time_from)
            print start_var
            end_var = str(offer.restaurant_offer_date)+" "+str(offer.restaurant_offer_time_to)
        #print str(offer.restaurant_offer_date)+str(offer.restaurant_offer_time_from)	    
            offers.append({'title': offer.restaurant_offer_detail, 'start': start_var, 'end':end_var})
        # something similar for owned events, maybe with a different className if you like
        print offers
        #data={'offers':offers}
        return HttpResponse(json.dumps({'offers':offers}, cls=DjangoJSONEncoder), content_type='application/json')
    except Exception,e:
        print 'Exception ',e
        data={'offers':offers}
        return HttpResponse(json.dumps({'offers':offers}, cls=DjangoJSONEncoder), content_type='application/json')


def map_state(request):
    city = request.GET.get('city')    
    try:
        fact=AreaFactTable.objects.get(fact_city=city)	
        print fact.fact_state
        data={'state':fact.fact_state}
        print 'success'
        return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception,e:
        print 'Exception ',e
        return HttpResponse(json.dumps({'error':'Error!'}, cls=DjangoJSONEncoder), content_type='application/json')

@csrf_exempt
def update_restaurant_details(request):
    #pdb.set_trace()
    cuisine_list=[]
    login_user=request.session['login_user']
    if request.method=='POST':
        if request.FILES:
            print "RestaurantBranch Image is not null"
            image = request.FILES['file']
        else:
            print "RestaurantBranch Image is null"
            rest_obj=Restaurant.objects.get(restaurant_id=request.POST['rest_id'])
            image= rest_obj.restaurant_image
        rest_obj=Restaurant.objects.get(restaurant_id=request.POST['rest_id'])
        owner_obj=RestaurantAdmin.objects.get(id=request.session['ownerid'])  
        #print owner_obj
        #Restaurant Object    
        print "Updating Restaurant....."
        if request.POST.get('rest-hour-check',False):
            #print "Restaurant if condition" 		    
            rest_obj.restaurant_admin_id = owner_obj    
            rest_obj.restaurant_name=request.POST['rest_name'].encode('ascii', 'ignore')
            rest_obj.restaurant_contactno=request.POST['rest_contactno']
            rest_obj.restaurant_image=image
            rest_obj.restaurant_addr1=request.POST['rest_addr1'].encode('ascii', 'ignore')
            rest_obj.restaurant_addr2=request.POST['rest_addr2'].encode('ascii', 'ignore')
            rest_obj.restaurant_area=request.POST['rest_area'].encode('ascii', 'ignore')
            rest_obj.restaurant_city=request.POST['rest_city']
            rest_obj.restaurant_state=request.POST['rest_state']
            rest_obj.restaurant_zipcode=request.POST['rest_pincode']
            rest_obj.restaurant_description=request.POST['rest_desc']
            rest_obj.restaurant_opentime_day="00:00:00"
            rest_obj.restaurant_closetime_day="00:00:00"
            rest_obj.restaurant_opentime_eve="00:00:00"
            rest_obj.restaurant_closetime_eve="00:00:00"
            rest_obj.restaurant_create_by=request.session['login_user']
            rest_obj.restaurant_update_by=request.session['login_user']
            rest_obj.restaurant_lat=request.POST['lat_txt']
            rest_obj.restaurant_lon=request.POST['lng_txt']
            rest_obj.save() 
        elif request.POST['rest_open_eve']=="":
            rest_obj.restaurant_admin_id = owner_obj    
            rest_obj.restaurant_name=request.POST['rest_name'].encode('ascii', 'ignore')
            rest_obj.restaurant_contactno=request.POST['rest_contactno']
            rest_obj.restaurant_image=image
            rest_obj.restaurant_addr1=request.POST['rest_addr1'].encode('ascii', 'ignore')
            rest_obj.restaurant_addr2=request.POST['rest_addr2'].encode('ascii', 'ignore')
            rest_obj.restaurant_area=request.POST['rest_area'].encode('ascii', 'ignore')
            rest_obj.restaurant_city=request.POST['rest_city']
            rest_obj.restaurant_state=request.POST['rest_state']
            rest_obj.restaurant_zipcode=request.POST['rest_pincode']
            rest_obj.restaurant_description=request.POST['rest_desc']
            rest_obj.restaurant_opentime_day=request.POST['rest_open_day']
            rest_obj.restaurant_closetime_day=request.POST['rest_close_day']
            rest_obj.restaurant_opentime_eve="00:00:00"
            rest_obj.restaurant_closetime_eve="00:00:00"
            rest_obj.restaurant_create_by=request.session['login_user']
            rest_obj.restaurant_update_by=request.session['login_user']
            rest_obj.restaurant_lat=request.POST['lat_txt']
            rest_obj.restaurant_lon=request.POST['lng_txt']
            rest_obj.save()     
        else:
            rest_obj.restaurant_admin_id= owner_obj    
            rest_obj.restaurant_name=request.POST['rest_name'].encode('ascii', 'ignore')
            rest_obj.restaurant_contactno=request.POST['rest_contactno']
            rest_obj.restaurant_image=image
            rest_obj.restaurant_addr1=request.POST['rest_addr1'].encode('ascii', 'ignore')
            rest_obj.restaurant_addr2=request.POST['rest_addr2'].encode('ascii', 'ignore')
            rest_obj.restaurant_area=request.POST['rest_area'].encode('ascii', 'ignore')
            rest_obj.restaurant_city=request.POST['rest_city']
            rest_obj.restaurant_state=request.POST['rest_state']
            rest_obj.restaurant_zipcode=request.POST['rest_pincode']
            rest_obj.restaurant_description=request.POST['rest_desc']
            rest_obj.restaurant_opentime_day=request.POST['rest_open_day']
            rest_obj.restaurant_closetime_day=request.POST['rest_close_day']
            rest_obj.restaurant_opentime_eve=request.POST['rest_open_eve']
            rest_obj.restaurant_closetime_eve=request.POST['rest_close_eve']
            rest_obj.restaurant_create_by=request.session['login_user']
            rest_obj.restaurant_update_by=request.session['login_user']
            rest_obj.restaurant_lat=request.POST['lat_txt']
            rest_obj.restaurant_lon=request.POST['lng_txt']           
            rest_obj.save()    
        
        print 'Hiii'
        CuisineRestaurentMap.objects.filter(restaurant_id=rest_obj).delete()
        print 'Cuisine is deleted'
        print request.POST['select_cuisine']
        print '>?'
        cuisine_list=dict(request.POST)['select_cuisine']        
        cuisine_save(rest_obj,cuisine_list,login_user)
        
        print 'Updating Restaurant....'    
        #rest_obj.save()
        print 'Updated Restaurant!'
        owner_list=RestaurantAdmin.objects.get(id=request.session['ownerid'])   
        restaurant_list = Restaurant.objects.get(restaurant_admin_id=owner_obj)
        #print 'Restaurant Object value:', restaurant_list  
        restaurant_branch_list=RestaurantBranch.objects.filter(restaurant_id=rest_obj)
        area_list=AreaFactTable.objects.all()
        
        cuisine_result=[]
        
        cusine_count=CuisineFactTable.objects.all().count()
        map_cusine_count=CuisineRestaurentMap.objects.filter(restaurant_id=rest_obj.restaurant_id).count()
        cuisine_result=''
        cuisine_result_id=''
        cuisine_rest=CuisineRestaurentMap.objects.filter(restaurant_id=rest_obj.restaurant_id)
        print cuisine_rest
        print '---------------------------------'
        if(cusine_count==map_cusine_count):
            cuisine_result=',ALL';
            for cuisines in cuisine_rest:
                cuisines_obj = cuisines.cuisine_id
                cuisine_result_id= cuisine_result_id+','+str(cuisines_obj.fact_id)          
        else: 
            cuisine_rest=CuisineRestaurentMap.objects.filter(restaurant_id=rest_obj.restaurant_id)
            for cuisines in cuisine_rest:
                #print cuisines.cuisine_id
                #print cuisines.cuisine_id.fact_cuisine
                cuisines_obj = cuisines.cuisine_id
                cuisine_result_id= cuisine_result_id+','+str(cuisines_obj.fact_id)
                cuisine_result=cuisine_result+','+cuisines_obj.fact_cuisine
        cuisine_result=cuisine_result[1:]
        cuisine_result_id=cuisine_result_id[1:]
        print cuisine_result
        print '---------------------------------'        
        print cuisine_result_id
        #print 'Restaurant Branch List:',restaurant_branch_list 
        #data = {'restaurant':restaurant_list.get_restaurant_info(),'rest':restaurant_list.get_rest_info(),'area_list':area_list,'owner_list':owner_list,'branch_list':restaurant_branch_list,'cuisine_result':cuisine_result,'cuisine_result_id':cuisine_result_id}
        data={'success':'true'}
        #return redirect('/my-restaurantform/')
        return HttpResponse(json.dumps(data),content_type='application/json')
        #return render(request,'my-restaurant.html', data)    
        
@csrf_exempt
def update_owner_details(request):
    if request.method=='POST':        
        rest_obj=Restaurant.objects.get(restaurant_id=request.POST['rest_id'])     
        owner_obj=RestaurantAdmin.objects.get(id=request.session['ownerid'])   
        #print owner_obj
        #Restaurant Object    
        print "Updating Restaurant Owner details"        
        rest_obj.restaurant_owner_firstname=request.POST['owner_fname']
        rest_obj.restaurant_owner_lastname=request.POST['owner_lname']
        rest_obj.restaurant_owner_contact=request.POST['owner_contactno']
        rest_obj.restaurant_owner_email=request.POST['owner_email']                        		            
        print 'Updating Restaurant Owner....'    
        rest_obj.save()
        print 'Updated Restaurant Owner!'
        owner_list=RestaurantAdmin.objects.get(id=request.session['ownerid'])   
        restaurant_list = Restaurant.objects.get(restaurant_admin_id=owner_obj)
        #print 'Restaurant Object value:', restaurant_list  
        restaurant_branch_list=RestaurantBranch.objects.filter(restaurant_id=rest_obj)
        area_list=AreaFactTable.objects.all()
        #print 'Restaurant Branch List:',restaurant_branch_list 
        
        cuisine_result=[]
        
        cusine_count=CuisineFactTable.objects.all().count()
        map_cusine_count=CuisineRestaurentMap.objects.filter(restaurant_id=rest_obj.restaurant_id).count()
        cuisine_result=''
        cuisine_result_id=''
        cuisine_rest=CuisineRestaurentMap.objects.filter(restaurant_id=rest_obj.restaurant_id)
        print cuisine_rest
        print '---------------------------------'
        if(cusine_count==map_cusine_count):
            cuisine_result=',ALL';
            for cuisines in cuisine_rest:
                cuisines_obj = cuisines.cuisine_id
                cuisine_result_id= cuisine_result_id+','+str(cuisines_obj.fact_id)          
        else: 
            cuisine_rest=CuisineRestaurentMap.objects.filter(restaurant_id=rest_obj.restaurant_id)
            for cuisines in cuisine_rest:
                #print cuisines.cuisine_id
                #print cuisines.cuisine_id.fact_cuisine
                cuisines_obj = cuisines.cuisine_id
                cuisine_result_id= cuisine_result_id+','+str(cuisines_obj.fact_id)
                cuisine_result=cuisine_result+','+cuisines_obj.fact_cuisine
        cuisine_result=cuisine_result[1:]
        cuisine_result_id=cuisine_result_id[1:]
        print cuisine_result
        print '---------------------------------'        
        print cuisine_result_id
        
        data = {'restaurant':restaurant_list.get_restaurant_info(),'rest':restaurant_list.get_rest_info(),'owner':owner_list,'branch_list':restaurant_branch_list,'area_list':area_list,'cuisine_result':cuisine_result,'cuisine_result_id':cuisine_result_id}
        #print data
        return redirect('/my-restaurantform/')
        #return render(request,'my-restaurant.html', data)        
        
def get_branch_details(request):       
    try:
        cuisine_result_id=''        
        branch_id = request.GET.get('branch_id')
        print branch_id
        branch_obj = RestaurantBranch.objects.get(restaurant_branch_id=branch_id)
        cuisine_rest=CuisineRestaurentBranchMap.objects.filter(restaurant_branch_id=branch_obj.restaurant_branch_id)
        for cuisine in cuisine_rest:
            cuisines_obj = cuisine.cuisine_id
            cuisine_result_id= cuisine_result_id+''+str(cuisines_obj.fact_id)
        
        y = [i.decode('UTF-8') for i in cuisine_result_id]
        print y
        
        data={  
                'success':'true',
                'branch_id':branch_id,
                'branch_name':branch_obj.restaurant_branch_name,                
                'branch_cuisine':y,
                'branch_contact':branch_obj.restaurant_branch_contact,
                'branch_addr1':branch_obj.restaurant_branch_address1,
                'branch_addr2':branch_obj.restaurant_branch_address2,
                'branch_area':branch_obj.restaurant_branch_area,
                'branch_city': branch_obj.restaurant_branch_city,
                'branch_state': branch_obj.restaurant_branch_state,
                'branch_zipcode': branch_obj.restaurant_branch_pincode,
                'branch_lat':branch_obj.restaurant_branch_lat,
                'branch_lng':branch_obj.restaurant_branch_lon,
                'rb_day_from':branch_obj.restaurant_branch_opentime_day.strftime("%H:%M"),
                'rb_day_to':branch_obj.restaurant_branch_closetime_day.strftime("%H:%M"),
                'rb_eve_from':branch_obj.restaurant_branch_opentime_eve.strftime("%H:%M"),
                'rb_eve_to':branch_obj.restaurant_branch_closetime_eve.strftime("%H:%M"),
             }
        print data
    except Exception,e:
        print e
        data={'success':'false'}
    return HttpResponse(json.dumps(data),content_type='application/json')        

@csrf_exempt
def update_branch_details(request):
    login_user=request.session['login_user']    
    if request.method=='POST':
        branch_lat = ''
        branch_lon = ''
        rb_obj=RestaurantBranch.objects.get(restaurant_branch_id=request.POST['branch_id_form'])
        owner_obj=RestaurantAdmin.objects.get(id=request.session['ownerid'])  
        rest_obj=Restaurant.objects.get(restaurant_id=request.POST['rest_id_form'])
        print rest_obj        
        #Restaurant Object    
        print "Updating Restaurant Branch....."
        print request.POST.get('rb-hour-check')
        if request.POST.get('rb-hour-check',False):
            print 'checked'
            rb_obj.restaurant_id= rest_obj
            rb_obj.restaurant_admin_id=owner_obj
            rb_obj.restaurant_branch_name=request.POST['branch_name'].encode('ascii', 'ignore')
            #rb_obj.restaurant_branch_cuisine_type=request.POST['branch_cuisine']
            rb_obj.restaurant_branch_contact=request.POST['branch_contact']
            #restaurant_branch_image=image
            rb_obj.restaurant_branch_address1=request.POST['branch_addr1'].encode('ascii', 'ignore')
            rb_obj.restaurant_branch_address2=request.POST['branch_addr2'].encode('ascii', 'ignore')
            rb_obj.restaurant_branch_area=request.POST['branch_area'].encode('ascii', 'ignore')
            rb_obj.restaurant_branch_city=request.POST['branch_city']
            rb_obj.restaurant_branch_state=request.POST['branch_state']
            rb_obj.restaurant_branch_pincode=request.POST['branch_pincode']
            rb_obj.restaurant_branch_lat=request.POST['lat_txt']
            rb_obj.restaurant_branch_lon=request.POST['lng_txt']
            rb_obj.restaurant_branch_opentime_day="00:00:00"
            rb_obj.restaurant_branch_closetime_day="00:00:00"
            rb_obj.restaurant_branch_opentime_eve="00:00:00"
            rb_obj.restaurant_branch_closetime_eve="00:00:00"
            print rb_obj.restaurant_branch_opentime_day
            rb_obj.restaurant_branch_create_by=request.session['login_user']
            rb_obj.restaurant_branch_update_by=request.session['login_user']            
            rb_obj.save()                               
        elif request.POST['branch_eve_from']=="":
            rb_obj.restaurant_id= rest_obj
            rb_obj.restaurant_admin_id=owner_obj
            rb_obj.restaurant_branch_name=request.POST['branch_name'].encode('ascii', 'ignore')
            #rb_obj.restaurant_branch_cuisine_type=request.POST['branch_cuisine']
            rb_obj.restaurant_branch_contact=request.POST['branch_contact']
            #restaurant_branch_image=image
            rb_obj.restaurant_branch_address1=request.POST['branch_addr1'].encode('ascii', 'ignore')
            rb_obj.restaurant_branch_address2=request.POST['branch_addr2'].encode('ascii', 'ignore')
            rb_obj.restaurant_branch_area=request.POST['branch_area'].encode('ascii', 'ignore')
            rb_obj.restaurant_branch_city=request.POST['branch_city']
            rb_obj.restaurant_branch_state=request.POST['branch_state']
            rb_obj.restaurant_branch_pincode=request.POST['branch_pincode']
            rb_obj.restaurant_branch_lat=request.POST['lat_txt']
            rb_obj.restaurant_branch_lon=request.POST['lng_txt']
            rb_obj.restaurant_branch_opentime_day=request.POST['branch_day_from']
            rb_obj.restaurant_branch_closetime_day=request.POST['branch_day_to']
            rb_obj.restaurant_branch_opentime_eve="00:00:00"
            rb_obj.restaurant_branch_closetime_eve="00:00:00"
            print rb_obj.restaurant_branch_opentime_day
            rb_obj.restaurant_branch_create_by=request.session['login_user']
            rb_obj.restaurant_branch_update_by=request.session['login_user']            
            rb_obj.save()   
        else:
            print 'not checked'
            rb_obj.restaurant_id= rest_obj
            rb_obj.restaurant_admin_id=owner_obj
            rb_obj.restaurant_branch_name=request.POST['branch_name'].encode('ascii', 'ignore')
            #rb_obj.restaurant_branch_cuisine_type=request.POST['branch_cuisine']
            rb_obj.restaurant_branch_contact=request.POST['branch_contact']
            #restaurant_branch_image=image
            rb_obj.restaurant_branch_address1=request.POST['branch_addr1'].encode('ascii', 'ignore')
            rb_obj.restaurant_branch_address2=request.POST['branch_addr2'].encode('ascii', 'ignore')
            rb_obj.restaurant_branch_area=request.POST['branch_area'].encode('ascii', 'ignore')
            rb_obj.restaurant_branch_city=request.POST['branch_city']
            rb_obj.restaurant_branch_state=request.POST['branch_state']
            rb_obj.restaurant_branch_pincode=request.POST['branch_pincode']
            rb_obj.restaurant_branch_lat=request.POST['lat_txt']
            rb_obj.restaurant_branch_lon=request.POST['lng_txt']
            rb_obj.restaurant_branch_opentime_day=request.POST['branch_day_from']
            rb_obj.restaurant_branch_closetime_day=request.POST['branch_day_to']
            rb_obj.restaurant_branch_opentime_eve=request.POST['branch_eve_from']
            rb_obj.restaurant_branch_closetime_eve=request.POST['branch_eve_to']
            rb_obj.restaurant_branch_update_by=request.session['login_user']
            print "Inserting Restaurant Branch....."     
            rb_obj.save()
            
        
        CuisineRestaurentBranchMap.objects.filter(restaurant_branch_id=rb_obj).delete()
        print 'Cuisine is deleted'
        print request.POST['select_cuisine_rb']
        print '>?'
        cuisine_list_rb=dict(request.POST)['select_cuisine_rb']        
        cuisine_rb_save(rb_obj,cuisine_list_rb,login_user)
        
        print 'Updated Restaurant!'
        owner_list=RestaurantAdmin.objects.get(id=request.session['ownerid'])   
        restaurant_list = Restaurant.objects.get(restaurant_admin_id=owner_obj)
        print restaurant_list  
        restaurant_branch_list=RestaurantBranch.objects.filter(restaurant_id=rest_obj)
        #x = restaurant_branch_list.count()
        
        area_list=AreaFactTable.objects.all()
        for restaurant_branch in restaurant_branch_list:
            print restaurant_branch.restaurant_branch_id
            print restaurant_branch.get_restaurantbranch_info()
        
        cuisine_result=[]
        
        cusine_count=CuisineFactTable.objects.all().count()
        map_cusine_count=CuisineRestaurentMap.objects.filter(restaurant_id=rest_obj.restaurant_id).count()
        cuisine_result=''
        cuisine_result_id=''
        cuisine_rest=CuisineRestaurentMap.objects.filter(restaurant_id=rest_obj.restaurant_id)
        print cuisine_rest
        print '---------------------------------'
        if(cusine_count==map_cusine_count):
            cuisine_result=',ALL';
            for cuisines in cuisine_rest:
                cuisines_obj = cuisines.cuisine_id
                cuisine_result_id= cuisine_result_id+','+str(cuisines_obj.fact_id)          
        else: 
            cuisine_rest=CuisineRestaurentMap.objects.filter(restaurant_id=rest_obj.restaurant_id)
            for cuisines in cuisine_rest:
                #print cuisines.cuisine_id
                #print cuisines.cuisine_id.fact_cuisine
                cuisines_obj = cuisines.cuisine_id
                cuisine_result_id= cuisine_result_id+','+str(cuisines_obj.fact_id)
                cuisine_result=cuisine_result+','+cuisines_obj.fact_cuisine
        cuisine_result=cuisine_result[1:]
        cuisine_result_id=cuisine_result_id[1:]
        print cuisine_result
        print '---------------------------------'        
        print cuisine_result_id
        
        data = {'restaurant':restaurant_list.get_restaurant_info(),'rest':restaurant_list.get_rest_info(),'area_list':area_list,'owner_list':owner_list,'branch_list':restaurant_branch_list,'cuisine_result':cuisine_result,'cuisine_result_id':cuisine_result_id}
        #print data
        return redirect('/my-restaurantform/')
        #return render(request,'my-restaurant.html', data)

@csrf_exempt
def insert_offer(request):
    try:
        #pdb.set_trace()
        if request.method=='POST':
            offer_name=request.POST['offer_name']
            v_restaurant_id=request.POST['rest_id']        
        
            print v_restaurant_id       
            rest_obj=Restaurant.objects.get(restaurant_id=v_restaurant_id)
            check_offer_obj=RestaurantOffer.objects.get(restaurant_offer_detail=offer_name.strip(),restaurant_id=rest_obj,restaurant_offer_status='1')        
            if check_offer_obj:
                data={'success':'exist'}        
                return HttpResponse(json.dumps(data),content_type='application/json') 
    except RestaurantOffer.DoesNotExist:
        offer_name=request.POST['offer_name']
        v_restaurant_id=request.POST['rest_id']
        print v_restaurant_id       
        rest_obj=Restaurant.objects.get(restaurant_id=v_restaurant_id)
        offer_obj = RestaurantOffer(
                restaurant_id=rest_obj,
                restaurant_offer_detail=offer_name,
                restaurant_offer_created_by=request.session['login_user'],
                restaurant_offer_update_by=request.session['login_user'],                                        
            )
        offer_obj.save()
        #objects.filter
        r_offer_list=RestaurantOffer.objects.filter(restaurant_id=rest_obj,restaurant_offer_status='1')
        r_offer_count=RestaurantOffer.objects.filter(restaurant_id=rest_obj,restaurant_offer_status='1').count()
        r_offer_list_to_send=[]
        for offer_list in r_offer_list:
                r_offer_list_to_send.append({'offer_id':offer_list.restaurant_offer_id,
                                            'offer_details':offer_list.restaurant_offer_detail})
        print 'Offer inserted!'                
        data={'success':'true',
            'offer': offer_obj.restaurant_offer_detail,
            'offer_id':offer_obj.restaurant_offer_id,
            'r_offer_list':r_offer_list_to_send,
            'r_offer_count':r_offer_count,
            }
        print data
    except Exception, e:
        print 'BIG :',e
        data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'Internal Server Error '}
    return HttpResponse(json.dumps(data),content_type='application/json')    
    
@csrf_exempt
def delete_offer(request):
    #pdb.set_trace()
    try:
        if request.method=='POST':
            offer_id=request.POST['offer_id']        
            print offer_id               
            offer_obj=RestaurantOffer.objects.get(restaurant_offer_id=offer_id)
            offer_obj.restaurant_offer_status='0'
            offer_obj.save();
##        offer_obj.delete()

            rest_obj=Restaurant.objects.get(restaurant_id=request.POST['rest_id'])
            r_offer_list=RestaurantOffer.objects.filter(restaurant_id=rest_obj,restaurant_offer_status='1')
            r_offer_count=RestaurantOffer.objects.filter(restaurant_id=rest_obj,restaurant_offer_status='1').count()
            r_offer_list_to_send=[]
            for offer_list in r_offer_list:
                r_offer_list_to_send.append({'offer_id':offer_list.restaurant_offer_id,
                                            'offer_details':offer_list.restaurant_offer_detail})
            print 'Offer deleted!'              
            data={'success':'true',
                'offer': offer_obj.restaurant_offer_detail,
                'offer_id':offer_obj.restaurant_offer_id,
                'r_offer_list':r_offer_list_to_send,
                'r_offer_count':r_offer_count,
                }  
    except Exception, e:
        print 'BIG :',e  
        data={'success':'error'}
    return HttpResponse(json.dumps(data),content_type='application/json')

@csrf_exempt
def update_offer(request):
    #pdb.set_trace
    print "Up=================="
    print request.POST
    #print request.POST['start_time']
    if request.method=='POST':
        v_restaurant_offer_id=request.POST['offer_id']
        v_restaurant_id=request.POST['rest_id'] 
        print v_restaurant_offer_id       
        rest_obj=Restaurant.objects.get(restaurant_id=v_restaurant_id)
        off_obj=RestaurantOffer.objects.get(restaurant_offer_id=v_restaurant_offer_id)
        offer_obj = Offer_map(
                restaurant_id=rest_obj,
                restaurant_offer_id=off_obj,
                offer_map_time_from=datetime.datetime.strptime(request.POST['start_time'],'%H:%M:%S'),
                offer_map_time_to=datetime.datetime.strptime(request.POST['end_time'],'%H:%M:%S'),
                offer_map_date=datetime.datetime.strptime(request.POST['date'],'%Y-%m-%d').date(),
                offer_map_created_by=request.session['login_user'],
                offer_map_update_by=request.session['login_user'], 
        )
        offer_obj.save()
        print 'Offer inserted!'                
        data={'success':'true'}
        print data
        return HttpResponse(json.dumps(data),content_type='application/json')
    
    
@csrf_exempt   
def check_operations_hours(request):
    print '-----------------------vikramkkkkkkk--------------------------------------'
    #pdb.set_trace()
    try:
        if request.method=='POST':     
            input_d_o= request.POST['rest_od']
            input_d_c= request.POST['rest_cd']
            input_e_o= request.POST['rest_oe']
            input_e_c= request.POST['rest_ce']            
             
            rest_obj=Restaurant.objects.get(restaurant_id=request.POST['rest_id'])
            open_time_day=rest_obj.restaurant_opentime_day.strftime("%H:%M")
            close_time_day=rest_obj.restaurant_closetime_day.strftime("%H:%M")
            open_time_eve=rest_obj.restaurant_opentime_eve.strftime("%H:%M")
            close_time_eve=rest_obj.restaurant_closetime_eve.strftime("%H:%M")
            
            print (input_d_o!=open_time_day) or (input_d_c!=close_time_day) or (input_e_o!=open_time_eve) or (input_e_c!=close_time_eve)
             
            print input_d_o
            print open_time_day
            print (input_d_o!=open_time_day)
                       
            if(input_d_o!=open_time_day) or (input_d_c!=close_time_day) or (input_e_o!=open_time_eve) or (input_e_c!=close_time_eve):
                data={'success':'true','message':'There might be existing offers and bookings that may fall outside the changed operational hours. Such bookings will have to be entertained when the guest arrives. Would you still like to change the operational hours of the restaurant?'}
            else:
                data={'success':'false','msg':'not match'}            
     
    except Exception, e:
        print 'Exception',e
        data={'success':'error'}
    return HttpResponse(json.dumps(data),content_type='application/json')
 
import datetime as dt
mytime = dt.datetime.strptime('0130','%H%M').time()
mydatetime = dt.datetime.combine(dt.date.today(), mytime)
#-------------------SAVE OFFER------------------------------
@csrf_exempt
def save_offer_details(request):
    #pdb.set_trace()
    print "=====vikram singh chandel============="
    try:
        test_time = datetime.datetime.now()
        print 'start time : ',test_time 
        if request.method=='POST':  
            offer_temp=request.POST['offers_list']      
            offer_list = json.loads(offer_temp)            
            rest_obj=Restaurant.objects.get(restaurant_id=request.POST['rest_id'])            
            offer_map_values=[]
            
            for offer in offer_list:                 
                off_obj=RestaurantOffer.objects.get(restaurant_offer_id=offer.get('offer_id')) 
                if "." in offer.get('start'):
                    start_date= datetime.datetime.strptime(offer.get('start')[:offer.get('start').index(".")],'%Y-%m-%dT%H:%M:%S')  
                    end_date= datetime.datetime.strptime(offer.get('end')[:offer.get('start').index(".")],'%Y-%m-%dT%H:%M:%S')                                 
                else:
                    start_date= datetime.datetime.strptime(offer.get('start')[:offer.get('start').index("Z")],'%Y-%m-%dT%H:%M:%S')  
                    end_date= datetime.datetime.strptime(offer.get('end')[:offer.get('start').index("Z")],'%Y-%m-%dT%H:%M:%S')      
                    
                day=end_date-start_date;                          
                for i in range(0, day.days+1):
                    offer_date=(start_date + timedelta(days=i)).date()
                    offer_time_from=start_date.time()
                    offer_time_to=end_date.time()               
                    offer_map_values.append({'restaurant_id':rest_obj,
                                      'restaurant_offer_id':off_obj,
                                      'offer_map_time_from':offer_time_from,
                                      'offer_map_time_to':offer_time_to,
                                      'offer_map_date':offer_date,
                                      'offer_map_created_by':request.session['login_user'],
                                      'offer_map_update_by':request.session['login_user'], 
                                    }) 
            
            for x in range(0, len(offer_map_values)):
                in_start_d= datetime.datetime.combine(offer_map_values[x]['offer_map_date'],offer_map_values[x]['offer_map_time_from'])
                in_end_d= datetime.datetime.combine(offer_map_values[x]['offer_map_date'],offer_map_values[x]['offer_map_time_to'])
                for y in range(0, len(offer_map_values)):
                    if x==y:
                        continue
                    db_start_d=datetime.datetime.combine(offer_map_values[y]['offer_map_date'],offer_map_values[y]['offer_map_time_from'])
                    db_end_d=datetime.datetime.combine(offer_map_values[y]['offer_map_date'],offer_map_values[y]['offer_map_time_to'])                    
                    if check_exsiting_offer_schedule(in_start_d,in_end_d,db_start_d,db_end_d):
                        data={'success':'time_slot_error' }
                        return HttpResponse(json.dumps(data),content_type='application/json')
                    
            for x in range(0, len(offer_map_values)):    
                list_existing_offer=Offer_map.objects.filter(restaurant_id=rest_obj, offer_map_date= offer_map_values[x]['offer_map_date'],offer_map_status='1')    
                in_start_d= datetime.datetime.combine(offer_map_values[x]['offer_map_date'],offer_map_values[x]['offer_map_time_from'])
                in_end_d= datetime.datetime.combine(offer_map_values[x]['offer_map_date'],offer_map_values[x]['offer_map_time_to'])                
                for ex_offer in list_existing_offer:                   
                    db_start_d=datetime.datetime.combine(ex_offer.offer_map_date,ex_offer.offer_map_time_from)
                    db_end_d=datetime.datetime.combine(ex_offer.offer_map_date,ex_offer.offer_map_time_to)
                    if check_exsiting_offer_schedule(in_start_d,in_end_d,db_start_d,db_end_d):
                        data={'success':'time_slot_error' }
                        return HttpResponse(json.dumps(data),content_type='application/json')    
                
            for x in range(0, len(offer_map_values)): 
                offer_obj = Offer_map(
                                    restaurant_id=offer_map_values[x]['restaurant_id'],
                                    restaurant_offer_id=offer_map_values[x]['restaurant_offer_id'],
                                    offer_map_time_from=offer_map_values[x]['offer_map_time_from'],
                                    offer_map_time_to=offer_map_values[x]['offer_map_time_to'],
                                    offer_map_date=offer_map_values[x]['offer_map_date'],
                                    offer_map_created_by=offer_map_values[x]['offer_map_created_by'],
                                    offer_map_update_by=offer_map_values[x]['offer_map_update_by'], 
                                )
                offer_obj.save()            
            data={'success':'true'}
            #send_mail(request.session['login_user'])
            test_time2 = datetime.datetime.now()
            print 'End Time : ',test_time2
            print 'Time Difference : ',test_time2 - test_time
    except Exception, e:
        print 'Exception : ',e
    return HttpResponse(json.dumps(data),content_type='application/json')

def check_exsiting_offer_schedule(in_start_d,in_end_d,db_start_d,db_end_d):
    if(db_start_d < in_start_d < db_end_d) or (db_start_d < in_end_d < db_end_d) or (in_start_d < db_start_d < in_end_d) or (in_start_d < db_end_d < in_end_d) or(in_start_d==db_start_d and in_end_d==db_end_d):
        return True
    else:
        return False
    
def check_exsiting_offer_schedule01(in_start_d,in_end_d,db_start_d,db_end_d):
    if(db_start_d <= in_start_d <= db_end_d) or (db_start_d <= in_end_d <= db_end_d) or (in_start_d <= db_start_d <= in_end_d) or (in_start_d <= db_end_d <= in_end_d):
        return True
    else:
        return False    


##@csrf_exempt
##def save_offer_details(request):
##    #pdb.set_trace()
##    print "=====vikram singh chandel============="
##    try:
##        test_time = datetime.datetime.now()
##        print 'start time : ',test_time 
##        if request.method=='POST':  
##            offer_temp=request.POST['offers_list']      
##            offer_list = json.loads(offer_temp)
##            
##            rest_obj=Restaurant.objects.get(restaurant_id=request.POST['rest_id'])
##            
##            for offer in offer_list:                 
##                off_obj=RestaurantOffer.objects.get(restaurant_offer_id=offer.get('offer_id')) 
##                start_date= datetime.datetime.strptime(offer.get('start')[:offer.get('start').index(".")],'%Y-%m-%dT%H:%M:%S')  
##                end_date= datetime.datetime.strptime(offer.get('end')[:offer.get('start').index(".")],'%Y-%m-%dT%H:%M:%S')                                 
##                day=end_date-start_date;                          
##                for i in range(0, day.days+1):
##                    
##                    #list_existing_offer=Offer_map.objects.filter(restaurant_id=rest_obj)
##                    offer_date=(start_date + timedelta(days=i)).date()
##                    offer_time_from=start_date.time()
##                    offer_time_to=end_date.time()
##                    list_existing_offer=Offer_map.objects.filter(restaurant_id=rest_obj, offer_map_date= offer_date)
##                    
##                    for ex_offer in list_existing_offer:
##                        in_start_d= datetime.datetime.combine(offer_date,offer_time_from)
##                        in_end_d= datetime.datetime.combine(offer_date,offer_time_to)
##                        db_start_d=datetime.datetime.combine(ex_offer.offer_map_date,ex_offer.offer_map_time_from)
##                        db_end_d=datetime.datetime.combine(ex_offer.offer_map_date,ex_offer.offer_map_time_to)
##                        if check_exsiting_offer_schedule(in_start_d,in_end_d,db_start_d,db_end_d):
##                            data={'success':'time_slot_error' }
##                            return HttpResponse(json.dumps(data),content_type='application/json')
##                        
##                    offer_obj = Offer_map(
##                                    restaurant_id=rest_obj,
##                                    restaurant_offer_id=off_obj,
##                                    offer_map_time_from=offer_time_from,
##                                    offer_map_time_to=offer_time_to,
##                                    offer_map_date=offer_date,
##                                    offer_map_created_by=request.session['login_user'],
##                                    offer_map_update_by=request.session['login_user'], 
##                                )
##                    offer_obj.save()
##                    
##            data={'success':'true'}
##            #send_mail(request.session['login_user'])
##            test_time2 = datetime.datetime.now()
##            print 'End Time : ',test_time2
##            print 'Time Difference : ',test_time2 - test_time
##    except Exception, e:
##        print 'Exception : ',e
##    return HttpResponse(json.dumps(data),content_type='application/json')



##def save_offer_details(request):
##    #pdb.set_trace()
##    print "=====vikram singh chandel============="
##    try:
##        if request.method=='POST':  
##            offer_temp=request.POST['offers_list']      
##            offer_list = json.loads(offer_temp)
##            rest_obj_check=Restaurant.objects.get(restaurant_id=request.POST['rest_id'])
##            print rest_obj_check
##            print "!!!!!!!!!!!!!!!!!!!!!!"
##            
##            list_existing_offer=Offer_map.objects.filter(restaurant_id=rest_obj_check)
##            for ex_offer in list_existing_offer:
##                print ex_offer;
##            
##            
##            for offer in offer_list:
##                print '------------------------------------------------'
##                rest_obj=Restaurant.objects.get(restaurant_id=offer.get('rest_id'))
##                off_obj=RestaurantOffer.objects.get(restaurant_offer_id=offer.get('offer_id')) 
##                start_date= datetime.datetime.strptime(offer.get('start')[:offer.get('start').index(".")],'%Y-%m-%dT%H:%M:%S')  
##                end_date= datetime.datetime.strptime(offer.get('end')[:offer.get('start').index(".")],'%Y-%m-%dT%H:%M:%S')                                 
##                day=end_date-start_date;         
##                print start_date
##                print end_date
##                print day.days                
##                for i in range(0, day.days+1):
##                    offer_obj = Offer_map(
##                                    restaurant_id=rest_obj,
##                                    restaurant_offer_id=off_obj,
##                                    offer_map_time_from=start_date.time(),
##                                    offer_map_time_to=end_date.time(),
##                                    offer_map_date=(start_date + timedelta(days=i)).date(),
##                                    offer_map_created_by=request.session['login_user'],
##                                    offer_map_update_by=request.session['login_user'], 
##                                )
##                    offer_obj.save()
##                    send_mail(request.session['login_user'])
##            data={'success':'true'}
##    except Exception, e:
##        print 'Exception : ',e
##    return HttpResponse(json.dumps(data),content_type='application/json')
#--------------------------------View Offers-----------------------------------------------
   
def get_offer_schedule_list(request):
    try:
        #pdb.set_trace()
        get_offer_schedule_list   =Offer_map.objects.filter(restaurant_id=request.GET['rest_id'],offer_map_status='1') 
        post_offer_schedule_list=[]
        for list in get_offer_schedule_list:
            print '---------------start------------------'
            print list.offer_map_time_from
            print list.offer_map_time_to
            print list.offer_map_date
            print unicode(list.offer_map_date)+' '+unicode(list.offer_map_time_from)
            post_offer_schedule_list.append({'title':list.restaurant_offer_id.restaurant_offer_detail,
                                            'start':unicode(list.offer_map_date)+' '+unicode(list.offer_map_time_from),
                                            'end':unicode(list.offer_map_date)+' '+unicode(list.offer_map_time_to),
                                            '_id':list.offer_map_id,
                                            'offer_id':list.restaurant_offer_id.restaurant_offer_id
                                            })
        print '---------------------end--------------------'
    except Exception, e:
        print 'Exception : ',e
    return HttpResponse(json.dumps(post_offer_schedule_list),content_type='application/json')

#-----------------------------check existence----------------------------------------------
def check_offer_schedule_existence(request):
    #pdb.set_trace()
    data={}
    try:
        print ''        
        offer_obj=Offer_map.objects.get(offer_map_id=request.GET['offer_map_id'],offer_map_status='1');
        if offer_obj:                
            booking_objs=RestaurantBooking.objects.filter(restaurant_offerMap_id=offer_obj)
            if booking_objs: 
                data = {'status': 'exist','message':'There might be confirmed bookings present on this offer and those will still need to be entertained when the guest arrives at the restaurant. Would you still like to delete the offer?'}
            else:
                data = {'status': 'exist','message':'Are you sure you want to delete this offer from the calendar?'}
        else:  
            data = {'status': 'not exist'}
    except RestaurantBooking.DoesNotExist as er:
        print er
        data = {'status': 'exist','message':'Are you sure you want to delete this offer from the calendar?'}
    except Offer_map.DoesNotExist:
        data = {'status': 'not exist'}
    except Exception, e:
        print 'Exception: ',e
        data = {'status': 'error'}
    return HttpResponse(json.dumps(data),content_type='application/json') 

#-----------------------------delete_offer_map ----------------------------------------------
def delete_offer_sechedule(request):
    try:    
        offer_obj=Offer_map.objects.get(offer_map_id=request.GET['offer_map_id']);    
        offer_obj.offer_map_status='0'  
##        offer_obj.delete()
        offer_obj.save()
        send_mail(request.session['login_user'])
        data = {'status': 'success'}
    except Exception, e:
        print 'Exception: ',e
        data = {'status': 'error'}
    return HttpResponse(json.dumps(data),content_type='application/json') 


def send_mail(deal_monk_username):
    #pdb.set_trace()
    gmail_user = "training.tungsten@gmail.com"
    gmail_pwd = "team@tungsten74#"
    FROM = 'Dealmonk App Admin'
    TO = []
    
    try:
        TO.append(deal_monk_username)

        TEXT = "Dear Sir,"+'\n'+'\n'+"The changes made by you to your promotions calendar have been saved. All changes made by you will take effect in real-time."+'\n'+'\n'+"Please feel free to email us at support@deal-monk.com or call us @ +9199479344 or +918527238292 for any questions or issues you face. We will be more than happy to assist you!"+'\n'+"Regards,"+'\n'+"DealMonk Team"
        SUBJECT = "Changes have been saved. "
        server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
        print '---------current pointer  -------------'

        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        server.sendmail(FROM, TO, message)
        server.close()			
        data = {'success': 'true'}

    except Exception, e:
        print e
    return 1
