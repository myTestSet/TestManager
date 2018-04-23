# -*- coding:utf-8 -*-

import json

from django.conf import settings
from django.contrib.auth import login
from super_test_manager import settings
from .constants import USERINFO_COOKIE_KEY



def get_user_info(user):
    '''
    获取用户姓名和用户 id
    :param user:
    :return:
    '''
    return {
        'user_id': user.id,
        'user_name':user.username,
    }


def update_userinfo_session_cookie(request, response, user):
    user_info = get_user_info(user)
    request.session['user_info'] = user_info
    request.session.set_expiry(settings.SESSION_COOKIE_AGE)
    request.session.save()
    response.set_cookie(
        USERINFO_COOKIE_KEY,
        json.dumps(user_info),
        expires=settings.SESSION_COOKIE_AGE,
    )


def do_login(request, user):
    '''
    登录动作
    :param request:
    :return:
    '''
    user.backend = settings.AUTHENTICATION_BACKENDS[0]
    login(request, user)
