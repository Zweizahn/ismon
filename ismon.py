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


class Data(object):
    """ Contains the main data structure
    """

    def __init__(self):
        self.time = OrderedDict(defaultdict(list))
        self.sums = defaultdict(dict)

    def __str__(self):
        for timestamp in self.time:
            print('\nTimestamp: {}'.format(timestamp))
            timelist = self.time[timestamp]
            for key, value in timelist.items():
                output = ''
                for k, v in value.items():
                    output += str(v) + ' '
                #                print(key, value['read'], value['write'], value['lread'], value['lwrite'])
                print(key, output)
            output = ''
            for k, v in self.sums[timestamp].items():
                output += str(v) + ' '
            print('Sum: ' + output)
            # dummy = input("Press key")
        return ''

    def keyDisk(self, words):
        return words[0] + '-' + words[1] + '-' + words[2] + '-' + words[3]

    def get_Timestamp(self, words):
        if len(words) > 5:
            timestamp = words[2] + '-' + words[3] + '-' + words[4]
        else:
            timestamp = ''
        return timestamp

    def enter_Data(self, timestamp, key, read, write, index):
        """
        Enters data in the local data structure
        :param timestamp:
        :param key:
        :param read:
        :param write:
        :return:
        """
        # print(timestamp, key, read, write)
        index1 = index + 'read'
        index2 = index + 'write'
        index3 = index + 'readsum'
        index4 = index + 'writesum'
        if timestamp not in self.time:
            self.time[timestamp] = defaultdict(dict)
            self.time[timestamp][key] = dict()
            self.sums[timestamp][index3] = 0
            self.sums[timestamp][index4] = 0
        # elif key in self.time[timestamp]:
        #     # This should only happen when we have duplicate data e.g. sorted for read and sorted for write
        #     # or ismon put out data twice for 1 seconds. Will ignore that data
        #     return
        self.time[timestamp][key][index1] = read
        self.time[timestamp][key][index2] = write
        self.sums[timestamp][index3] = self.sums[timestamp].get(index3,0) + read
        self.sums[timestamp][index4] = self.sums[timestamp].get(index4,0) + write

    def latency(self, value):
        """
        :rtype : int
        """
        if 'us' in value:
            # micro second value returns 1 milli second
            return 1
        elif value == 'N/A':
            # N/A values return 0
            return 0
        elif 'ms' in value:
            # milli second value, cut last 2 chars
            #            print(value)
            return int(value[:len(value) - 2])
        else:
            # full second value
            return int(value[:len(value) - 1])

    def read(self, filename):
        print("reading file...", filename)
        try:
            handle = open(filename, 'r')
            print("Opening {} for reading".format(filename))
        except IOError:
            print("File {} does not exists".format(filename))
            return

        linenumber = 0
        timestamp = ''
        line = ''
        pending = False
        for line in handle:
            linenumber += 1
            line = line.strip()
            if line == '':
                # ignore empty lines
                continue
            words = line.split()
            if words[0].endswith(':'):
                # Check if line contains timestamp
                timestamp = self.get_Timestamp(words)
            elif 'Pnd' in words:
                # Pending commands switched on, assuming it won't be switched off again
                pending = True
            elif words[0].isnumeric():
                length = len(words)
                if length == 8:
                    # vdev: virtual latency
                    key = int(words[0])
                    read = self.latency(words[4])
                    write = self.latency(words[5])
                    index = 'l'
                #                    self.enter_Data(timestamp, key, read, write, 'lread', 'lwrite')
                elif length == 9:
                    if words[1] == '0':
                        # ACLS: absolut, no pending commands, assuming no vdev is called '0'
                        key = self.keyDisk(words)
                        read = int(words[4])
                        write = int(words[5])
                    else:
                        # vdev: absolut with pending commands
                        key = int(words[0])
                        read = int(words[3])
                        write = int(words[4])
                    index = 'a'
                #                    self.enter_Data(timestamp, key, read, write, 'read', 'write')
                elif length == 10:
                    if pending:
                        if words[1] == '0':
                            # ACLS: absolut with pending commands, assuming no vdev is called '0'
                            key = self.keyDisk(words)
                            read = int(words[5])
                            write = int(words[6])
                        else:
                            # vdev: absolut with pending commands
                            key = int(words[0])
                            read = int(words[4])
                            write = int(words[5])
                        index = 'a'
                    #                        self.enter_Data(timestamp, key, read, write, 'read', 'write')
                    else:
                        # physical latency
                        key = self.keyDisk(words)
                        read = self.latency(words[6])
                        write = self.latency(words[7])
                        index = 'l'
                    #                        self.enter_Data(timestamp, key, read, write, 'lread', 'lwrite')
                else:
                    # Should not happen
                    print("Somethings wrong line {}".format(linenumber))
                    continue
                self.enter_Data(timestamp, key, read, write, index)
        print('Number of lines read: {}'.format(linenumber))


########################################################################
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Wrong invocation of program:")
        print("  ismon-read-physical ipstor_ismon.Plog ipstor_ismon.PYlog")
        exit()

    log = Data()
    #    ylog = Data()
    log.read(sys.argv[1])
    log.read(sys.argv[2])
    print(log)
# print(ylog)
