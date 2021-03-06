#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import keystoneclient.auth.identity.v3
import keystoneclient.session
import cinderclient.client

import local_settings

auth = keystoneclient.auth.identity.v3.Password(auth_url=local_settings.auth_url_v3,
                                                username=local_settings.username,
                                                password=local_settings.password,
                                                user_domain_name='Default',
                                                project_domain_name='Default',
                                                project_name=local_settings.tenant_name)
session = keystoneclient.session.Session(auth=auth)
cinder = cinderclient.client.Client('2', session=session)

q = cinder.quota_classes.get('default')
print type(q)
print dir(q)
ret = {}
for attr in dir(q):
    if attr.startswith('_'):
        continue
    if attr == 'id':
        continue
    if attr in ('HUMAN_ID', 'NAME_ATTR', 'get', 'human_id', 'is_loaded',
                'manager', 'set_loaded', 'update'):
        continue
    obj = getattr(q, attr)
    ret[attr] = obj
print json.dumps(ret)

