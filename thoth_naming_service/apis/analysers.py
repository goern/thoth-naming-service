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

from werkzeug.exceptions import BadRequest, ServiceUnavailable  # pragma: no cover
from flask import request  # pragma: no cover
from flask_restplus import Namespace, Resource, fields, reqparse  # pragma: no cover

ns = Namespace('analysers', description='Thoth: Naming Service')  # pragma: no cover

parser = reqparse.RequestParser()
parser.add_argument('tag', type=str, help='Used for filtering the Analyser Images')


# FIXME hardcored database of analyser images! ;)
DATABASE = {
    'apiVersion': 'v1',
    'kind': 'List',
    'items': [
        {
            'apiVersion': 'v1',
            'kind': 'Analyser',
            'metadata': {
                'name': 'fridex/thoth-package-extract',
                'description': 'This analyser will extract RPM and Python Packages. DEPRECATED: use "thoth/package-extract"'
            },
            'dockerImageRepository': 'docker://docker.io/fridex/thoth-package-extract:latest'
        },
        {
            'apiVersion': 'v0alpha0',
            'kind': 'Analyser',
            'metadata': {
                'name': 'thoth/package-extract',
                'description': 'This analyser will extract RPM and Python Packages.'
            },
            'dockerImageRepository': 'docker-registry.default.svc:5000/thoth-test-core/package-extract',
            'tag': 'default'
        }
    ]
}


@ns.route('/')
@ns.expect(parser)
@ns.response(200, '')
@ns.response(404, 'Analyser Image Not Found')
class AnalyserList(Resource):
    """Lists of all currently known Analysers"""
    @ns.doc('list_analysers')
    def get(self):
        """List all Analysers"""

        args = parser.parse_args()

        if args['tag'] is not None:
            for item in DATABASE['items']:
                if 'tag' in item.keys():
                    if item['tag'] == args['tag']:
                        return item
                    else:
                        return None, 404

        return DATABASE
