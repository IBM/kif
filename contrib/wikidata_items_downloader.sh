#!/bin/bash
# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

PYTHON=${PYTHON:-python}
WIKIDATA=${WIKIDATA:-https://query.wikidata.org/sparql}
PAGE_SIZE=${PAGE_SIZE:-5000}

run() {
  set -x
  $PYTHON -m kif_lib.vocabulary.wd -aQ -w $WIKIDATA -s $PAGE_SIZE -t $1&
}

run 'Q113145171'               # type of chemical entity
run 'Q16521'                   # taxon
run 'Q223662'                  # SI base unit
run 'Q28640'                   # profession
run 'Q34770'                   # language
run 'Q4022'                    # river
run 'Q4830453'                 # business
run 'Q5'                       # human
run 'Q515'                     # city
run 'Q55983715'                # organisms known by a particular common name
run 'Q6256'                    # country
run 'Q8502'                    # mountain
wait $(jobs -rp)
