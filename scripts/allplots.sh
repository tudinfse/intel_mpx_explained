#!/usr/bin/env bash

RESULTSDIR=`pwd`/../raw_results
VERBOSE=-v

cd ..

set -x #echo on

# phoenix
./fex.py $VERBOSE plot -n phoenix_perf -t perf               -f $RESULTSDIR/phoenix/perf.csv
./fex.py $VERBOSE plot -n phoenix_perf -t instr              -f $RESULTSDIR/phoenix/perf.csv
./fex.py          plot -n phoenix_perf -t misc_stat          -f $RESULTSDIR/phoenix/perf.csv
./fex.py          plot -n phoenix_perf -t cache              -f $RESULTSDIR/phoenix/cache.csv
./fex.py $VERBOSE plot -n phoenix_perf -t mem                -f $RESULTSDIR/phoenix/mem.csv
./fex.py $VERBOSE plot -n phoenix_perf -t multi              -f $RESULTSDIR/phoenix/multithreading.csv
./fex.py          plot -n phoenix_perf -t mpxcount           -f $RESULTSDIR/phoenix/mpx_instructions.csv
./fex.py $VERBOSE plot -n phoenix_perf -t native_mem_access  -f $RESULTSDIR/phoenix/cache.csv
./fex.py $VERBOSE plot -n phoenix_perf -t ku_instr           -f $RESULTSDIR/phoenix/ku_instructions.csv
./fex.py $VERBOSE plot -n phoenix_perf -t mpx_feature_perf   -f $RESULTSDIR/phoenix/perf.csv
./fex.py $VERBOSE plot -n phoenix_perf -t mpx_feature_mem    -f $RESULTSDIR/phoenix/mem.csv
./fex.py $VERBOSE plot -n phoenix_perf -t ipc                -f $RESULTSDIR/phoenix/perf.csv

# phoenix varinput
./fex.py $VERBOSE plot -n phoenix_var_input -t perf -f $RESULTSDIR/phoenix/var_input_perf.csv
./fex.py $VERBOSE plot -n phoenix_var_input -t mem  -f $RESULTSDIR/phoenix/var_input_mem.csv

# parsec
./fex.py $VERBOSE plot -n parsec_perf -t perf                -f $RESULTSDIR/parsec/perf.csv
./fex.py $VERBOSE plot -n parsec_perf -t instr               -f $RESULTSDIR/parsec/perf.csv
./fex.py          plot -n parsec_perf -t misc_stat           -f $RESULTSDIR/parsec/perf.csv
./fex.py          plot -n parsec_perf -t cache               -f $RESULTSDIR/parsec/cache.csv
./fex.py $VERBOSE plot -n parsec_perf -t mem                 -f $RESULTSDIR/parsec/mem.csv
./fex.py $VERBOSE plot -n parsec_perf -t multi               -f $RESULTSDIR/parsec/multithreading.csv
./fex.py          plot -n parsec_perf -t mpxcount            -f $RESULTSDIR/parsec/mpx_instructions.csv
./fex.py $VERBOSE plot -n parsec_perf -t native_mem_access   -f $RESULTSDIR/parsec/cache.csv
./fex.py $VERBOSE plot -n parsec_perf -t ku_instr            -f $RESULTSDIR/parsec/ku_instructions.csv
./fex.py $VERBOSE plot -n parsec_perf -t mpx_feature_perf    -f $RESULTSDIR/parsec/perf.csv
./fex.py $VERBOSE plot -n parsec_perf -t mpx_feature_mem     -f $RESULTSDIR/parsec/mem.csv
./fex.py $VERBOSE plot -n parsec_perf -t ipc                 -f $RESULTSDIR/parsec/perf.csv

# parsec varinput
./fex.py $VERBOSE plot -n parsec_var_input -t perf -f $RESULTSDIR/parsec/var_input_perf.csv
./fex.py $VERBOSE plot -n parsec_var_input -t mem  -f $RESULTSDIR/parsec/var_input_mem.csv

# spec
./fex.py $VERBOSE plot -n spec_perf   -t perf               -f $RESULTSDIR/spec/perf.csv
./fex.py $VERBOSE plot -n spec_perf   -t instr              -f $RESULTSDIR/spec/perf.csv
./fex.py          plot -n spec_perf   -t misc_stat          -f $RESULTSDIR/spec/perf.csv
./fex.py          plot -n spec_perf   -t cache              -f $RESULTSDIR/spec/cache.csv
./fex.py $VERBOSE plot -n spec_perf   -t mem                -f $RESULTSDIR/spec/mem.csv
./fex.py          plot -n spec_perf   -t mpxcount           -f $RESULTSDIR/spec/mpx_instructions.csv
./fex.py $VERBOSE plot -n spec_perf   -t native_mem_access  -f $RESULTSDIR/spec/cache.csv
./fex.py $VERBOSE plot -n spec_perf   -t mpx_feature_perf   -f $RESULTSDIR/spec/perf.csv
./fex.py $VERBOSE plot -n spec_perf   -t mpx_feature_mem    -f $RESULTSDIR/spec/mem.csv
./fex.py $VERBOSE plot -n spec_perf   -t ipc                -f $RESULTSDIR/spec/perf.csv

# spec varinput
./fex.py $VERBOSE plot -n spec_var_input -t perf -f $RESULTSDIR/spec/var_input_perf.csv
./fex.py $VERBOSE plot -n spec_var_input -t mem  -f $RESULTSDIR/spec/var_input_mem.csv

# case studies
./fex.py $VERBOSE plot -n apache_perf    -t tput -f $RESULTSDIR/casestudies/apache/raw.csv
./fex.py $VERBOSE plot -n memcached_perf -t tput -f $RESULTSDIR/casestudies/memcached/raw.csv
./fex.py $VERBOSE plot -n nginx_perf     -t tput -f $RESULTSDIR/casestudies/nginx/raw.csv

# microbenchmarks
./fex.py $VERBOSE plot -n micro_perf -t perf -f $RESULTSDIR/micro/raw.csv

# merged
./fex.py $VERBOSE plot -n mergedplots -t tput     -f $RESULTSDIR/casestudies/raw.csv
./fex.py $VERBOSE plot -n mergedplots -t perf     -f $RESULTSDIR/merged/perf.csv
./fex.py $VERBOSE plot -n mergedplots -t mem      -f $RESULTSDIR/merged/mem.csv
./fex.py $VERBOSE plot -n mergedplots -t mpxcount -f $RESULTSDIR/merged/mpxcount.csv
./fex.py $VERBOSE plot -n mergedplots -t multi    -f $RESULTSDIR/merged/multithreading.csv
./fex.py $VERBOSE plot -n mergedplots -t cache    -f $RESULTSDIR/merged/cache.csv 
./fex.py $VERBOSE plot -n mergedplots -t instr    -f $RESULTSDIR/merged/instr.csv
./fex.py $VERBOSE plot -n mergedplots -t ipc      -f $RESULTSDIR/merged/ipc.csv
./fex.py $VERBOSE plot -n mergedplots -t mpx_feature_perf -f $RESULTSDIR/merged/mpx_feature_perf.csv 
./fex.py $VERBOSE plot -n mergedplots -t mpx_feature_mem  -f $RESULTSDIR/merged/mpx_feature_mem.csv
