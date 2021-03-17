#!/usr/bin/env python3

import re
import tempfile
import subprocess
import os
import glob


def get_data_from_file(f):
    line = f.readline()
    if line == '':
        return None
    try:
        timestamp, parkingg, freespace = line.split(';')
        timestamp = int(timestamp)
        parkingg  = parkingg.strip()
        freespace = int(freespace)
    except:
        # invalid line, let's read the next one
        # TODO: warning?
        return get_data_from_file(f)

    return ( int(timestamp), parkingg, int(freespace), line )


raw_data_dir = 'data'
preprocessed_data_dir = 'data/preprocessed'

if not os.path.exists(preprocessed_data_dir):
    os.makedirs(preprocessed_data_dir)

parkingdat_files = dict.fromkeys(glob.glob(f'{raw_data_dir}/host-*2016*-parkingzh.dat'))

all_lines = 0
saved_lines = 0
different_value_events = 0
duplicated_line_events = 0
wrong_order_timestamp_event = 0
measurements_too_close_events = 0


parking_garages = {}
current_lines = {}
previous_data = {}

try:
    for parkingdat in parkingdat_files.keys():
        print(f'Start reading from {parkingdat}')
        parkingdat_files[parkingdat] = open(parkingdat,'r')
        current_lines[parkingdat] = get_data_from_file(parkingdat_files[parkingdat])
        if current_lines[parkingdat] == None:
            current_lines.pop(parkingdat)
            print(' ... it doesn\'t have any valid lines.')
    print()

    while bool(current_lines):
        all_lines += 1
        min_timestamp, min_parkingdat = min([ (current_lines[k], k) for k in current_lines.keys() ])

        timestamp, parkingg, freespace, line = current_lines[min_parkingdat]

        if parkingg not in parking_garages.keys():
            parkingg_fpath = f'{preprocessed_data_dir}/{parkingg}.dat'
            print(f'Found new parking garage: {parkingg} ({parkingg_fpath})')
            if os.path.isfile(parkingg_fpath):
                os.remove(parkingg_fpath)
            parking_garages[parkingg] = open(parkingg_fpath, 'w')
            p_timestamp = 0
        else:
            p_timestamp, p_freespace, = previous_data[parkingg]


        if timestamp == p_timestamp:
            if freespace == p_freespace:
                # same data from another host
                duplicated_line_events += 1
            else:
                # different values from different hosts
                different_value_events += 1
        elif timestamp - p_timestamp < 30:
            # we are collecting data in every minutes, but because of the different hosts we can have data points
            # too close to each other (typically only 1-2 seconds difference)
            measurements_too_close_events += 1
        elif timestamp < p_timestamp:
            # this shouldn't happen
            wrong_order_timestamp_event += 1
        else:
            saved_lines += 1
            print(line.rstrip(), file = parking_garages[parkingg])
            previous_data[parkingg] = (timestamp, freespace)


        current_lines[min_parkingdat] = get_data_from_file(parkingdat_files[min_parkingdat])
        if current_lines[min_parkingdat] == None:
            current_lines.pop(min_parkingdat)

finally:
    for pfile in parking_garages.values():
        pfile.close()

    for parkingdat in parkingdat_files.values():
        if parkingdat != None:
            parkingdat.close()

print()
print(f'{all_lines=}')
print(f'{saved_lines=}')
print(f'{wrong_order_timestamp_event=} <- This must be zero!')
print(f'{different_value_events=}      <- This should be zero too but I know it\'s usually not.')
print(f'{duplicated_line_events=}')
print(f'{measurements_too_close_events=}')

