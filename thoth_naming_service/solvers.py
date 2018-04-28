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
from pprint import pprint


KUBERNETES_API_URL = os.getenv(
    'KUBERNETES_API_URL', 'https://kubernetes.default.svc.cluster.local')
KUBERNETES_API_TOKEN = os.getenv('KUBERNETES_API_TOKEN') or _get_api_token()
KUBERNETES_VERIFY_TLS = bool(int(os.getenv('KUBERNETES_VERIFY_TLS', "0")))  # FIXME reset to 1


def _get_api_token():
    """Get token to Kubernetes master."""
    try:
        with open('/var/run/secrets/kubernetes.io/serviceaccount/token', 'r') as token_file:
            return token_file.read()
    except FileNotFoundError as exc:
        raise FileNotFoundError("Unable to get service account token, please check that service has "
                                "service account assigned with exposed token") from exc


def solvers() -> []:
    configuration = openshift.client.Configuration()
    configuration.api_key_prefix['authorization'] = 'Bearer'
    configuration.api_key['authorization'] = KUBERNETES_API_TOKEN
    configuration.host = KUBERNETES_API_URL
    configuration.verify_ssl = KUBERNETES_VERIFY_TLS

    api_instance = openshift.client.ImageOpenshiftIoV1Api(openshift.client.ApiClient(configuration))

    solver_images = []

    try:
        api_response = api_instance.list_namespaced_image_stream('thoth-test-core', label_selector='component=solver')

        for imagestream in api_response.items:
            solver_images.append({
                'name': imagestream.metadata.name,
                'dockerImageRepository': imagestream.status.docker_image_repository
            })

    except ApiException as e:
        print("Exception when calling ImageOpenshiftIoV1Api->list_namespaced_image_stream: %s\n" % e)

    return solver_images


if __name__ == '__main__':
    pprint(solvers())
