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

import re

@csrf_exempt
def insert_restaurant_menu(request):
    print "========vikas kumawat=========="
    
    try:
        print request.POST
    #print request.POST['start_time']
        rest_id = request.POST['rest_id'] 
        print rest_id
        cat_name = request.POST['menu_name']
        cat_obj = CategoriesFactTable.objects.get(category_name='Create Your Own')
        cat_id = cat_obj.category_id
        print cat_id
        print "Menu is inserting"
        rest_obj=Restaurant.objects.get(restaurant_id=rest_id)
        menu_obj = MenuItemTable(
                restaurant_id=rest_obj,
                category_id=cat_obj,
                category_name=cat_name,
                menu_item_name=cat_name,
                menu_item_price="00",
                menu_item_type="VEG",
                menu_item_create_date=datetime.datetime.now(),
                menu_item_create_by=request.session['login_user'],
                menu_item_update_date=datetime.datetime.now(),
                menu_item_update_by=request.session['login_user'],
                menu_item_status=0,
        )
        menu_obj.save()
        
        btn = '<input type="button" class="btn btn-w-m btn-success" onclick="m(this.value,this.id,'+str(rest_id)+')" id="'+str(cat_id)+'" value="'+cat_name+'"></input>'       
        data = {'success':'true','btn':btn}
        #data = {'success':'true'}
        #print btn
    except Exception,e:
        print e
        data = {'success':'error'}            
    return HttpResponse(json.dumps(data),content_type='application/json')

@csrf_exempt
def add_menu_item(request):
    print "adding items"
    print request.POST
    try:
        if request.method=='POST': 
                rest_obj=Restaurant.objects.get(restaurant_id=request.POST['rest_id'])
                cat_obj=CategoriesFactTable.objects.get(category_id=request.POST['menu_id'])
                menu_obj= MenuItemTable(
                        category_id=cat_obj,
                        restaurant_id=rest_obj,
                        category_name=cat_obj.category_name,
                        menu_item_name=request.POST['item_name'],
                        menu_item_price=request.POST['item_price'],
                        menu_item_type=request.POST['type_name'],
                        menu_item_create_date=datetime.datetime.now(),
                        menu_item_create_by=request.session['login_user'],
                        menu_item_update_date=datetime.datetime.now(),
                        menu_item_update_by=request.session['login_user'],
                        )
                print "Inserting Restaurant Branch....."
                menu_obj.save()
    except Exception,e:
        print e
        data = {'error':'Internal Error!'}
        return render(request,'menu.html',data)
    return redirect('/restaurant_menu/')


