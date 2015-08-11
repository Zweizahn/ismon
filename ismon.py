#!/usr/bin/env python3

# Reading ismon data for physical disks both load and latentcy and creating output:
#    <timestamp> <disk> <KB-R> <KB-R> <Latency R> <Latency W>

# Reading input file
#
#


__author__ = 'Erik'
__version__ = 'v0.1'

import sys
from collections import defaultdict
from collections import OrderedDict


#########################################################################
""" functions section
"""


def get_Timestamp(words):
    if len(words) > 5:
        timestamp = words[2] + '-' + words[3] + '-' + words[4]
    else:
        print("Incorrect timestamp")
        timestamp = ''
    return timestamp


#########################################################################
""" Classes section
"""


class Data(object):
    """ Contains the main data structure
    """

    def __init__(self):
        self.time = OrderedDict(defaultdict(list))

    def keysDisk(self):
        pass

    def keyVdev(self):
        pass

    def lineAbs(self):
        pass

    def lineLatency(self):
        pass

    def read(self, filename):
        print("reading file...")
        try:
            handle = open(filename, 'r')
            print("Opening {} for reading".format(filename))
        except:
            print("File {} does not exists".format(filename))
            return

        linenumber = 0
        timestamp = ''
        line = ''
        while line in handle:
            linenumber += 1
            line = line.strip()
            if line == '':
                # ignore empty lines
                continue
            words = line.split()
            if words[0][-1] == ':':
                # Check if line contains timestamp
                timestamp = get_Timestamp(words)
            elif isinstance(word[0], str):
                # Ignore further lines starting with a string
                continue
            else:
                length = len(words)
                if length == 8:
                    # vdev: virtual latency
                    pass
                elif length == 9:
                    # ACLS: absolut
                    pass
                elif length == 10:
                    if isinstance(word[1], str):
                        # vdev: absolut
                        pass
                    else:
                        # physical latency
                        pass
                else:
                    # Should not happen
                    print("Somethings wrong line {}".format(linenumber))


########################################################################
""" Main
"""
print(__name__)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Wrong invocation of program:")
        print("  ismon-read-physical ipstor_ismon.Plog ipstor_ismon.PYlog")
        exit()

    plog = data()
    pylog = data()
    plog.read(sys.argv[1])
    pylog.read(sys.argv[2])

   
