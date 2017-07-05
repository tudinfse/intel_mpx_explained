from __future__ import print_function

import logging
from os import environ as env
from os import devnull
from subprocess import check_call, check_output, STDOUT, CalledProcessError, TimeoutExpired, DEVNULL

DEBUG   = env["DEBUG"]
VERBOSE = env["VERBOSE"]
TIMEOUT = env["TIMEOUT"]
BUILD_MSG = "[build] name: %s; type: %s;"
FNULL = open(devnull, 'w')


# common functions
def build_libc(t, conf_path):
    logging.debug(BUILD_MSG % ('libc', t))
    if not env.get("EXP_NO_BUILD"):
        c("make BUILD_TYPE=" + t + " -I " + conf_path + " -C " + "libc")


def build_benchmark(b, t, makefile, build_path):
    logging.debug(BUILD_MSG % (b, t))
    common_makefiles = env["PROJ_ROOT"] + "/makefiles"

    if not env.get("EXP_NO_BUILD"):
        quiet = '-s' if not VERBOSE else ''
        threads = env["BUILD_THREADS"]

        try:
            build_cmd = "make -j{0} BUILD_TYPE={1} -I {2} -C {3} {4}".format(threads, t, common_makefiles, makefile, quiet)
            if VERBOSE:
                logging.debug("Build command: " + build_cmd)
            c(build_cmd)
        except CalledProcessError as e:
            logging.error("Could not build the benchmark (exit code = %d). See the error message below." % e.returncode)
            logging.debug(e.output)


def replace_in_file(name, find, replace, ignoreifcontains=False):
    f = open(name, 'r')
    file_data = f.read()
    f.close()

    if ignoreifcontains:
        if replace in file_data:
            return

    new_data = file_data.replace(find, replace)

    f = open(name, 'w')
    f.write(new_data)
    f.close()


# Shortcuts
def c(cmd):
    stderr = FNULL if not VERBOSE else None
    stdin = FNULL if not VERBOSE else None
    check_call(cmd, stderr=stderr, stdin=stdin, shell=True)


def my_check_output(cmd, use_check_call = False):
    logging.debug("Command: " + cmd)

    timeout = None
    if TIMEOUT:
        timeout = int(TIMEOUT)

    try:
        if use_check_call:
            check_call(cmd, shell=True, stdout=DEVNULL, stderr=DEVNULL, timeout=timeout)
            result = b'[[ succesfully ran command via check_call ]]'
        else:
            result = check_output(cmd, shell=True, stderr=STDOUT, timeout=timeout)
    except TimeoutExpired as e:
        logging.error("The benchmark hanged.")
        result = b''
    except CalledProcessError as e:
        logging.error("Could not run the benchmark (exit code = %d). See the error message below." % e.returncode)
        output = e.output.decode("utf-8") if e.output else "No error message"
        logging.debug(output)
        result = b''

    return result.decode("utf-8")
