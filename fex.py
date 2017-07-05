#!/usr/bin/env python3
from __future__ import print_function

import logging
import os
import re
from argparse import ArgumentParser
from importlib import import_module
from subprocess import check_call, STDOUT, Popen, CalledProcessError

import coloredlogs
import cpuinfo
import platform

import config
from core.environment import Environment, set_all_environments


# config is needed everywhere
conf = config.Config()


def set_logging(verbose=False):
    os.environ['COLOREDLOGS_LOG_FORMAT'] = '%(asctime)-15s %(levelname)-8s %(message)s'
    coloredlogs.install(
        level=logging.INFO if not verbose else logging.DEBUG,
        datefmt="%m-%d %H:%M:%S"
    )

    logging.addLevelName(21, 'RUNNER')
    logging.addLevelName(22, 'BUILDER')
    logging.addLevelName(23, 'SCRIPT')


def get_arguments():
    """
    Parse command line arguments
    :return Namespace: parsed arguments
    """
    parser = ArgumentParser(description='')
    subparsers = parser.add_subparsers(help='sub-command help', dest='subparser_name')

    parser.add_argument(
        '-v', '--verbose',
        choices=['1', '2', '3'],
        required=False,
        help='Verbosity level: defines how much information to show.'
             '(-v 1 - [default] basic info;'
             '-v 2 - not implemented;'
             '-v 3 - full experiment description, including HW parameters, compilers and flags, etc.)'
    )

    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        required=False,
        help='Debug mode: compile with debug info (but still with all optimizations enabled) and set helpful environmental variables.'
    )

    # parser for installing benchmarks
    parser_install = subparsers.add_parser('install', help='download and install all benchmarks')
    parser_install.add_argument(
        '-n', '--names',
        nargs='*',
        help="List of program names to be installed"
    )

    # parser for processing logs
    parser_collect = subparsers.add_parser('collect', help='collect statistics based on received results')
    parser_collect.add_argument(
        '-n', '--names',
        nargs='*',
        help='Names of experiments to get collect from'
    )
    parser_collect.add_argument(
        '--stats',
        type=str,
        choices=list(conf.stats_action.keys()),
        default='perf',
        help='Statistics tool'
    )

    # parser for building plots
    parser_plot = subparsers.add_parser('plot', help='build plot based on received results')
    parser_plot.add_argument(
        '-n', '--names',
        nargs='*',
    )
    parser_plot.add_argument(
        '-t', '--plot_type',
        required=True,
        help='Type of plot to build.'
    )
    parser_plot.add_argument(
        '-f', '--file',
        type=str,
        default='',
        help='Input csv file with results.'
    )

    # parser for running performance tests
    parser_perf = subparsers.add_parser('run', help='Run an experiment')
    parser_perf.add_argument(
        '-n', '--names',
        nargs='+',
        help="Names of experiments to run"
    )
    parser_perf.add_argument(
        '-r', '--num_runs',
        type=str,
        default='1',
        help="How much times to run the experiments (results will be averaged on the collection stage)"
    )
    parser_perf.add_argument(
        '-m', '--num_threads',
        nargs='+',
        default='1',
        help='Maximum number of threads (multiple values possible)'
    )
    parser_perf.add_argument(
        '-t', '--types',
        required=True,
        nargs='+',
        help='Build type (multiple values possible)'
    )
    parser_perf.add_argument(
        '--stats',
        type=str,
        choices=list(conf.stats_action.keys()),
        default='perf',
        help='Measurement tool'
    )
    parser_perf.add_argument(
        '--no-build',
        action='store_true',
        required=False,
        help='Don\'t build benchmarks (previous build is used, if any)'
    )
    parser_perf.add_argument(
        '--no-run',
        action='store_true',
        required=False,
        help='Don\'t run the experiments (only build)'
    )
    parser_perf.add_argument(
        '--no-clean',
        action='store_true',
        required=False,
        help='Don\'t delete the previous build'
    )
    parser_perf.add_argument(
        '--singlethreaded_build',
        action='store_true',
        required=False,
        help='Disable multithreading during the build stage'
    )
    parser_perf.add_argument(
        '-b', '--benchmark_name',
        default='',
        help='Run only one benchmark from the benchmark suite'
    )
    parser_perf.add_argument(
        '--timeout',
        required=False,
        help='Time limit for executing a single run'
    )
    parser_perf.add_argument(
        '-i', '--input',
        choices=['native', 'test'],
        default="native",
        help='Input type: native - normal run, test - fast run with small inputs'
    )

    args = parser.parse_args()
    return args


