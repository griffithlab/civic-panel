#!/usr/bin/env python3

"""
This is a test python file for the CIViC smMIPs paper

Usage: python3 TEST.py <name>

Arguments:
    <name> = List your name
"""

import sys
import numpy as np

person = sys.argv[1]

def print_name(person): 
    print('Your name is ' + person)
    
interact(print_name(person))