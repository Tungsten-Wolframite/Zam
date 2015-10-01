from django.shortcuts import render
from django.contrib.auth.models import User
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
import pdb
import csv
import json
#importing exceptions
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from dealmonkapp import models
from django.core.serializers.json import DjangoJSONEncoder
# Create your views here.
import smtplib
import re

from datetime import date


SERVER_PATH='http://192.168.0.123:9999'
#SERVER_PATH='http://54.148.82.251/'
def home(request):
    try:
        if request.user.is_authenticated():
            print request.user
            return redirect('/dashboard/')
        return render_to_response('index.html')
    except Exception,e:
        print 'Exception:',e
        return render_to_response('index.html')
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)    
def open_dashboard(request):
    #pdb.set_trace()
    try:
        print request.user
        if not request.user.is_authenticated():
            return redirect('/')        
        else:
            owner_obj=RestaurantAdmin.objects.get(id=request.session['ownerid'])
            user_img=get_image(owner_obj)
            if owner_obj.restaurant_admin_has_restaurant==1:
                user_img=get_image(owner_obj)         
                rest_obj=Restaurant.objects.get(restaurant_admin_id=owner_obj)
                print rest_obj
                rest_bk_list= RestaurantBooking.objects.filter(restaurant_id=rest_obj,restaurant_booking_date=datetime.now())           
                print '----------'
                print rest_bk_list
                offer_list=Offer_map.objects.filter(restaurant_id=rest_obj,offer_map_date=datetime.now())           
                data={'rest_bk_list':rest_bk_list,'offer_list':offer_list,'user_img':user_img}
                return render(request,'dashboard.html',data)
            else:
                data={'user_img':user_img}
                return render(request,'dashboard.html',data)
    except Exception,e:
        return render_to_response('index.html')

def open_bookings(request):
    return render(request,'bookings.html')  

def open_promotions(request): 
    try:        
        if not request.user.is_authenticated():
            return redirect('/')    
        
        owner_obj=RestaurantAdmin.objects.get(id=request.session['ownerid'])    
        if owner_obj.restaurant_admin_has_restaurant==1:
            user_img=get_image(owner_obj)         
            rest_obj = Restaurant.objects.get(restaurant_admin_id=owner_obj)          
            offerList = RestaurantOffer.objects.filter(restaurant_id=rest_obj,restaurant_offer_status='1')
            total_offer=RestaurantOffer.objects.filter(restaurant_id=rest_obj,restaurant_offer_status='1').count();
            d_opentime= rest_obj.restaurant_opentime_day.strftime('%H:%M:%S')
            d_closetime=rest_obj.restaurant_closetime_day.strftime('%H:%M:%S')
            e_opentime= rest_obj.restaurant_opentime_eve.strftime('%H:%M:%S')
            e_closetime=rest_obj.restaurant_closetime_eve.strftime('%H:%M:%S')
                
            data={'offerlist':offerList,'restaurant':rest_obj,
                'd_opentime':d_opentime,'d_closetime':d_closetime,
                'e_opentime':e_opentime,'e_closetime':e_closetime,
                'total_offer':total_offer,
                'user_img':user_img,
                }
            return render(request,'promotions.html',data)
        else:
            area_list = AreaFactTable.objects.all()     
            cuisine_list=CuisineFactTable.objects.all()
            data={'area_list':area_list,'cuisine_list':cuisine_list,'error_msg':'Please add restaurant details first and then proceed to Promotions!'}
            return render(request,'my-restaurantform.html',data)  
    except Exception,e:
        data={"error":e}
        return HttpResponse(json.dumps(data),content_type='application/json')


def get_image(owner_obj):
    try:
        img_path= owner_obj.restaurant_admin_profile_pic.url
        if img_path:
            return SERVER_PATH+img_path
        else:
            return SERVER_PATH+'/media/Admin_images/admin-image.png'
    except Exception,e:
        return SERVER_PATH+'/media/Admin_images/admin-image.png'
    

