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

import csv
import json
#importing exceptions
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError


# This is Sign Up from mobile and web
@csrf_exempt
def consumer_register(request):
   # pdb.set_trace()
    try:
        print request
        if request.method == 'POST':
            json_obj=json.loads(request.body)
            consume_email   = json_obj[AppUserConstants.EMAIL_ID]
            password  = json_obj[AppUserConstants.PASS_WORD]
            sign_up_via= json_obj[AppUserConstants.SIGN_UP_VIA]
            first_name = json_obj[AppUserConstants.FIRST_NAME]
            last_name = json_obj[AppUserConstants.FIRST_NAME]
            #_user_nick_name   = json_obj[AppUserConstants.USER_NICK_NAME]
            consumer_contact=json_obj[AppUserConstants.USER_CONTACT]
            #_sign_up_source = json_obj[AppUserConstants.SIGN_UP_SOURCE]
            user_profile_image=json_obj[AppUserConstants.USER_PROFILE_IMAGE]
            #_last_name=json_obj[AppUserConstants.LAST_NAME]
            #_apns_token=json_obj[AppUserConstants.APNS_TOKEN]
            #_user_full_name=json_obj[AppUserConstants.USER_FULL_NAME]

            
            user_obj = UserProfile(
                consume_email   = consume_email,
                sign_up_via = sign_up_via,
                first_name  = _first_name,
                last_name   = _last_name,
                user_full_name   = _user_full_name,
                email    = _email_id,
                user_nick_name=_user_nick_name,
                sign_up_source = _sign_up_source,
                user_profile_image=_user_profile_image
            )
            user_obj.save()
            user_obj.set_password(password)
            user_obj.save()
            data = { ExceptionLabel.SUCCESS : 'true','user_id':user_obj.id}
        else:
            data = { ExceptionLabel.SUCCESS : 'false', ExceptionLabel.ERROR_MESSAGE : 'Invalid Request' }
            print 'hello'
    except Exception, e:
        print 'exception hello',e
        data = { ExceptionLabel.SUCCESS : 'false', ExceptionLabel.ERROR_MESSAGE : 'Invalid Request' }
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def consumer_login(request):
    #pdb.set_trace()
    try:
        if request.method == 'POST':
            json_obj=json.loads(request.body)
            print 'JSON OBJECT : ',json_obj
            user = authenticate(email=json_obj['username'], password= json_obj['password'])
            if user is not None:
                if user.is_active:
                    login(request,user)
                    data= {'success' : 'true', ExceptionLabel.ERROR_MESSAGE:'Successfully Login'}# 'user_info':get_user_profile_editor(user_id)}
                    
                else:
                    data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'User Is Not Active'}
            else:
                data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'Invalid Username or Password'}
        else:
            data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'Invalid Request'}
    except User.DoesNotExist:
        data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'User Not Exit'}
    except MySQLdb.OperationalError, e:
        data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'Internal Server Error '}
    except Exception, e:
        data= {'success' : 'false', ExceptionLabel.ERROR_MESSAGE:'Internal Server Error '}
    return HttpResponse(json.dumps(data), content_type='application/json')

def consumer_logout(request):
    logout(request)
    data = { ExceptionLabel.SUCCESS : 'true'}
    return HttpResponse(json.dumps(data), content_type='application/json')
