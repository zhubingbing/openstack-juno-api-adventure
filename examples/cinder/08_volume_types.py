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

q = cinder.volume_types.list(search_opts={'name': 'ssd'})  # name不能过滤，是cinderclient的问题吗？
print json.dumps([{'id': i.id, 'extra_specs': i.extra_specs, 'is_public': i.is_public,
                   'name': i.name} for i in q])