def get_menu_details(request):       
    try:
        menu_list=''        
        rest_id = request.GET.get('rest_id')
        cat_id = request.GET.get('cat_id')
        cat_name = request.GET.get('cat_name')
        print cat_name
        cat_id = int(re.search(r'\d+', cat_id).group())
        #print cat_id
        rest_obj=Restaurant.objects.get(restaurant_id=rest_id)
        cat_obj=CategoriesFactTable.objects.get(category_id=cat_id)
        menu_list=MenuItemTable.objects.filter(category_id=cat_id,restaurant_id=rest_id,menu_item_status=1,category_name=cat_name)
        
        #print menu_list
        menu_item_list=[]
        for menu in menu_list:
            if menu.menu_item_type == "VEG":
                share = '<form id="menu_form" method="post" role="form" class="form-inline"><div id="m_f'+str(menu.menu_item_id)+'"><input type="hidden" id="ct_id" name="ct_id" value="'+str(cat_id)+'"/><input type="hidden" id="rt_id" name="rt_id" value="'+str(menu.restaurant_id)+'"/><input type="hidden" id="m_id" name="m_id" value="'+str(menu.menu_item_id)+'"/><div class="col-sm-1"></div><div class="form-group"><input class="form-control food" id="it_name'+str(menu.menu_item_id)+'" name="it_name" placeholder="Item Name" type="text" disabled="true" value="'+menu.menu_item_name+'" style="width: 380px;" maxlength="45"/></div>&nbsp;&nbsp;&nbsp;<div class="form-group"><input class="form-control food" id="it_price'+str(menu.menu_item_id)+'" name="it_price" placeholder="Item Price" type="text" disabled="true" value="'+str(menu.menu_item_price)+'" style="width: 200px;" maxlength="3"/></div>&nbsp;<div class="form-group"><input type="hidden" class="form-control food" id="it_type'+str(menu.menu_item_id)+'" name="it_type" placeholder="Item Type" disabled="true" value="'+menu.menu_item_type+'"/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<button id="v_btn'+str(menu.menu_item_id)+'" class="btn btn-primary btn-circle" type="button">V</button>&nbsp;&nbsp;<button id="gf_btn'+str(menu.menu_item_id)+'" class="btn btn-warning btn-outline btn-circle" type="button">GF</button>&nbsp;&nbsp;<button id="nv_btn'+str(menu.menu_item_id)+'" class="btn btn-danger btn-outline btn-circle" type="button">NV</button>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input id="ed'+str(menu.menu_item_id)+'" onclick="edit(this.id,'+str(menu.menu_item_id)+');" type="button" class="btn btn-outline btn-primary" value="Edit"/>&nbsp; &nbsp;<input id="del'+str(menu.menu_item_id)+'" onclick="delt(this.id,'+str(menu.menu_item_id)+');" type="button" class="btn btn-outline btn-danger" value="Delete"/></div><input type="hidden" id="e_id'+str(menu.menu_item_id)+'" name="ct_id" value="0"/></form>'
            
            elif menu.menu_item_type == "NON-VEG":
                share = '<form id="menu_form" method="post" role="form" class="form-inline"><div id="m_f'+str(menu.menu_item_id)+'"><input type="hidden" id="ct_id" name="ct_id" value="'+str(cat_id)+'"/><input type="hidden" id="rt_id" name="rt_id" value="'+str(menu.restaurant_id)+'"/><input type="hidden" id="m_id" name="m_id" value="'+str(menu.menu_item_id)+'"/><div class="col-sm-1"></div><div class="form-group"><input class="form-control food" id="it_name'+str(menu.menu_item_id)+'" name="it_name" placeholder="Item Name" type="text" disabled="true" value="'+menu.menu_item_name+'" style="width: 380px;" maxlength="45"/></div>&nbsp;&nbsp;&nbsp;<div class="form-group"><input class="form-control food" id="it_price'+str(menu.menu_item_id)+'" name="it_price" placeholder="Item Price" type="text" disabled="true" value="'+str(menu.menu_item_price)+'" style="width: 200px;" maxlength="3"/></div>&nbsp;<div class="form-group"><input type="hidden" class="form-control food" id="it_type'+str(menu.menu_item_id)+'" name="it_type" placeholder="Item Type" disabled="true" value="'+menu.menu_item_type+'"/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<button id="v_btn'+str(menu.menu_item_id)+'" class="btn btn-primary btn-outline btn-circle" type="button">V</button>&nbsp;&nbsp;<button id="gf_btn'+str(menu.menu_item_id)+'" class="btn btn-outline btn-warning btn-circle" type="button">GF</button>&nbsp;&nbsp;<button id="nv_btn'+str(menu.menu_item_id)+'" class="btn btn-danger btn-circle" type="button">NV</button>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input id="ed'+str(menu.menu_item_id)+'" onclick="edit(this.id,'+str(menu.menu_item_id)+');" type="button" class="btn btn-outline btn-primary" value="Edit"/>&nbsp; &nbsp;<input id="del'+str(menu.menu_item_id)+'" onclick="delt(this.id,'+str(menu.menu_item_id)+');" type="button" class="btn btn-outline btn-danger" value="Delete"/></div><input type="hidden" id="e_id'+str(menu.menu_item_id)+'" name="ct_id" value="0"/></form>'
            
            else :
                share = '<form id="menu_form" method="post" role="form" class="form-inline"><div id="m_f'+str(menu.menu_item_id)+'"><input type="hidden" id="ct_id" name="ct_id" value="'+str(cat_id)+'"/><input type="hidden" id="rt_id" name="rt_id" value="'+str(menu.restaurant_id)+'"/><input type="hidden" id="m_id" name="m_id" value="'+str(menu.menu_item_id)+'"/><div class="col-sm-1"></div><div class="form-group"><input class="form-control food" id="it_name'+str(menu.menu_item_id)+'" name="it_name" placeholder="Item Name" type="text" disabled="true" value="'+menu.menu_item_name+'" style="width: 380px;" maxlength="45"/></div>&nbsp;&nbsp;&nbsp;<div class="form-group"><input class="form-control food" id="it_price'+str(menu.menu_item_id)+'" name="it_price" placeholder="Item Price" type="text" disabled="true" value="'+str(menu.menu_item_price)+'" style="width: 200px;" maxlength="3"/></div>&nbsp;<div class="form-group"><input type="hidden" class="form-control food" id="it_type'+str(menu.menu_item_id)+'" name="it_type" placeholder="Item Type" disabled="true" value="'+menu.menu_item_type+'"/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<button id="v_btn'+str(menu.menu_item_id)+'" class="btn btn-primary btn-outline btn-circle" type="button">V</button>&nbsp;&nbsp;<button id="gf_btn'+str(menu.menu_item_id)+'" class="btn btn-warning btn-circle" type="button">GF</button>&nbsp;&nbsp;<button id="nv_btn'+str(menu.menu_item_id)+'" class="btn btn-danger btn-outline btn-circle" type="button">NV</button>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input id="ed'+str(menu.menu_item_id)+'" onclick="edit(this.id,'+str(menu.menu_item_id)+');" type="button" class="btn btn-outline btn-primary" value="Edit"/>&nbsp; &nbsp;<input id="del'+str(menu.menu_item_id)+'" onclick="delt(this.id,'+str(menu.menu_item_id)+');" type="button" class="btn btn-outline btn-danger" value="Delete"/><input type="hidden" id="e_id'+str(menu.menu_item_id)+'" name="ct_id" value="0"/></form>'
            
            data={  
                    'success':'true',
                    'share':share
                 }
            menu_item_list.append(data)

        data = {'data':menu_item_list}
        #print data
    except Exception,e:
        print e
        data={'success':'false'}
    return HttpResponse(json.dumps(data),content_type='application/json')  