class CLIEnvironment(Environment):
    def __init__(self, cli_args, *args, **kwargs):
        super(CLIEnvironment, self).__init__(*args, **kwargs)

        # multithreading
        if getattr(cli_args, "singlethreaded_build", ''):
            self.forced_variables["BUILD_THREADS"] = '1'
        else:
            self.forced_variables["BUILD_THREADS"] = '8'

        # execution parameters
        if cli_args.subparser_name in ['run', 'collect']:
            self.forced_variables.update({
                'STATS_ACTION': conf.stats_action[cli_args.stats],
                'STATS_COLLECT': cli_args.stats,
            })

        if cli_args.subparser_name == 'plot':
            if cli_args.file == "" and len(cli_args.names) == 1:
                    cli_args.file = os.environ["DATA_PATH"] + '/results/' + cli_args.names[0] + '/raw.csv'
            self.forced_variables.update({
                'PLOT_TYPE': cli_args.plot_type,
                'PLOT_FILE': cli_args.file,
            })

        if cli_args.subparser_name == 'run':
            self.forced_variables.update({
                'NUM_RUNS': cli_args.num_runs,
                'NUM_THREADS': ' '.join(cli_args.num_threads),
                'TYPES': ' '.join(cli_args.types),
                'REBUILD': '' if cli_args.no_clean else '1',
                'TIMEOUT': cli_args.timeout,
            })


def exec_scripts(path, name_pattern):
    """
    Runs scripts which match name_patten in path
    :param str path:
    :param str name_pattern:
    """
    patten = re.compile(name_pattern)
    for file in os.listdir(path):
        if re.match(patten, file):
            proc = Popen(path + "/" + file, stderr=STDOUT, shell=True)
            out, err = proc.communicate()
            return True
    return False


def run_python_module(exp_name, file_name, benchmark_name=None):
    try:
        module = import_module("experiments.%s.%s" % (exp_name, file_name))
        output = module.main(benchmark_name) if benchmark_name else module.main()
    except ImportError as e:
        logging.error("Probably, file experiments/%s/%s.py not found" % (exp_name, file_name))
        raise e

    return output


class Manager:
    """
    Main management point
    """

    def __init__(self, args):
        logging.info("Creating a manager")

        self.names = args.names
        self.benchmark_name = args.benchmark_name if args.subparser_name == 'run' else ''

        self.verbose = str(args.verbose) if args.verbose else ''
        self.debug = str(args.debug) if args.debug else ''
        if self.debug:
            logging.warning("Debug mode is on. These measurements most probably will be incorrect!")

    def set_configuration(self, args):
        conf.input_type = getattr(args, "input", "native")

        # if verbosity level is set to 3, also output all experimental parameters
        if self.verbose == '3':
            self.print_hw_parameters(args)

    def set_environment(self, args):
        cli_env = CLIEnvironment(args, self.debug, self.verbose)
        cli_env.setup()

        if getattr(args, "no_run", False):
            set_all_environments(self.debug, self.verbose, 'build')
        elif getattr(args, "no_build", False):
            set_all_environments(self.debug, self.verbose, 'run')
        else:
            set_all_environments(self.debug, self.verbose, 'both')

    def start(self, action):
        """
        Do the specified action
        """
        if action == 'install':
            for name in self.names:
                logging.info('Installing %s' % name)
                check_call("mkdir -p %s/build/" % os.environ["PROJ_ROOT"], shell=True)
                found = exec_scripts("install/compilers/", "%s.(sh|py)" % name)
                if not found:
                    found = exec_scripts("install/benchmarks/", "%s.(sh|py)" % name)
                if not found:
                    exec_scripts("install/dependencies/", "%s.(sh|py)" % name)
        elif action == 'run':
            for name in self.names:
                logging.info('Running %s' % name)
                self.run_benchmark(name)
        elif action == 'collect':
            for name in self.names:
                run_python_module(exp_name=name, file_name='collect')
        elif action == 'plot':
            for name in self.names:
                try:
                    run_python_module(exp_name=name, file_name='plot', benchmark_name=os.environ["PLOT_TYPE"])
                except CalledProcessError as e:
                    logging.error(
                        "Could not build the plot (exit code = %d). Error message:" % e.returncode)
                    logging.error(e.output)

    def run_benchmark(self, name):
        # prepare the result directory
        try:
            os.makedirs(os.environ['DATA_PATH'] + '/results/' + name)
        except os.error:  # if directory already exist - ignore
            pass

        # run
        run_python_module(exp_name=name, file_name='run', benchmark_name=self.benchmark_name)

        # collect
        logging.info("Collecting data")
        run_python_module(exp_name=name, file_name='collect')

    def print_hw_parameters(self, args):
        msg = "Experiment parameters:\n"

        info = cpuinfo.get_cpu_info()
        msg += "CPU: {0} ({1} cores)\n".format(info['brand'], info['count']) + \
               "Architecture: {0}\n".format(platform.machine()) +\
               "L2 size: {0}\n".format(info['l2_cache_size']) +\
               "Platform: {0}\n\n".format(platform.platform()) +\
               "Environment variables:\n{0}\n\n".format(os.environ) +\
               "Command line arguments:\n{0}\n\n".format(args.__dict__)

        logging.info(msg)


def main():
    args = get_arguments()
    set_logging(args.verbose)

    manager = Manager(args)
    manager.set_environment(args)
    manager.set_configuration(args)
    manager.start(action=args.subparser_name)


if __name__ == '__main__':
    main()
