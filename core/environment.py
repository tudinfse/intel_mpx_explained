"""
Setup the execution environment based on the command line argument
"""

import logging
import os
from os import environ as env


CURR_PATH = os.path.dirname(os.path.abspath(__file__))


class Environment(object):
    # these variables will be set only if not set already
    # priority: 0
    default_variables = {}

    # these values will be added to existing ones
    # priority: 1
    updated_variables = {}

    # these variables will be re-written (regardless of the previous value)
    # priority: 2
    forced_variables = {}

    # these variables will be set if experiments are run without re-building
    # priority: 3
    only_run_variables = {}

    # these variables will be set if experiments are build but not run
    # priority: 3
    only_build_variables = {}

    # these variables will be set in the debug mode. They have the highest priority
    # priority: 4
    debug_variables = {}

    def __init__(self, debug=False, verbose=False):
        self.debug   = debug
        self.verbose = verbose
        env["DEBUG"] = "1" if self.debug else ""
        env["VERBOSE"] = "1" if self.verbose else ""

    def setup(self, env_type='both'):
        logging.debug("Setting up the environment. Type: {} - {}".format(self.__class__.__name__, env_type))

        # default
        for var, value in self.default_variables.items():
            current_value = env.get(var)
            env[var] = value if not current_value else current_value

        # updated
        for var, value in self.updated_variables.items():
            current_value = env.get(var)
            env[var] = value if not current_value else current_value + value

        # forced
        for var, value in self.forced_variables.items():
            env[var] = value if value else ""

        # build only
        if env_type == 'build':
            env['EXP_NO_RUN'] = '1'
            for var, value in self.only_build_variables.items():
                env[var] = value

        # run only
        elif env_type == 'run':
            env['EXP_NO_BUILD'] = '1'
            for var, value in self.only_run_variables.items():
                env[var] = value

        # debug
        if self.debug:
            for var, value in self.debug_variables.items():
                env[var] = value


class GenericEnvironment(Environment):
    forced_variables = {}

    updated_variables = {
        'LD_LIBRARY_PATH': '/usr/local/lib64/:/usr/local/lib/:%s/install/libs/' % CURR_PATH,
    }

    default_variables = {
        'COMP_BENCH': CURR_PATH,
        'DATA_PATH': CURR_PATH + '/data/',
        'BIN_PATH': CURR_PATH + '/bin/'
    }

    debug_variables = {}


class MPXEnvironment(Environment):
    default_variables = {
        'CHKP_RT_BNDPRESERVE': '0',  # support of legacy code, i.e. libraries
        'CHKP_RT_MODE': 'stop',  # options: count, stop
        'CHKP_RT_VERBOSE': '0',  # options: 0, 1, 2, 3
        'CHKP_RT_PRINT_SUMMARY': '0',

    }

    only_build_variables = {
        "CHKP_RT_MODE": 'count',
        "CHKP_RT_PRINT_SUMMARY": '0',
    }

    debug_variables = {
        "CHKP_RT_VERBOSE": "2",
    }


class SGXEnvironment(Environment):
    default_variables = {
        'HEAP': '0xF0000',
        'MUSL_VERSION': '1',
        'MUSL_ETHREADS': '4',
        'MUSL_STHREADS': '4',
    }

    only_build_variables = {
        "MUSL_VERSION": '',
    }


class ASanEnvironment(Environment):
    default_variables = {
        'ASAN_OPTIONS': 'verbosity=0:' +
                        'detect_leaks=false:' +
                        'print_summary=true:' +
                        'halt_on_error=true:' +
                        'poison_heap=true:' +
                        'alloc_dealloc_mismatch=0:' +
                        'new_delete_type_mismatch=0:' +
                        'quarantine_size_mb=1',
    }

    only_build_variables = {
        "ASAN_OPTIONS": 'verbosity=0:' +
                        'detect_leaks=false:' +
                        'print_summary=false:' +
                        'halt_on_error=false:' +
                        'poison_heap=false',
    }

    debug_variables = {
        "ASAN_OPTIONS": 'verbosity=1:' +
                        'detect_leaks=false:' +
                        'print_summary=false:' +
                        'halt_on_error=false:' +
                        'poison_heap=false:' +
                        'alloc_dealloc_mismatch=0:' +
                        'new_delete_type_mismatch=0:' +
                        'quarantine_size_mb=1',
    }


def set_all_environments(debug=False, verbose=False, env_type='both'):
    """
    Simple wrapper
    """

    Envs = [
        GenericEnvironment,
        MPXEnvironment,
        SGXEnvironment,
        ASanEnvironment
    ]

    for EnvClass in Envs:
        env_obj = EnvClass(debug, verbose)
        env_obj.setup(env_type)
