#!/usr/bin/env python3

# Reading ismon data for physical disks both load and latentcy and creating output:
#    <timestamp> <disk> <KB-R> <KB-R> <Latency R> <Latency W>

# Reading input file
#
#


__author__ = 'Erik'

import sys


def read_file(handle) -> object:
    """

    :rtype : object
    """
    while True:
        line = handle.readline()
    line = line.strip()
    words = line.split()


if len(sys.argv) < 3:
    print("Wrong invocation of program:")
    print("  ismon-read-physical ipstor_ismon.Plog ipstor_ismon.PYlog")
    exit()

plog = sys.argv[1]
pylog = sys.argv[2]

try:
    phandle = open(plog, 'r')
except:
    print("File {} does not exists").format(plog)
    exit()

try:
    yhandle = open(pylog, 'r')
except:
    print("File {} does not exists").format(pylog)
    exit()

read_file(phandle)

