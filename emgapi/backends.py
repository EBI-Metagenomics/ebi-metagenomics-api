#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2019 EMBL - European Bioinformatics Institute
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import requests

from django.conf import settings

from django.contrib.auth.models import User


class EMGBackend:
    """ENA Auth backend
    """

    supports_anonymous_user = False
    supports_object_permissions = False

    def authenticate(self, request, username=None, password=None):
        ena_auth_url = settings.EMG_BACKEND_AUTH_URL
        data = {
            'authRealms': ['SRA'],
            'rememberMe': False,
            'username': username,
            'password': password,
        }
        req = requests.post(ena_auth_url, json=data)
        resp = req.json()
        if req.status_code == 200:
            if resp.get('authenticated', False):
                user, created = User.objects.get_or_create(
                    username__iexact=username,
                    defaults={'username': username.lower()}
                )
                return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
