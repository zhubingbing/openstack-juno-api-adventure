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

q = cinder.backups.create('e25fa8ac-4db7-4a08-805f-d10a6abf7b20',
                          container='volumebackups',
                          name='vol-backup-1',
                          description='fdsfsdfsdfs')
print type(q), dir(q)

