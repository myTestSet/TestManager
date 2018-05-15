# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


from backend import create_idno_tmp, create_idno, create_bankcard
# Create your views here.


def create_id_no(requets):
    '''
    生成身份证号
    :param requets:
    :return:
    '''
    if requets.method == 'GET':
        return render(requets, 'test_util/id_no.html')
    elif requets.method == 'POST':
        birthday = requets.POST['birthday']
        idno_tmp = create_idno_tmp(birthday)
        idno = create_idno(idno_tmp)
        bankcard_no = create_bankcard()
        context = {
            'bankcard_no': bankcard_no,
            'idno': idno
        }
        return render(requets, 'test_util/id_no.html', context)