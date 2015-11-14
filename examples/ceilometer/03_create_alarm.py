#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import json
import time

import keystoneclient
import keystoneclient.auth.identity.v3
import keystoneclient.session
import keystoneclient.v3.client
import ceilometerclient.client

import local_settings

keystone = keystoneclient.v3.client.Client(auth_url=local_settings.auth_url_v3,
                                           username=local_settings.username,
                                           password=local_settings.password,
                                           unscoped=True)
keystone.management_url = local_settings.auth_url_v3
projects = keystone.projects.list(user=keystone.user_id)
auth = keystoneclient.auth.identity.v3.Token(auth_url=local_settings.auth_url_v3,
                                             token=keystone.auth_token,
                                             project_id=projects[0].id)
session = keystoneclient.session.Session(auth=auth)

client = ceilometerclient.client.get_client('2',
                                            token=session.get_token(),
                                            ceilometer_url='http://10.202.19.11:8777')
alarm = client.alarms.create(name='alarm-' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '%.06f' % time.time(),
                             description='description fdsfds',
                             type='threshold',
                             enabled=False,
                             repeat_action=True,
                             project_id=projects[0].id,
                             threshold_rule={
                                 'comparison_operator': 'gt',
                                 'evaluation_period': 2,
                                 'exclude_outliners': False,
                                 'meter_name': 'cpu_util',
                                 'period': 600,
                                 'query': [],
                                 'statistic': 'avg',
                                 'threshold': 70.0,
                             },
                             alarm_actions=['http://127.0.0.1:8000/ops/alarms'])
print alarm