def load_upcoming_guests(request): 
    if not request.user.is_authenticated():
            return redirect('/') 
    try:
        owner_obj=RestaurantAdmin.objects.get(id=request.session['ownerid'])
        if owner_obj.restaurant_admin_has_restaurant==1: 
            user_img=get_image(owner_obj)  
            data={'user_img':user_img}
            return render(request,'bookings.html',data) 
        else:
            area_list = AreaFactTable.objects.all()     
            cuisine_list=CuisineFactTable.objects.all()
            data={'area_list':area_list,'cuisine_list':cuisine_list,'error_msg':'Please add restaurant details first and then proceed to Upcoming Guest!'}
            return render(request,'my-restaurantform.html',data)
    except Exception,e:
        data={"error":e}
        return HttpResponse(json.dumps(data),content_type='application/json')

   
def open_myrestaurant(request):
    return render(request,'my-restaurant.html')  

def open_my_restaurantform(request):
    #pdb.set_trace()
    try:
        if not request.user.is_authenticated():
            return redirect('/') 
        
        owner_obj=RestaurantAdmin.objects.get(id=request.session['ownerid'])        
        #rest_obj=Restaurant.objects.get(owner_id=owner_obj)               
        if owner_obj.restaurant_admin_has_restaurant==1:
            print "Go to view Restaurant"
            user_img=get_image(owner_obj)   
            rest_obj = Restaurant.objects.get(restaurant_admin_id=owner_obj)
            #rb_obj = RestaurantBranch.objects.get(restaurant_id=rest_obj)
            restaurant_branch_list=RestaurantBranch.objects.filter(restaurant_id=rest_obj)
            owner_list=RestaurantAdmin.objects.get(id=request.session['ownerid'])
            restaurant_list = Restaurant.objects.get(restaurant_admin_id=owner_obj)
            area_list=AreaFactTable.objects.all()
            cuisine_list=CuisineFactTable.objects.all()
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
            print '----------------vikas-----------------'        
            print restaurant_list
            
            items,item_ids = [],[]
            for item in restaurant_branch_list:
                if item.restaurant_branch_id not in item_ids:
                    items.append({'restaurant_branch_id':item.restaurant_branch_id,'restaurant_branch_name':item.restaurant_branch_name,'restaurant_branch_city':item.restaurant_branch_city,
                        'restaurant_branch_opentime_day':item.restaurant_branch_opentime_day.strftime("%I:%M %p"),'restaurant_branch_closetime_day':item.restaurant_branch_closetime_day.strftime("%I:%M %p"),
                        'restaurant_branch_opentime_eve':item.restaurant_branch_opentime_eve.strftime("%I:%M %p"),'restaurant_branch_closetime_eve':item.restaurant_branch_closetime_eve.strftime("%I:%M %p")
                        })
                    item_ids.append(item.restaurant_branch_id)
                    
            print items
        
            data={'restaurant':restaurant_list.get_restaurant_info(),'rest':restaurant_list.get_rest_info(),
            'owner':owner_list,'branch_list':restaurant_branch_list,'area_list':area_list,
            'cuisine_list':cuisine_list,'cuisine_rest':cuisine_rest,'cuisine_result':cuisine_result,
            'cuisine_result_id':cuisine_result_id,'user_img':user_img,'items':items}
            return render(request,'my-restaurant.html',data)     
        else:
            print "Go to add Restaurant"
            area_list=AreaFactTable.objects.all()
            cuisine_list=CuisineFactTable.objects.all()
            #cuisine_rest=CuisineRestaurentMap.objects.filter(restaurant_id=rest_obj.restaurant_id)
            return render(request,'my-restaurantform.html',{'area_list':area_list,'cuisine_list':cuisine_list}) 
    except Exception,e:
        data={"error":e}
        return HttpResponse(json.dumps(data),content_type='application/json')

