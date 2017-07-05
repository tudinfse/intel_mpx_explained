"""
Setup the execution environment based on the command line argument
"""

import logging
from os import environ as env

import config


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
        self.debug = debug
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


def set_all_environments(debug=False, verbose=False, env_type='both'):
    """
    Simple wrapper
    """
    Envs = getattr(config.Config(), "environments", [])

    for EnvClass in Envs:
        env_obj = EnvClass(debug, verbose)
        env_obj.setup(env_type)