@csrf_exempt
def update_menu_details(request):
    print "adding items"
    #'rest_id': rest_id ,'cat_id':cat_id,'menu_id':menu_id,'it_name':it_name,'it_price':it_price,'it_type':it_type
    try:
        menu_id = request.POST.get('menu_id')
        it_name = request.POST.get('it_name')
        it_price = request.POST.get('it_price')
        it_type = request.POST.get('it_type')
        menu_obj = MenuItemTable.objects.get(menu_item_id=menu_id)
        menu_obj.menu_item_name = it_name
        menu_obj.menu_item_price = it_price
        menu_obj.menu_item_type = it_type
        menu_obj.save()
        print 'Menu item updated!' 
        #data={'success':'true'}               
    except Exception,e:
        print e        
        #data={'success':'false'}
    return HttpResponse(json.dumps({'success':'true'}),content_type='application/json')

 
@csrf_exempt
def delete_menu_details(request):
    print 'Deleting Menu item!' 
    try:
        menu_id = request.POST.get('menu_id')
        menu_obj = MenuItemTable.objects.get(menu_item_id=menu_id)
        menu_obj.menu_item_status = "0"
        menu_obj.save()
        print 'Menu item deleted!' 
        #data={'success':'true'}               
    except Exception,e:
        print e        
        #data={'success':'false'}
    return HttpResponse(json.dumps({'success':'true'}),content_type='application/json')
    
