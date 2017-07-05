"""
Main configuration file

Warning: this feature (i.e., centralized config file) is still in development
It is going to be largely extended in future
"""
from core.abstract_config import AbstractConfig
from core.collect import get_float_from_string, get_int_from_string, parse_time
from environment import GenericEnvironment, ASanEnvironment, MPXEnvironment, SGXEnvironment


class Config(AbstractConfig):
    """
    Example config

    Note that Config is a singleton
    """

    # ========================
    # Run and Build parameters
    # ========================

    # default input type
    input_type = ""

    # list of used environments
    environments = (
        GenericEnvironment,
        ASanEnvironment,
        MPXEnvironment,
        # SGXEnvironment
    )

    # measurement tools
    stats_action = {
        "perf": "perf stat " +
                "-e cycles,instructions " +
                "-e branch-instructions,branch-misses " +
                "-e major-faults,minor-faults " +
                "-e dTLB-loads,dTLB-load-misses,dTLB-stores,dTLB-store-misses ",
        "perf_cache": "perf stat " +
                      "-e instructions " +
                      "-e L1-dcache-loads,L1-dcache-load-misses " +
                      "-e L1-dcache-stores,L1-dcache-store-misses " +
                      "-e LLC-loads,LLC-load-misses " +
                      "-e LLC-store-misses,LLC-stores ",
        "perf_instr": "perf stat " +
                      "-e instructions " +
                      "-e instructions:u " +
                      "-e instructions:k " +
                      "-e mpx:mpx_new_bounds_table",
        "perf_ports": "perf stat " +  # ports for Intel Skylake!
                      "-e r02B1 " +  # UOPS_EXECUTED.CORE
                      "-e r01A1,r02A1 " +  # ports 0 and 1 (UOPS_DISPATCHED_PORT.PORT_X)
                      "-e r04A1,r08A1 " +  # ports 2 and 3
                      "-e r10A1,r20A1 " +  # ports 4 and 5
                      "-e r40A1,r80A1 ",  # ports 6 and 7
        "time": "/usr/bin/time --verbose",
        "mpxcount": "bin/pin/pin -t bin/pin/mpxinscount.so -o mpxcount.tmp --",
        "none": "",
    }

    # ========================
    # Data preparation
    # ========================

    # Results processing (how data is gathered from raw logs)

    # the format is as follows:
    # name of field in csv file: [ keyword to identify a necessary line in logs, function to process the line]
    parsed_data = {
        "perf": {
            "cycles": ["cycles", lambda l: get_int_from_string(l)],
            "instructions": [" instructions ", lambda l: get_int_from_string(l)],  # spaces are added not to confuse with branch-instructions

            "branch_instructions": ["branch-instructions", lambda l: get_int_from_string(l)],
            "branch_misses": ["branch-misses", lambda l: get_int_from_string(l)],

            "major_faults": ["major-faults", lambda l: get_int_from_string(l)],
            "minor_faults": ["minor-faults", lambda l: get_int_from_string(l)],

            "dtlb_loads": ["dTLB-loads", lambda l: get_int_from_string(l)],
            "dtlb_load_misses": ["dTLB-load-misses", lambda l: get_int_from_string(l)],
            "dtlb_stores": ["dTLB-stores", lambda l: get_int_from_string(l)],
            "dtlb_store_misses": ["dTLB-store-misses", lambda l: get_int_from_string(l)],

            "time": ["seconds time elapsed", lambda l: get_float_from_string(l)],
        },
        "perf_cache": {
            "l1_dcache_loads": ["L1-dcache-loads", lambda l: get_int_from_string(l)],
            "l1_dcache_load_misses": ["L1-dcache-load-misses", lambda l: get_int_from_string(l)],
            "l1_dcache_stores": ["L1-dcache-stores", lambda l: get_int_from_string(l)],
            "l1_dcache_store_misses": ["L1-dcache-store-misses", lambda l: get_int_from_string(l)],

            "llc_loads": ["LLC-loads", lambda l: get_int_from_string(l)],
            "llc_load_misses": ["LLC-load-misses", lambda l: get_int_from_string(l)],
            "llc_store_misses": ["LLC-store-misses", lambda l: get_int_from_string(l)],
            "llc_stores": ["LLC-stores", lambda l: get_int_from_string(l)],

            "time": ["seconds time elapsed", lambda l: get_float_from_string(l)],
            "instructions": [" instructions ", lambda l: get_int_from_string(l)],
        },
        "perf_instr": {
            "instructions": [" instructions ", lambda l: get_int_from_string(l)],
            "instructions:u": [" instructions:u ", lambda l: get_int_from_string(l)],
            "instructions:k": [" instructions:k ", lambda l: get_int_from_string(l)],

            "mpx_new_bounds_table ": ["mpx:mpx_new_bounds_table ", lambda l: get_int_from_string(l)],
            "time": ["seconds time elapsed", lambda l: get_float_from_string(l)],
        },
        "perf_ports": {
            "UOPS_EXECUTED.CORE": ["r02B1", lambda l: get_int_from_string(l)],
            "PORT_0": ["r01A1", lambda l: get_int_from_string(l)],
            "PORT_1": ["r02A1", lambda l: get_int_from_string(l)],
            "PORT_2": ["r04A1", lambda l: get_int_from_string(l)],
            "PORT_3": ["r08A1", lambda l: get_int_from_string(l)],
            "PORT_4": ["r10A1", lambda l: get_int_from_string(l)],
            "PORT_5": ["r20A1", lambda l: get_int_from_string(l)],
            "PORT_6": ["r40A1", lambda l: get_int_from_string(l)],
            "PORT_7": ["r80A1", lambda l: get_int_from_string(l)],
        },
        "time": {
            "time": ["Elapsed (wall clock) time", lambda l: parse_time(l)],
            "user_time": ["User time (seconds)", lambda l: get_float_from_string(l)],
            "sys_time": ["System time (seconds)", lambda l: get_float_from_string(l)],

            "major_faults": ["Major (requiring I/O) page faults", lambda l: get_int_from_string(l)],
            "minor_faults": ["Minor (reclaiming a frame) page faults", lambda l: get_int_from_string(l)],

            "voluntary_context_switches": ["Voluntary context switches", lambda l: get_int_from_string(l)],
            "involuntary_context_switches": ["Involuntary context switches", lambda l: get_int_from_string(l)],

            "maxsize": ["Maximum resident set size", lambda l: get_int_from_string(l)],
        },
        "mpxcount": {
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
        },
        "none": {},
    }

    # Results aggregation (what means to calculate)

    # the format is as follows:
    # type: (what column to aggregate, what columns to keep untouched)
    aggregated_data = {
        "perf": (["time"], ["compiler", "type", "name", "input", "threads"]),
        "multi": (["time"], ["compiler", "type", "name", "input", "threads"]),
        "perfstacked": (["time"], ["compiler", "type", "name", "input", "threads"]),
        "mem": (["maxsize"], ["compiler", "type", "name", "input", "threads"]),
        "tput": (["tput", "lat"], ["compiler", "type", "name", "num_clients", "input", "threads"]),
        "instr": (["instructions"], ["compiler", "type", "name", "input", "threads"]),
        "mpxcount": (
            ["bndldx", "bndstx", "bndmovreg", "bndmovmem", "bndcu", "bndmk", "bndcl", "instructions", "memory_reads", "memory_writes"],
            ["compiler", "type", "name", "input", "threads"]
        ),
        "cache": (
            ["instructions", "l1_dcache_loads", "l1_dcache_load_misses", "l1_dcache_stores", "l1_dcache_store_misses", "llc_loads", "llc_load_misses", "llc_stores", "llc_store_misses"],
            ["compiler", "type", "name", "input", "threads"]
        ),
        "misc_stat": (
            ["instructions", "dtlb_stores", "dtlb_store_misses", "dtlb_load_misses", "dtlb_loads", "branch_misses", "branch_instructions"],
            ["compiler", "type", "name", "input", "threads"]
        ),
        "ku_instr": (
            ["instructions", "instructions:u", "instructions:k"],
            ["compiler", "type", "name", "input", "threads"]
        ),
        "native_mem_access": (
            ["instructions", "l1_dcache_loads", "l1_dcache_stores"],
            ["compiler", "type", "name", "input", "threads"]
        ),
        "ipc": (
            ["instructions", "cycles"],
            ["compiler", "type", "name", "input", "threads"]
        ),
        "mpx_feature_perf": (["time"], ["compiler", "type", "name", "input", "threads"]),
        "mpx_feature_mem": (["maxsize"], ["compiler", "type", "name", "input", "threads"]),
    }

    # ========================
    # Plotting
    # ========================
    build_names = {
        "long": {
            "clang-native": "Native (Clang)",
            "safecode-enabled": "SAFECode (Clang)",
            "safecode-native": "Native (SAFECode)",
            "clang-asan": "ASan (Clang)",
            "softbound-enabled": "SoftBound (Clang)",
            "softbound-native": "Native (SoftBound)",
            "icc-native": "Native (ICC)",
            "icc-mpx_no_narrow_bounds_only_write": "MPX n.n.b. o.w. (ICC)",
            "icc-mpx_no_narrow_bounds": "MPX n.n.b. (ICC)",
            "icc-mpx_only_write": "MPX o.w. (ICC)",
            "icc-mpx": "MPX (ICC)",
            "icc-ptr": "Pointer Checker (ICC)",

            "gcc-native": "Native (GCC)",
            "gcc-mpx_no_narrow_bounds_only_write": "MPX n.n.b. o.w. (GCC)",
            "gcc-mpx_no_narrow_bounds": "MPX n.n.b. (GCC)",
            "gcc-mpx_only_write": "MPX o.w. (GCC)",
            "gcc-mpx": "MPX (GCC)",
            "gcc-asan": "ASan (GCC)",
            "gcc-asan_only_write": "ASan o.w. (GCC)",
        },
        "short": {
            "clang-native": "Native (Clang)",
            "safecode-enabled": "SAFECode",
            "safecode-native": "Native (SAFECode)",
            "clang-asan": "ASan",
            "softbound-enabled": "SoftBound",
            "softbound-native": "Native (SoftBound)",

            "icc-native": "Native (ICC)",
            "icc-mpx_no_narrow_bounds_only_write": "MPX (ICC)",
            "icc-mpx_no_narrow_bounds": "MPX (ICC)",
            "icc-mpx_only_write": "MPX (ICC)",
            "icc-mpx": "MPX (ICC)",
            "icc-ptr": "Pointer Checker (ICC)",

            "gcc-native": "Native (GCC)",
            "gcc-mpx_no_narrow_bounds_only_write": "MPX (GCC)",
            "gcc-mpx_no_narrow_bounds": "MPX (GCC)",
            "gcc-mpx_only_write": "MPX (GCC)",
            "gcc-mpx": "MPX (GCC)",
            "gcc-asan": "ASan",
            "gcc-asan_only_write": "ASan",
        },
        "tiny": {
            "Native (Clang)": r"$N$",
            "SAFECode (Clang)": r"$C$",
            "ASan (Clang)": r"$A$",
            "SoftBound (Clang)": r"$B$",

            "Native (ICC)": r"$N$",
            "MPX n.n.b. (ICC)": r"$I$",
            "MPX o.w. (ICC)": r"$\bar{I}$",
            "MPX (ICC)": r"$I$",

            "Native (GCC)": r"$N$",
            "MPX n.n.b. (GCC)": r"$G$",
            "MPX o.w. (GCC)": r"$\bar{G}$",
            "MPX (GCC)": r"$G$",
            "ASan (GCC)": r"$A$",
        },
        "empty": {
            "clang-native": "",
            "safecode-enabled": "",
            "clang-asan": "",
            "softbound-enabled": "",

            "icc-native": "",
            "icc-mpx_no_narrow_bounds_only_write": "",
            "icc-mpx_no_narrow_bounds": "",
            "icc-mpx_only_write": "",
            "icc-mpx": "",

            "gcc-native": "",
            "gcc-mpx_no_narrow_bounds_only_write": "",
            "gcc-mpx_no_narrow_bounds": "",
            "gcc-mpx_only_write": "",
            "gcc-mpx": "",
            "gcc-asan": "",
            "gcc-asan_only_write": "",
        },
        "mpx_feature": {
            "icc-native": "Native (ICC)",
            "icc-mpx_no_narrow_bounds_only_write": "No narrow bounds only write (ICC)",
            "icc-mpx_no_narrow_bounds": "No narrow bounds (ICC)",
            "icc-mpx_only_write": "Only write (ICC)",
            "icc-mpx": "Full (ICC)",

            "gcc-native": "Native (GCC)",
            "gcc-mpx_no_narrow_bounds_only_write": "No narrow bounds only write (GCC)",
            "gcc-mpx_no_narrow_bounds": "No narrow bounds (GCC)",
            "gcc-mpx_only_write": "Only write (GCC)",
            "gcc-mpx": "Full (GCC)",
        }
    }

    input_names = {
        "long": {
            0: "Small",
            1: "Medium",
            2: "Large",
            3: "Extra Large",
            4: "XXL"
        },
        "short": {
            0: "S",
            1: "M",
            2: "L",
            3: "XL",
            4: "XXL"
        }
    }

    default_build_order = (
        "clang-asan",
        "icc-mpx",
        # "icc-ptr",
        "gcc-mpx",
        # "gcc-mpx_disabled",
        "safecode-enabled",
        "softbound-enabled",
    )
    other_build_orders = {
        "mpxcount": (
            "icc-mpx",
            "icc-mpx_only_write",
            "gcc-mpx",
            "gcc-mpx_only_write",
        ),
        "multi": (
            "gcc-native",
            "clang-asan",
            "icc-mpx",
            "gcc-mpx",
        ),
        "native_mem_access": (
            "clang-native",
            "icc-native",
            "gcc-native",
            "safecode-native",
            "softbound-native",
        ),
        "ipc": (
            "gcc-native",
            "clang-asan",
            "icc-mpx",
            "gcc-mpx",
            "safecode-enabled",
            "softbound-enabled",
        ),
        "cache": (
            "gcc-native",
            "clang-asan",
            "icc-mpx",
            "gcc-mpx",
            "safecode-enabled",
            "softbound-enabled",
        ),
        "mpx_feature_perf": (
            "icc-mpx",
            "icc-mpx_no_narrow_bounds",
            "icc-mpx_only_write",
            "gcc-mpx",
            "gcc-mpx_no_narrow_bounds",
            "gcc-mpx_only_write",
        ),
        "mpx_feature_mem": (
            "icc-mpx",
            "icc-mpx_no_narrow_bounds",
            "icc-mpx_only_write",
            "gcc-mpx",
            "gcc-mpx_no_narrow_bounds",
            "gcc-mpx_only_write",
        ),
        "tput": (
            "gcc-native",
            "gcc-asan",
            "icc-mpx_no_narrow_bounds",
            "gcc-mpx_no_narrow_bounds",
        ),
    }
