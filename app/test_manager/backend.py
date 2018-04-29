# -*- coding:utf-8 -*-

from urllib import unquote


def suite_format_data(data):
    '''
    处理请求数据
    :param data:
    :return:
    '''
    data_list = data.split('&')
    sum_list = []
    for i in range(0, len(data_list)):
        sum_list.append(data_list[i].split('='))
    fdict = dict(sum_list)
    request_tmp = unquote(fdict['request'])
    request = {'base_url': request_tmp}
    name = fdict['suite_name']
    variables = []
    variables_tmp = unquote(fdict['variables'].replace('+', '')).split('!@#')
    variables_dict = {variables_tmp[0]: variables_tmp[1]}
    variables.append(variables_dict)
    project_id = fdict['project_id']
    request_dict = {
        'request': request,
        'name': name,
        'variables': variables,
        'project_id': project_id
    }
    return request_dict


def case_format_data(data):
    '''
    处理case请求数据
    :param data:
    :return:
    '''
    pass