@csrf_exempt
def add_menu_details(request):
    print 'Adding Menu item!'
    
    try:
        #'cat_id':cat_id,'rest_id':rest_id,'it_name':it_name,'it_price':it_price,'it_type':it_type
        cat_id = request.POST.get('cat_id')
        cat_id = int(re.search(r'\d+', cat_id).group())
        rest_id = request.POST.get('rest_id')
        it_name = request.POST.get('it_name')
        it_price = request.POST.get('it_price')
        it_type = request.POST.get('it_type')
        cat_name = request.POST.get('cat_name')
        rest_obj=Restaurant.objects.get(restaurant_id=rest_id)
        cat_obj=CategoriesFactTable.objects.get(category_id=cat_id)
        menu_obj= MenuItemTable(
                category_id=cat_obj,
                restaurant_id=rest_obj,
                category_name=cat_name,
                menu_item_name=it_name,
                menu_item_price=it_price,
                menu_item_type=it_type,
                menu_item_create_date=datetime.datetime.now(),
                menu_item_create_by=request.session['login_user'],
                menu_item_update_date=datetime.datetime.now(),
                menu_item_update_by=request.session['login_user'],
                )
                #print "Inserting Restaurant Branch....."
        menu_obj.save()
        
        if menu_obj.menu_item_type == "VEG":
            share = '<form id="menu_form" method="post" role="form" class="form-inline"><div id="m_f'+str(menu_obj.menu_item_id)+'"><input type="hidden" id="ct_id" name="ct_id" value="'+str(cat_id)+'"/><input type="hidden" id="rt_id" name="rt_id" value="'+str(menu_obj.restaurant_id)+'"/><input type="hidden" id="m_id" name="m_id" value="'+str(menu_obj.menu_item_id)+'"/><div class="col-sm-1"></div><div class="form-group"><input class="form-control food" id="it_name'+str(menu_obj.menu_item_id)+'" name="it_name" placeholder="Item Name" type="text" disabled="true" value="'+menu_obj.menu_item_name+'" style="width: 380px;" maxlength="45"/></div>&nbsp;&nbsp;&nbsp;<div class="form-group"><input class="form-control food" id="it_price'+str(menu_obj.menu_item_id)+'" name="it_price" placeholder="Item Price" type="text" disabled="true" value="'+str(menu_obj.menu_item_price)+'" style="width: 200px;" maxlength="3"/></div>&nbsp;<div class="form-group"><input type="hidden" class="form-control food" id="it_type'+str(menu_obj.menu_item_id)+'" name="it_type" placeholder="Item Type" disabled="true" value="'+menu_obj.menu_item_type+'"/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<button id="v_btn'+str(menu_obj.menu_item_id)+'" class="btn btn-primary btn-circle" type="button">V</button>&nbsp;&nbsp;<button id="gf_btn'+str(menu_obj.menu_item_id)+'" class="btn btn-warning btn-outline btn-circle" type="button">GF</button>&nbsp;&nbsp;<button id="nv_btn'+str(menu_obj.menu_item_id)+'" class="btn btn-danger btn-outline btn-circle" type="button">NV</button>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input id="ed'+str(menu_obj.menu_item_id)+'" onclick="edit(this.id,'+str(menu_obj.menu_item_id)+');" type="button" class="btn btn-outline btn-primary" value="Edit"/>&nbsp; &nbsp;<input id="del'+str(menu_obj.menu_item_id)+'" onclick="delt(this.id,'+str(menu_obj.menu_item_id)+');" type="button" class="btn btn-outline btn-danger" value="Delete"/></div><input type="hidden" id="e_id'+str(menu_obj.menu_item_id)+'" name="ct_id" value="0"/></form>'
            
        elif menu_obj.menu_item_type == "NON-VEG":
            share = '<form id="menu_form" method="post" role="form" class="form-inline"><div id="m_f'+str(menu_obj.menu_item_id)+'"><input type="hidden" id="ct_id" name="ct_id" value="'+str(cat_id)+'"/><input type="hidden" id="rt_id" name="rt_id" value="'+str(menu_obj.restaurant_id)+'"/><input type="hidden" id="m_id" name="m_id" value="'+str(menu_obj.menu_item_id)+'"/><div class="col-sm-1"></div><div class="form-group"><input class="form-control food" id="it_name'+str(menu_obj.menu_item_id)+'" name="it_name" placeholder="Item Name" type="text" disabled="true" value="'+menu_obj.menu_item_name+'" style="width: 380px;" maxlength="45"/></div>&nbsp;&nbsp;&nbsp;<div class="form-group"><input class="form-control food" id="it_price'+str(menu_obj.menu_item_id)+'" name="it_price" placeholder="Item Price" type="text" disabled="true" value="'+str(menu_obj.menu_item_price)+'" style="width: 200px;" maxlength="3"/></div>&nbsp;<div class="form-group"><input type="hidden" class="form-control food" id="it_type'+str(menu_obj.menu_item_id)+'" name="it_type" placeholder="Item Type" disabled="true" value="'+menu_obj.menu_item_type+'"/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<button id="v_btn'+str(menu_obj.menu_item_id)+'" class="btn btn-primary btn-outline btn-circle" type="button">V</button>&nbsp;&nbsp;<button id="gf_btn'+str(menu_obj.menu_item_id)+'" class="btn btn-outline btn-warning btn-circle" type="button">GF</button>&nbsp;&nbsp;<button id="nv_btn'+str(menu_obj.menu_item_id)+'" class="btn btn-danger btn-circle" type="button">NV</button>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input id="ed'+str(menu_obj.menu_item_id)+'" onclick="edit(this.id,'+str(menu_obj.menu_item_id)+');" type="button" class="btn btn-outline btn-primary" value="Edit"/>&nbsp; &nbsp;<input id="del'+str(menu_obj.menu_item_id)+'" onclick="delt(this.id,'+str(menu_obj.menu_item_id)+');" type="button" class="btn btn-outline btn-danger" value="Delete"/></div><input type="hidden" id="e_id'+str(menu_obj.menu_item_id)+'" name="ct_id" value="0"/></form>'
            
        else :
            share = '<form id="menu_form" method="post" role="form" class="form-inline"><div id="m_f'+str(menu_obj.menu_item_id)+'"><input type="hidden" id="ct_id" name="ct_id" value="'+str(cat_id)+'"/><input type="hidden" id="rt_id" name="rt_id" value="'+str(menu_obj.restaurant_id)+'"/><input type="hidden" id="m_id" name="m_id" value="'+str(menu_obj.menu_item_id)+'"/><div class="col-sm-1"></div><div class="form-group"><input class="form-control food" id="it_name'+str(menu_obj.menu_item_id)+'" name="it_name" placeholder="Item Name" type="text" disabled="true" value="'+menu_obj.menu_item_name+'" style="width: 380px;" maxlength="45"/></div>&nbsp;&nbsp;&nbsp;<div class="form-group"><input class="form-control food" id="it_price'+str(menu_obj.menu_item_id)+'" name="it_price" placeholder="Item Price" type="text" disabled="true" value="'+str(menu_obj.menu_item_price)+'" style="width: 200px;" maxlength="3"/></div>&nbsp;<div class="form-group"><input type="hidden" class="form-control food" id="it_type'+str(menu_obj.menu_item_id)+'" name="it_type" placeholder="Item Type" disabled="true" value="'+menu_obj.menu_item_type+'"/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<button id="v_btn'+str(menu_obj.menu_item_id)+'" class="btn btn-primary btn-outline btn-circle" type="button">V</button>&nbsp;&nbsp;<button id="gf_btn'+str(menu_obj.menu_item_id)+'" class="btn btn-warning btn-circle" type="button">GF</button>&nbsp;&nbsp;<button id="nv_btn'+str(menu_obj.menu_item_id)+'" class="btn btn-danger btn-outline btn-circle" type="button">NV</button>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input id="ed'+str(menu_obj.menu_item_id)+'" onclick="edit(this.id,'+str(menu_obj.menu_item_id)+');" type="button" class="btn btn-outline btn-primary" value="Edit"/>&nbsp; &nbsp;<input id="del'+str(menu_obj.menu_item_id)+'" onclick="delt(this.id,'+str(menu_obj.menu_item_id)+');" type="button" class="btn btn-outline btn-danger" value="Delete"/></div><input type="hidden" id="e_id'+str(menu_obj.menu_item_id)+'" name="ct_id" value="0"/></form>'
        
        print 'Menu item inserted!' 
        data={'success':'true','share':share}
        print menu_obj.menu_item_id               
    except Exception,e:
        print e        
        #data={'success':'false'}
    return HttpResponse(json.dumps(data),content_type='application/json')