def edit_my_restaurantform(request):
    try:
        if not request.user.is_authenticated():
            return redirect('/') 
        
        owner_obj=RestaurantAdmin.objects.get(id=request.session['ownerid'])        
        #rest_obj=Restaurant.objects.get(owner_id=owner_obj)               
        if owner_obj.restaurant_admin_has_restaurant==1:
            print "Go to view Restaurant"
            rest_obj = Restaurant.objects.get(restaurant_admin_id=owner_obj)
            #rb_obj = RestaurantBranch.objects.get(restaurant_id=rest_obj)
            #restaurant_branch_list=RestaurantBranch.objects.filter(restaurant_id=rest_obj)
            owner_list=RestaurantAdmin.objects.get(id=request.session['ownerid'])
            user_img=get_image(owner_obj)
            restaurant_list = Restaurant.objects.get(restaurant_admin_id=owner_obj)
            area_list=AreaFactTable.objects.all()
            cuisine_list=CuisineFactTable.objects.all()
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
            data={'restaurant':restaurant_list.get_restaurant_info(),'rest':restaurant_list.get_rest_info(),'owner':owner_list,'area_list':area_list,'cuisine_list':cuisine_list,'cuisine_rest':cuisine_rest,'cuisine_result':cuisine_result,'cuisine_result_id':cuisine_result_id,'user_img':user_img}
            return render(request,'edit-restaurant.html',data)     
        else:
            print "Go to add Restaurant"
            area_list=AreaFactTable.objects.all()
            cuisine_list=CuisineFactTable.objects.all()
            #cuisine_rest=CuisineRestaurentMap.objects.filter(restaurant_id=rest_obj.restaurant_id)
            return render(request,'my-restaurantform.html',{'area_list':area_list,'cuisine_list':cuisine_list}) 
    except Exception, e:
        data={"error":e}
        return HttpResponse(json.dumps(data),content_type='application/json')

def edit_my_restaurant_branch(request):
    try:
        if not request.user.is_authenticated():
            return redirect('/')
        owner_obj=RestaurantAdmin.objects.get(id=request.session['ownerid'])        
        #rest_obj=Restaurant.objects.get(owner_id=owner_obj)               
        if owner_obj.restaurant_admin_has_restaurant==1:
            print "Go to view Restaurant"
            rest_obj = Restaurant.objects.get(restaurant_admin_id=owner_obj)
            #rb_obj = RestaurantBranch.objects.get(restaurant_id=rest_obj)
            restaurant_branch_list=RestaurantBranch.objects.filter(restaurant_id=rest_obj)
            owner_list=RestaurantAdmin.objects.get(id=request.session['ownerid'])
            user_img=get_image(owner_obj)
            restaurant_list = Restaurant.objects.get(restaurant_admin_id=owner_obj)
            area_list=AreaFactTable.objects.all()
            cuisine_list=CuisineFactTable.objects.all()
        
            data={'restaurant':restaurant_list.get_restaurant_info(),'rest':restaurant_list.get_rest_info(),'owner':owner_list,'branch_list':restaurant_branch_list,'area_list':area_list,'cuisine_list':cuisine_list,'user_img':user_img}
            return render(request,'edit-restaurant-branch.html',data)     
        else:
            print "Go to add Restaurant"
            area_list=AreaFactTable.objects.all()
            cuisine_list=CuisineFactTable.objects.all()
            #cuisine_rest=CuisineRestaurentMap.objects.filter(restaurant_id=rest_obj.restaurant_id)
            return render(request,'my-restaurantform.html',{'area_list':area_list,'cuisine_list':cuisine_list}) 
    except Exception, e:
        data={"error":e}
        return HttpResponse(json.dumps(data),content_type='application/json')


def open_addbooking(request):
    return render_to_response('add-booking.html')  

def open_add_branch(request):
    try: 
        if not request.user.is_authenticated():
            return redirect('/')
           
        owner_list=RestaurantAdmin.objects.get(id=request.session['ownerid'])
        user_img=get_image(owner_obj)
        return render(request,'add-restaurant-branch.html',{'area_list':area_list,'cuisine_list':cuisine_list,'user_img':user_img})  
    except Exception, e:
        data={"error":e}
        return HttpResponse(json.dumps(data),content_type='application/json')

def open_forgot_password(request):
    return render(request,'forgot-password.html')  
   #return render_to_response('forgot-password.html')  

