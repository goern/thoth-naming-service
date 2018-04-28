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

from flask_restplus import Api

import thoth_naming_service
from .analysers import ns as analysers_v1
from .solvers import ns as solvers_v1

api = Api(version=thoth_naming_service.__version__, title='Thoth: Naming Service',
          description=thoth_naming_service.__description__, doc='/openapi/')

api.add_namespace(analysers_v1, path='/api/v0alpha0/analyzers')
api.add_namespace(solvers_v1, path='/api/v0alpha0/solvers')
