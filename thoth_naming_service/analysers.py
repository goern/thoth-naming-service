#!/usr/bin/env python
# -*- coding: utf-8 -*-
#   thoth-naming-service
#   Copyright(C) 2018 Christoph Görn
#
#   This program is free software: you can redistribute it and / or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Thoth: Naming Service, ask me if you want to find things..."""


import os

import openshift.client
from kubernetes.client.rest import ApiException

from thoth_naming_service.utils import get_api_token


KUBERNETES_API_URL = os.getenv(
    'KUBERNETES_API_URL', 'https://kubernetes.default.svc.cluster.local')
KUBERNETES_API_TOKEN = os.getenv('KUBERNETES_API_TOKEN') or get_api_token()
KUBERNETES_VERIFY_TLS = bool(int(os.getenv('KUBERNETES_VERIFY_TLS', "0")))  # FIXME reset to 1


def get_analyser_image_list():
    configuration = openshift.client.Configuration()
    configuration.api_key_prefix['authorization'] = 'Bearer'
    configuration.api_key['authorization'] = KUBERNETES_API_TOKEN
    configuration.host = KUBERNETES_API_URL
    configuration.verify_ssl = KUBERNETES_VERIFY_TLS

    api_instance = openshift.client.ImageOpenshiftIoV1Api(openshift.client.ApiClient(configuration))

    return []  # TODO
