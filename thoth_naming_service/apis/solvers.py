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

import urllib3

import daiquiri

from werkzeug.exceptions import BadRequest, ServiceUnavailable  # pragma: no cover
from flask import request  # pragma: no cover
from flask_restplus import Namespace, Resource, fields, reqparse  # pragma: no cover

from thoth_naming_service import get_solver_image_list


DEBUG = bool(os.getenv('DEBUG', False))


daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger('api')

if DEBUG:
    logger.setLevel(level=logging.DEBUG)
else:
    logger.setLevel(level=logging.INFO)


ns = Namespace('solvers', description='Thoth: Naming Service')  # pragma: no cover


# FIXME hardcored database of analyser images! ;)
DATABASE = {
    'apiVersion': 'v1',
    'kind': 'List',
    'items': [
        {
            'apiVersion': 'v0alpha0',
            'kind': 'SolverImage',
            'metadata': {
                'name': 'solver-26-job',
                'description': 'This Solver is based on Fedora 26'
            },
            'dockerImageRepository': 'docker-registry.default.svc:5000/thoth-test-core/solver-f26-job',
        },
        {
            'apiVersion': 'v0alpha0',
            'kind': 'SolverImage',
            'metadata': {
                'name': 'solver-27-job',
                'description': 'This Solver is based on Fedora 27'
            },
            'dockerImageRepository': 'docker-registry.default.svc:5000/thoth-test-core/solver-f27-job',
        },
    ]
}


@ns.route('/')
@ns.response(200, '')
class SolverList(Resource):
    """Lists of all currently known Solvers"""
    @ns.doc('list_solvers')
    def get(self):
        """List all Solvers"""

        solver_images = []

        try:
            for image in get_solver_image_list():
                name = next(iter(image))

                solver_images.append({
                    'apiVersion': 'v0alpha0',
                    'kind': 'SolverImage',
                    'metadata': {
                        'name': name,
                        'description': 'NotImplemented'
                    },
                    'dockerImageRepository': image[name],
                })

        except urllib3.exceptions.MaxRetryError as e:
            logger.error(e)
            return None, 504

        return {
            'apiVersion': 'v1',
            'kind': 'List',
            'items': solver_images
        }