def open_change_password(request):
    try:
        if not request.user.is_authenticated():
            return redirect('/')
        
        owner_obj=RestaurantAdmin.objects.get(id=request.session['ownerid']) 
        user_img=get_image(owner_obj)  
        data={'user_img':user_img}    
        return render(request,'change_password_new.html',data)  
    except Exception,e:
        data={"error":e}
        return HttpResponse(json.dumps(data),content_type='application/json')  
   

def open_booking_confirm(request):
    return render_to_response('booking-confirmation.html')  

def open_old_bookings(request):
    try:
        if not request.user.is_authenticated():
            return redirect('/')
        return render(request,'view-old-bookings.html')
    except Exception,e:
        data={"error":e}
        return HttpResponse(json.dumps(data),content_type='application/json')

def open_restaurant_branch(request):
    try:
        if not request.user.is_authenticated():
            return redirect('/')
        
        area_list=AreaFactTable.objects.all()
        cuisine_list=CuisineFactTable.objects.all()
        owner_obj=RestaurantAdmin.objects.get(id=request.session['ownerid'])
        user_img=get_image(owner_obj)
        return render(request,'add-restaurant-branch.html',{'area_list':area_list,'cuisine_list':cuisine_list,'user_img':user_img})
    except Exception,e:
        data={"error":e}
        return HttpResponse(json.dumps(data),content_type='application/json')

def open_register(request):
    return render(request,'register.html')

@csrf_exempt
def admin_register(request):
    if request.method=="POST":
        #pdb.set_trace()
        try:
            first_name = request.POST['fname']
            last_name = request.POST['lname']
            username = request.POST['email']	
            contact = request.POST['contact']
            password = request.POST['pass']
            cpassword = request.POST['cpass']
            #owner_id=RestaurantOwner.owner_id
            print username 
            print password
            
            check_obj=RestaurantAdmin.objects.get(username=username);
            if check_obj:
                return render_to_response('register_restaurant.html',{'error_msg':'User Already Exist!'},context_instance=RequestContext(request))
##               data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'User Already Exist'}                 
##               return render_to_response('register.html', {'errors':data})
        except User.DoesNotExist:
            if password == cpassword:
                    admin_obj=RestaurantAdmin(
                        username = username,
                        password = password,
                        first_name = first_name,
                        last_name = last_name,				
                        restaurant_admin_first_name = first_name,
                        restaurant_admin_last_name = last_name,
                        restaurant_admin_email = username,
                        restaurant_admin_contactno = request.POST['contact'],			
                        )
                    admin_obj.is_staff=True
                    admin_obj.set_password(password)
                    admin_obj.save()			
                    register_conformation_mail_to_restaurant(username)
                    register_conformation_mail_to_dealmonk(request.session['login_user'],username)
                    data= {'error_msg':'Restaurant Added Successfully!'}
                    #return render(request,'register_restaurant.html')
                    return render_to_response('register_restaurant.html',{'error_msg':'Restaurant Added Successfully!'},context_instance=RequestContext(request))
                    #return render_to_response('register_restaurant.html',{'error_msg':'Successfully Added Restaurant!'})	        
            else:
                    data= {'error_msg' : 'Passwords do not match!'}
                    return render_to_response('register_restaurant.html', data)           
        except MySQLdb.OperationalError, e:
            print 'DB :',e
            data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'Internal Server Error '}
        except Exception, e:
            print 'BIG :',e
            data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'Internal Server Error '}
    return render_to_response('register_restaurant.html', {'errors':data})

