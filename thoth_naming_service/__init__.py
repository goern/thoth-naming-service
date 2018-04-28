import os

__version__ = '0.3.0'
__description__ = 'Thoth: Naming Service, ask me if you want to find things...'
__git_commit_id__ = os.getenv('OPENSHIFT_BUILD_COMMIT', 'local')

from .solvers import get_solver_image_list
from .analysers import get_analyser_image_list
