# -*- coding:utf-8 -*-
# @Author= 'liuzunrui'
# @Time :2018/5/15 下午2:35

import time
from random import choice, randint


def generate_random(lenth):
    date = str(time.time()).split(".")
    lstr = str(date[0]) + str(date[1])
    return lstr[(len(lstr)-lenth):]


def create_idno_tmp(birthday):
    first_bit = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    idno_tmp = choice(first_bit) + generate_random(5) + str(birthday) + generate_random(3)
    return idno_tmp


def create_idno(idno_tmp):
    res = 0
    iW = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    last_bit = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
    for i in range(0, len(idno_tmp)):
        res = res + int(idno_tmp[i]) * iW[i]

    check_right_bit = last_bit[res % 11]
    id_no = idno_tmp + check_right_bit
    return id_no


def create_bankcard():
    card_header_tmp = ['622700', '621488']
    card_header = choice(card_header_tmp)
    res_tmp = ''
    if card_header is '622700':
        for i in range(0, 8):
            res_tmp = res_tmp + str(randint(0, 9))
            res = '99211' + res_tmp
    elif card_header is '621488':
        for i in range(0, 10):
            res_tmp = res_tmp + str(randint(0, 9))
            res = res_tmp
    bankcard_no = card_header + res
    return bankcard_no