@csrf_exempt
def admin_login(request):
    #pdb.set_trace()
    try:
        username = request.POST['username']
        password = request.POST['password']
        #owner_id=RestaurantOwner.owner_id
        print username 
        print password        
        #print owner_id
        user = authenticate( username=username, password=password)
        #print user.owner_id
        print user
        if user is not None:
            if user.is_active:
                login(request,user)
                request.session['login_user']=user.username
                request.session['full_name']=user.first_name+" "+user.last_name
                request.session['login_status']=True
                request.session["ownerid"]=user.id
                print request.session["ownerid"]
                if user.is_superuser:
                    return render(request,'register_restaurant.html') #render_to_response('dashboard.html')      
                else:
                    owner_obj=RestaurantAdmin.objects.get(id=request.session['ownerid'])
                    if owner_obj.restaurant_admin_has_restaurant==1:
                        user_img=get_image(owner_obj) 
                        rest_obj=Restaurant.objects.get(restaurant_admin_id=owner_obj)
                        print rest_obj
                        rest_bk_list= RestaurantBooking.objects.filter(restaurant_id=rest_obj,restaurant_booking_date=datetime.now())           
                        print '----------'
                        print rest_bk_list
                        offer_list=Offer_map.objects.filter(restaurant_id=rest_obj,offer_map_date=datetime.now())           
                        data={'rest_bk_list':rest_bk_list,'offer_list':offer_list,'user_img':user_img}
                        return render(request,'dashboard.html',data)
                    else:
                        return render(request,'dashboard.html')
            else:
                data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'User Is Not Active'}
        else:
            data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'Invalid Username or Password'}
    except User.DoesNotExist:
        data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'User Not Exit'}
    except MySQLdb.OperationalError, e:
        print 'DB :',e
        data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'Internal Server Error '}
    except Exception, e:
        print 'BIG :',e
        data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'Internal Server Error '}
    return render_to_response('index.html', {'errors':data})

def signOutAdmin(request):
    logout(request)
    return redirect('home')

def register_conformation_mail_to_restaurant(username):
    #pdb.set_trace()
    gmail_user = "training.tungsten@gmail.com"
    gmail_pwd = "team@tungsten74#"
    FROM = 'Dealmonk App Admin'
    TO = []
    
    try:
        TO.append(username)

        TEXT = "Dear Sir,"+'\n'+"Congratulations!"+'\n'+"Your restaurant has been successfully registered."+'\n'+'\n'+"We are delighted to welcome you to the DealMonk family!"+'/n'+"We will be looking forward to helping you get the most out of DealMonk App & will be in touch with you to assist in designing the best promotions for your restaurant."+'\n'+'\n'+"Please feel free to email us at support@deal-monk.com or call us @ +9199479344 or +918527238292 for any questions or issues you face. We will be more than happy to assist you!"+'\n'+'\n'+"Regards,"+'\n'+"DealMonk Team"
        
        SUBJECT = "Registration successful!"
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

def register_conformation_mail_to_dealmonk(deal_monk_username,registered_user):
    #pdb.set_trace()
    gmail_user = "training.tungsten@gmail.com"
    gmail_pwd = "team@tungsten74#"
    FROM = 'Dealmonk App Admin'
    TO = []
    
    try:
        TO.append(deal_monk_username)

        TEXT = "You Have Successfully Added "+registered_user
        SUBJECT = "Register Conformation Mail"
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

@csrf_exempt
def change_password(request):
    #pdb.set_trace()
    try:   
        password = request.POST['old_password']
        new_password = request.POST['new_password']
        user_name=request.session['login_user']    
        user = authenticate(username=user_name, password=password)
        if user is not None:            
            user.set_password(new_password)
            user.save()
            data= {'error_msg':'Your password has been changed successfully!'}
        else:
            data= {'error_msg':'Old password does not match!'}
        print '--------------------------------------------------'
    except Exception, e:
        print '----------Exception---------------'
        print e
        data={'error_msg':'Server Exception!'}
    return render_to_response('change_password_new.html',data,context_instance=RequestContext(request))    



def forgot_password(request):
    #pdb.set_trace()
    try:
        user_name = request.POST['user_id']
        user_obj=User.objects.get(username=user_name) 
        if user_obj is not None:            
            user_obj.set_password('dealmonk_user') 
            user_obj.save()
            email_for_forgot_pwd(user_name,'dealmonk_user')
            data= {'error_msg':'Reset password sent to your entered email id'}
        else:
            data= {'error_msg':'Please enter registered email id'}
        print '--------------------------------------------------'
    except Exception, e:
        print '----------Exception---------------'
        print e
        data={'error_msg':'Server Exception!'}
    return render_to_response('forgot-password.html',data,context_instance=RequestContext(request))    
   

