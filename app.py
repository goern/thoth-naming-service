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

from flask import Flask
from flask import jsonify
from flask import request
from flask.helpers import make_response

import requests

from prometheus_client import CONTENT_TYPE_LATEST
from prometheus_client import Counter
from prometheus_client import Histogram
from prometheus_client import core
from prometheus_client import generate_latest

import thoth_naming_service
from thoth_naming_service.apis import api

DEBUG = bool(os.getenv('DEBUG', False))

daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger('nameing-service')

if DEBUG:
    logger.setLevel(level=logging.DEBUG)
else:
    logger.setLevel(level=logging.INFO)


app = Flask(__name__)
app.config.SWAGGER_UI_JSONEDITOR = True
app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
app.logger.setLevel(logging.DEBUG)

api.init_app(app)


@app.route('/readiness')
def api_readiness():
    return jsonify({
        'name': 'Thoth Naming Service',
        'version': thoth_naming_service.__version__
    }), 200, {'ContentType': 'application/json'}


@app.route('/liveness')
def api_liveness():
    return jsonify({
        'name': 'Thoth Build Analysers',
        'version': thoth_naming_service.__version__
    }), 200, {'ContentType': 'application/json'}


@app.route('/schema')
def print_api_schema():
    return jsonify(api.__schema__)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=DEBUG)
