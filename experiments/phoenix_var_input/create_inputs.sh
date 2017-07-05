#!/usr/bin/env bash

cd /data/inputs/phoenix/linear_regression/input/
touch key_200MB.txt; for i in 1 2; do cat key_file_100MB.txt >> key_200MB.txt; done;
touch key_400MB.txt; for i in 1 2 3 4; do cat key_file_100MB.txt >> key_400MB.txt; done;
touch key_800MB.txt; for i in 1 2 3 4 5 6 7 8; do cat key_file_100MB.txt >> key_800MB.txt; done;
cd -

cd /data/inputs/phoenix/string_match/input/
touch key_200MB.txt; for i in 1 2; do cat key_file_100MB.txt >> key_200MB.txt; done;
touch key_400MB.txt; for i in 1 2 3 4; do cat key_file_100MB.txt >> key_400MB.txt; done;
touch key_800MB.txt; for i in 1 2 3 4 5 6 7 8; do cat key_file_100MB.txt >> key_800MB.txt; done;
cd -

cd /data/inputs/phoenix/word_count/input/
touch key_200MB.txt; for i in 1 2; do cat word_100MB.txt >> key_200MB.txt; done;
touch key_400MB.txt; for i in 1 2 3 4; do cat word_100MB.txt >> key_400MB.txt; done;
cd -
