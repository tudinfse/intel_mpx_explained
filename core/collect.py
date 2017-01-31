# More or less generic benchmark output parser
import csv
import re
import os
import logging

data = os.environ['DATA_PATH'] + '/results'


def parse_time(s):
    """
    Parse time as reported by /usr/bin/time, e.g., "0:00.21" (which is 0.21 seconds)
    and return it as number of seconds (float )
    Return 0.0 if does not match
    """
    s = s.replace(',', '.')  # due to different locales

    pattern = r"(\d{0,2}):?(\d{1,2}):(\d{1,2}\.\d{1,5})"
    match = re.search(pattern, s)
    if not match:
        return 0.0

    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2))
    seconds = float(match.group(3))

    return hours * 3600 + minutes * 60 + seconds


def get_float_from_string(s):
    s = s.replace(',', '.')         # due to different locales
    pattern = r'\d{1,10}\.\d{1,10}'
    match = re.search(pattern, s)
    if match:
        match = match.group(0)
        result = float(match)
        return result
    return 0.0


def get_int_from_string(s):
    s = s.replace('.', '')         # due to different locales
    pattern = r'\d{1,20}'
    match = re.search(pattern, s)
    if match:
        match = match.group(0)
        result = int(match)
        return result
    return 0


def collect(result_file, full_output_file, user_parameters={}, sgx_experiment=False):
    parameters = {}
    if os.environ['STATS_COLLECT'] == 'perf':
        parameters = {
            "cycles"        : ["cycles",            lambda l: get_int_from_string(l)],
            "instructions"  : [" instructions ",    lambda l: get_int_from_string(l)],  # spaces are not to confuse with branch-instructions

            "branch_instructions"   : ["branch-instructions",   lambda l: get_int_from_string(l)],
            "branch_misses"         : ["branch-misses",         lambda l: get_int_from_string(l)],

            "major_faults": ["major-faults", lambda l: get_int_from_string(l)],
            "minor_faults": ["minor-faults", lambda l: get_int_from_string(l)],

            "dtlb_loads"        : ["dTLB-loads",        lambda l: get_int_from_string(l)],
            "dtlb_load_misses"  : ["dTLB-load-misses",  lambda l: get_int_from_string(l)],
            "dtlb_stores"       : ["dTLB-stores",       lambda l: get_int_from_string(l)],
            "dtlb_store_misses" : ["dTLB-store-misses", lambda l: get_int_from_string(l)],

            "time"              : ["seconds time elapsed", lambda l: get_float_from_string(l)],
        }

    elif os.environ['STATS_COLLECT'] == 'perf_cache':
        parameters = {
            "l1_dcache_loads":        ["L1-dcache-loads",       lambda l: get_int_from_string(l)],
            "l1_dcache_load_misses":  ["L1-dcache-load-misses", lambda l: get_int_from_string(l)],
            "l1_dcache_stores":       ["L1-dcache-stores",      lambda l: get_int_from_string(l)],
            "l1_dcache_store_misses": ["L1-dcache-store-misses",      lambda l: get_int_from_string(l)],

            "llc_loads":          ["LLC-loads",         lambda l: get_int_from_string(l)],
            "llc_load_misses":    ["LLC-load-misses",   lambda l: get_int_from_string(l)],
            "llc_store_misses":   ["LLC-store-misses",  lambda l: get_int_from_string(l)],
            "llc_stores":         ["LLC-stores",        lambda l: get_int_from_string(l)],

            "time":               ["seconds time elapsed", lambda l: get_float_from_string(l)],
            "instructions":       [" instructions ",    lambda l: get_int_from_string(l)],
        }

    elif os.environ['STATS_COLLECT'] == 'time':
        parameters = {
            "time"      :    ["Elapsed (wall clock) time",  lambda l: parse_time(l)],
            "user_time" :    ["User time (seconds)",        lambda l: get_float_from_string(l)],
            "sys_time"  :    ["System time (seconds)",      lambda l: get_float_from_string(l)],

            "major_faults": ["Major (requiring I/O) page faults",       lambda l: get_int_from_string(l)],
            "minor_faults": ["Minor (reclaiming a frame) page faults",  lambda l: get_int_from_string(l)],

            "voluntary_context_switches":   ["Voluntary context switches",   lambda l: get_int_from_string(l)],
            "involuntary_context_switches": ["Involuntary context switches", lambda l: get_int_from_string(l)],

            "maxsize": ["Maximum resident set size", lambda l: get_int_from_string(l)],
        }

    elif os.environ['STATS_COLLECT'] == 'mpxcount':
        parameters = {
            "instructions": ["program: total", lambda l: get_int_from_string(l)],

            "memory_reads":  ["program: memreads",  lambda l: get_int_from_string(l)],
            "memory_writes": ["program: memwrites", lambda l: get_int_from_string(l)],

            "bndmk": ["program: bndmk", lambda l: get_int_from_string(l)],
            "bndcl": ["program: bndcl", lambda l: get_int_from_string(l)],
            "bndcu": ["program: bndcu", lambda l: get_int_from_string(l)],

            "bndldx": ["program: bndldx", lambda l: get_int_from_string(l)],
            "bndstx": ["program: bndstx", lambda l: get_int_from_string(l)],

            "bndmovreg": ["program: bndmovreg", lambda l: get_int_from_string(l)],
            "bndmovmem": ["program: bndmovmem", lambda l: get_int_from_string(l)],
        }

    elif os.environ['STATS_COLLECT'] == 'perf_instr':
        parameters = {
            "instructions"  : [" instructions ",    lambda l: get_int_from_string(l)],  # spaces are not to confuse with branch-instructions
            "instructions:u"  : [" instructions:u ",    lambda l: get_int_from_string(l)],
            "instructions:k"  : [" instructions:k ",    lambda l: get_int_from_string(l)],

            "mpx_new_bounds_table "   : ["mpx:mpx_new_bounds_table ",   lambda l: get_int_from_string(l)],
            "time": ["seconds time elapsed", lambda l: get_float_from_string(l)],
        }

    elif os.environ['STATS_COLLECT'] == 'perf_ports':
        parameters = {
            "UOPS_EXECUTED.CORE"  : ["r02B1",          lambda l: get_int_from_string(l)],
            "PORT_0"  : ["r01A1", lambda l: get_int_from_string(l)],
            "PORT_1"  : ["r02A1", lambda l: get_int_from_string(l)],
            "PORT_2"  : ["r04A1", lambda l: get_int_from_string(l)],
            "PORT_3"  : ["r08A1", lambda l: get_int_from_string(l)],
            "PORT_4"  : ["r10A1", lambda l: get_int_from_string(l)],
            "PORT_5"  : ["r20A1", lambda l: get_int_from_string(l)],
            "PORT_6"  : ["r40A1", lambda l: get_int_from_string(l)],
            "PORT_7"  : ["r80A1", lambda l: get_int_from_string(l)],
        }

    parameters.update(user_parameters)

    if sgx_experiment:
        # add SGX-related stats
        parameters["sgxtime"] = ["[SGX ENCLAVE STATS] enclave_time", lambda l: get_float_from_string(l)]
        parameters["sgxmem"]  = ["[SGX ENCLAVE STATS] highwatermark_mmaped_mem", lambda l: get_int_from_string(l)]

    # add MPX-related stats
    parameters["mpxbtnum"]  = ["Number of allocated Bounds Tables", lambda l: get_int_from_string(l)]
    parameters["mpxerrors"] = ["Number of bounds violations", lambda l: get_int_from_string(l)]

    with open(full_output_file, 'r') as ffull:
        with open(result_file, 'w') as fres:
            field_names = ['name', 'compiler', 'type', 'threads', 'input'] + list(parameters.keys())
            writer = csv.DictWriter(fres, fieldnames=field_names)
            writer.writeheader()

            values = {i: '' for i in field_names}  # initialize

            for l in ffull.readlines():
                if l.startswith('[run] '):
                    # write previous results (but skip the first run)
                    if values['name']:  # on the first run this variable is not initialized, we use this as indicator
                        writer.writerow(values)

                    # parse results of the next run (custom params are nullified)
                    values['name'] = get_run_argument('name', l)
                    values['compiler'] = get_run_argument('type', l).split('_', 1)[0]
                    values['type'] = get_run_argument('type', l).split('_', 1)[1]
                    values['threads'] = get_run_argument('threads', l)
                    values['input'] = get_run_argument('input', l)
                    for parameter, parser in parameters.items():
                        values[parameter] = ''

                # Custom parameters
                for parameter, parser in parameters.items():
                    key = parser[0]
                    parse_function = parser[1]
                    if key in l:
                        values[parameter] = parse_function(l)
                        break

            # write results form a last measurement
            writer.writerow(values)


def get_run_argument(name, line):
    return re.search(r'%s: (\S+);' % name, line).group(1)

