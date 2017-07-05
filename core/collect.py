# More or less generic benchmark output parser
import csv
import re
import os
import config


def parse_time(s):
    """
    Parse time as reported by /usr/bin/time, i.e., [hours:]minutes:seconds"
    and return it as number of seconds (float )
    Return 0.0 if does not match
    """
    s = s.replace(',', '.')  # due to different locales

    pattern = r"((\d{0,2}):)?(\d{1,2}):(\d{1,2}\.\d{1,5})"
    match = re.search(pattern, s)
    if not match:
        return 0.0

    hours = int(match.group(2)) if match.group(2) else 0
    minutes = int(match.group(3))
    seconds = float(match.group(4))

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


def get_run_argument(name, line):
    return re.search(r'%s: (\S+);' % name, line).group(1)


def collect(exp_name, result_file="", full_output_file="", user_parameters={}):
    """
    Main collection function
    """
    # set default directories, if not given
    if not result_file and not full_output_file:
        data = os.environ['DATA_PATH'] + '/results'
        full_output_file = "%s/%s/%s.log" % (data, exp_name, exp_name)
        result_file = "%s/%s/raw.csv" % (data, exp_name)

    # get current measurement parameters
    conf = config.Config()
    parameters = conf.parsed_data[os.environ['STATS_COLLECT']]
    parameters.update(user_parameters)

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