def email_for_forgot_pwd(username,registered_user):
    #pdb.set_trace()
    gmail_user = "training.tungsten@gmail.com"
    gmail_pwd = "team@tungsten74#"
    FROM = 'Dealmonk App Admin'
    TO = []
    
    try:
        TO.append(username)
        TEXT = "Your password has been changed, your new password is "+registered_user
        SUBJECT = "Reset Password"
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

@csrf_exempt
def upload_admin_image(request):
    #pdb.set_trace()
    
##    try:
##        user_name = request.POST['user_name']
##        admin_obj =RestaurantAdmin.objects.get(username=user_name)
##        print request.FILES['pic']
##        admin_obj.restaurant_admin_profile_pic= request.FILES['pic']
##        admin_obj.save()        
##        image=SERVER_PATH+admin_obj.restaurant_admin_profile_pic.url
##        data={'success':'true','image':image}        
##    except Exception, e:
##        print e
##        data={'success':'error','image':SERVER_PATH+'/media/admin-image.png'}   
##    return redirect('/promotions/')


    try:
        user_name = request.POST['user_name']
        admin_obj =RestaurantAdmin.objects.get(username=user_name)
        print request.FILES['image']
        admin_obj.restaurant_admin_profile_pic= request.FILES['image']
        admin_obj.save()        
        image=SERVER_PATH+admin_obj.restaurant_admin_profile_pic.url
        data={'success':'true','image':image}        
    except Exception, e:
        print e
        data={'success':'error'} 
    return HttpResponse(json.dumps(data),content_type='application/json')

def open_restaurant_menu(request):
    owner_obj=RestaurantAdmin.objects.get(id=request.session['ownerid'])
    user_img=get_image(owner_obj)
    if owner_obj.restaurant_admin_has_restaurant==1:
        rest_obj = Restaurant.objects.get(restaurant_admin_id=owner_obj)
        
        menu_list = CategoriesFactTable.objects.exclude(category_name='Create Your Own')
        cat_obj= CategoriesFactTable.objects.get(category_name='Create Your Own')
        menu_item_list = MenuItemTable.objects.filter(restaurant_id=rest_obj)
        menu_obj = MenuItemTable.objects.filter(restaurant_id=rest_obj,category_id=cat_obj)
        items, item_ids = [], []
        clr = ["btn-primary", "btn-warning", "btn-success", "btn-danger"]
        i=0;
        words=[]
        m_list= []
        for menu in menu_list:
            if menu.category_name not in item_ids:
                str = menu.category_name
                words= str.split( )
                #words = words[0]+""+words[1]
                if len(words)>1:
                    #words = words[0]+""+words[1]
                    str = re.sub("\s","", str)
                    print str
                else:
                    str = words[0]
                    print str
                m_list.append({'m_id':menu.category_id,'m_category':menu.category_name,'color':clr[i],'str':str})
                i=i+1;
                if i>3:
                    i=0;
                item_ids.append(menu.category_name)


        for item in menu_obj:
            if item.category_name not in item_ids:
                str = item.category_name
                words= str.split( )
                #words = words[0]+""+words[1]
                if len(words)>1:
                    #words = words[0]+""+words[1]
                    str = re.sub("\s","", str)
                    print str
                else:
                    str = words[0]
                    print str
                items.append({'m_id':item.category_id,'m_category':item.category_name,'color':clr[i],'str':str})
                i=i+1;
                if i>3:
                    i=0;    
                item_ids.append(item.category_name)
        
        data = {'m_list':m_list,'rest_obj':rest_obj,'menu_item_list':menu_item_list,'menu_obj':items,'user_img':user_img}        
        return render(request,'menu.html',data)
    else:
        area_list = AreaFactTable.objects.all()     
        cuisine_list=CuisineFactTable.objects.all()
        data={'area_list':area_list,'cuisine_list':cuisine_list,'error_msg':'Please add restaurant details first and then proceed to Menu!','user_img':user_img}
        return render(request,'my-restaurantform.html',data)
