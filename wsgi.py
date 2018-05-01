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
import time
import logging

import daiquiri

from flask import Flask, Response, jsonify, request
from flask.helpers import make_response

import requests

from prometheus_client import CONTENT_TYPE_LATEST
from prometheus_client import Counter, Histogram
from prometheus_client import core, generate_latest

import thoth_naming_service
from thoth_naming_service.apis import api

DEBUG = bool(os.getenv('DEBUG', False))

FLASK_REQUEST_LATENCY = Histogram('flask_request_latency_seconds', 'Flask Request Latency',
                                ['method', 'endpoint'])
FLASK_REQUEST_COUNT = Counter('flask_request_count', 'Flask Request Count',
                              ['method', 'endpoint', 'http_status'])

daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger('nameing-service')

if DEBUG:
    logger.setLevel(level=logging.DEBUG)
else:
    logger.setLevel(level=logging.INFO)


def before_request():
    request.start_time = time.time()


def after_request(response):
    request_latency = time.time() - request.start_time
    FLASK_REQUEST_LATENCY.labels(request.method, request.path).observe(request_latency)
    FLASK_REQUEST_COUNT.labels(request.method, request.path, response.status_code).inc()

    return response


application = Flask(__name__)
application.config.SWAGGER_UI_JSONEDITOR = True
application.config.SWAGGER_UI_DOC_EXPANSION = 'list'
application.logger.setLevel(logging.DEBUG)

api.init_app(application)

application.before_request(before_request)
application.after_request(after_request)


@application.route('/readiness')
def api_readiness():
    return jsonify({
        'name': thoth_naming_service.__description__,
        'version': f'v{thoth_naming_service.__version__}+{thoth_naming_service.__git_commit_id__}'
    }), 200, {'ContentType': 'application/json'}


@application.route('/liveness')
def api_liveness():
    return jsonify({
        'name': thoth_naming_service.__description__,
        'version': f'v{thoth_naming_service.__version__}+{thoth_naming_service.__git_commit_id__}'
    }), 200, {'ContentType': 'application/json'}


@application.route('/schema')
def print_api_schema():
    return jsonify(api.__schema__)


@application.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    logger.info(f'Thoth Naming Service v{thoth_naming_service.__version__}+{thoth_naming_service.__git_commit_id__}')
    application.run(host='0.0.0.0', port=8080, debug=DEBUG)
