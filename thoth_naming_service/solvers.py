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
import logging

import daiquiri

import openshift.client
from kubernetes.client.rest import ApiException
from pprint import pprint


DEBUG = bool(os.getenv('DEBUG', False))
KUBERNETES_API_URL = os.getenv(
    'KUBERNETES_API_URL', 'https://kubernetes.default.svc.cluster.local')
KUBERNETES_API_TOKEN = os.getenv('KUBERNETES_API_TOKEN') or _get_api_token()
KUBERNETES_VERIFY_TLS = bool(int(os.getenv('KUBERNETES_VERIFY_TLS', "0")))  # FIXME reset to 1


daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger('naming_service')

if DEBUG:
    logger.setLevel(level=logging.DEBUG)
else:
    logger.setLevel(level=logging.INFO)


def _get_api_token():
    """Get token to Kubernetes master."""
    try:
        with open('/var/run/secrets/kubernetes.io/serviceaccount/token', 'r') as token_file:
            return token_file.read()
    except FileNotFoundError as exc:
        raise FileNotFoundError("Unable to get service account token, please check that service has "
                                "service account assigned with exposed token") from exc


def get_image_list() -> []:
    """get_image_list() will query the OpenShift ImageStream API to find ImageStream belonging/labeled 'solver'"""

    configuration = openshift.client.Configuration()
    configuration.api_key_prefix['authorization'] = 'Bearer'
    configuration.api_key['authorization'] = KUBERNETES_API_TOKEN
    configuration.host = KUBERNETES_API_URL
    configuration.verify_ssl = KUBERNETES_VERIFY_TLS

    logger.debug(f'querying ImageOpenshiftIoV1 API at {KUBERNETES_API_URL}')

    api_instance = openshift.client.ImageOpenshiftIoV1Api(openshift.client.ApiClient(configuration))

    solver_images = []

    try:
        api_response = api_instance.list_namespaced_image_stream('thoth-test-core', label_selector='component=solver')

        for imagestream in api_response.items:
            solver_images.append({imagestream.metadata.name: imagestream.status.docker_image_repository})

    except ApiException as e:
        print("Exception when calling ImageOpenshiftIoV1Api->list_namespaced_image_stream: %s\n" % e)

    return solver_images


if __name__ == '__main__':
    pprint(get_image_list())
