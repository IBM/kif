#!/bin/bash
# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

PYTHON=${PYTHON:-python}
WIKIDATA=${WIKIDATA:-https://query.wikidata.org/sparql}
MAX_REQUESTS=${MAX_REQUESTS:-1}
MAX_RETRIES=${MAX_RETRIES:-5}
PAGE_SIZE=${PAGE_SIZE:-5000}
PARALLEL_RUNS=${PARALLEL_RUNS:-2}
TIMEOUT=${TIMEOUT:-90}

run() {
  set -x
  $PYTHON -m kif_lib.vocabulary.wd.downloader\
          --append\
          --items\
          --max-requests $MAX_REQUESTS\
          --max-retries $MAX_RETRIES\
          --page-size $PAGE_SIZE\
          --timeout $TIMEOUT\
          --type "$1"\
          --wikidata $WIKIDATA&
}

declare -a types=(
  'Q113145171'               # type of chemical entity
  'Q144'                     # dog
  'Q16521'                   # taxon
  'Q223662'                  # SI base unit
  'Q28640'                   # profession
  'Q34770'                   # language
  'Q4022'                    # river
  'Q4830453'                 # business
  'Q5'                       # human
  'Q515'                     # city
  'Q55983715'                # organisms known by a particular common name
  'Q6256'                    # country
  'Q8502'                    # mountain
)

n=${#types[@]}
for (( i=0; i < $n; i++ )); do
  run ${types[$i]}
  if test $((($i + 1) % ${PARALLEL_RUNS})) -eq 0; then
    wait $(jobs -pr)
  fi
done
