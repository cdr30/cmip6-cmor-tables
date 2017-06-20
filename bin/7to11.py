"""
SYNOPSIS

    7to11.py

DESCRIPTION

    Convert a set of JSON MIP table files from version 1.00.07 of the MIP 
    tables to version 1.00.11. The only change made is to move the frequency
    from the header and place it in each variable's entry.

REQUIREMENTS

    None
"""
from collections import OrderedDict
import json
import os

files_to_fix =[
    'CMIP6_3hr.json', 'CMIP6_6hrLev.json', 'CMIP6_6hrPlev.json',
    'CMIP6_Amon.json', 'CMIP6_6hrPlevPt.json', 'CMIP6_AERday.json',
    'CMIP6_LImon.json', 'PRIMAVERA_PrimSIday.json', 'CMIP6_AERhr.json',
    'CMIP6_AERmon.json', 'CMIP6_AERmonZ.json', 'CMIP6_Lmon.json',
    'CMIP6_Oclim.json', 'CMIP6_Oday.json', 'CMIP6_Odec.json', 'CMIP6_Ofx.json',
    'CMIP6_Omon.json', 'CMIP6_Oyr.json', 'CMIP6_SIday.json',
    'CMIP6_SImon.json', 'CMIP6_CF3hr.json', 'CMIP6_CFday.json',
    'CMIP6_CFmon.json', 'CMIP6_CFsubhr.json', 'CMIP6_CFsubhrOff.json',
    'CMIP6_E1hr.json', 'CMIP6_E1hrClimMon.json', 'CMIP6_E3hr.json',
    'CMIP6_E3hrPt.json', 'CMIP6_E6hrZ.json', 'CMIP6_day.json',
    'CMIP6_Eday.json', 'CMIP6_EdayZ.json', 'CMIP6_Efx.json', 'CMIP6_Emon.json',
    'CMIP6_EmonZ.json', 'CMIP6_Esubhr.json', 'CMIP6_Eyr.json',
    'CMIP6_IfxAnt.json', 'CMIP6_IfxGre.json', 'CMIP6_ImonAnt.json',
    'CMIP6_ImonGre.json', 'CMIP6_IyrAnt.json', 'CMIP6_IyrGre.json',
    'CMIP6_fx.json', 'PRIMAVERA_Prim1hr.json', 'PRIMAVERA_Prim3hr.json',
    'PRIMAVERA_Prim3hrPt.json', 'PRIMAVERA_Prim6hr.json',
    'PRIMAVERA_Prim6hrPt.json', 'PRIMAVERA_PrimO6hr.json',
    'PRIMAVERA_PrimOday.json', 'PRIMAVERA_PrimOmon.json',
    'PRIMAVERA_Primmon.json', 'PRIMAVERA_PrimmonZ.json',
    'PRIMAVERA_Primday.json', 'PRIMAVERA_PrimdayPt.json'
]


def main():
    """
    Run the software
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    table_dir = os.path.abspath(os.path.join(current_dir, '..', 'Tables'))


    for filename in files_to_fix:
        # load the file
        with open(os.path.join(table_dir, filename), 'r') as src_file:
            src_data = json.load(src_file, object_pairs_hook=OrderedDict)

        # remove the frequency from the header but keep a copy
        frequency = src_data['Header']['frequency']
        del src_data['Header']['frequency']

        # process each variable in the file
        for data_var in src_data['variable_entry']:
            # copy the items into a list
            var_list = [
                (key, value)
                for key, value in src_data['variable_entry'][data_var].items()
            ]

            # add the frequency to each variable
            var_list.insert(0, ('frequency', frequency))

            # put back in to the main data structure
            src_data['variable_entry'][data_var] = OrderedDict(var_list)

        # save the output
        with open(os.path.join(table_dir, filename), 'w') as dest_file:
            json.dump(src_data, dest_file, indent=4)


if __name__ == '__main__':
    main()
