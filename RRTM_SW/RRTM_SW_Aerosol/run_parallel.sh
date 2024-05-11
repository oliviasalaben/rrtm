#!/bin/bash

# Path to Python script
SCRIPT="ipython execute_rrtm_for_sza_and_rs_coord.ipynb"

# Loop through the combinations and execute the script in parallel
for season in 0 1 2 3; do
    for ilat in $(seq 0 $((${#lat_sza[@]} - 1))); do
            for ilon in $(seq 0 $((${#lon_sza[@]} - 1))); do
                        $SCRIPT $season $ilat $ilon &
                                done
                                    done
                                    done

                                    wait
