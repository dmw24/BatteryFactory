#!/bin/bash
# usage: team/scripts/sc_validate.sh SC001 [sample]  — JSON parse, build+checks, quote verification sample
t=$1; n=${2:-40}
python3 -c "import json,sys;p=json.load(open('data/supply_chain/patches/$t.json'));print('$t rows',len(p['rows']),'sources',len(p['sources']))" || exit 1
python3 checks/sc_checks.py | grep -E "FAIL|summary"
python3 checks/verify_quotes.py --sc --task $t --sample $n | grep -E "MISSING|FETCH_FAIL|SUMMARY"
