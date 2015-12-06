""" Custom reporter to generate Github-flavoured markdown tables """

import sys
import argparse
import unitbench

parser = argparse.ArgumentParser()
parser.add_argument('--gfm', dest='gfm', action='store_true')
gfm = parser.parse_args().gfm

class Reporter(unitbench.Reporter):
    """ Custom reporter """

    def __init__(self, output_stream=sys.stdout):
        self.stream = output_stream

    def write_results(self, value, results):
        if gfm:
            self.stream.write("{0}|{1}|{2}|{3}\n".format(value, "user (ns)", "sys (ns)", "real (ns)"))
            self.stream.write(":--|--:|--:|--:\n")
            for r in results:
                if hasattr(r, "user_mean") and \
                   hasattr(r, "system_mean") and \
                   hasattr(r, "wall_mean"):
                    self.stream.write("{0}|{1:,.0f}|{2:,.0f}|{3:,.0f}\n".format(r.name, \
                        r.user_mean * 10**9, \
                        r.system_mean * 10**9, \
                        r.wall_mean * 10**9))
        else:
            self.stream.write("{0:<20}{1:>15}{2:>15}{3:>15}\n".format(value, "user (ns)", "sys (ns)", "real (ns)"))
            self.stream.write("=" * 65 + "\n")
            for r in results:
                if hasattr(r, "user_mean") and \
                   hasattr(r, "system_mean") and \
                   hasattr(r, "wall_mean"):
                    self.stream.write("{0:<20} {1:>14,.0f} {2:>14,.0f} {3:>14,.0f}\n".format(r.name, \
                        r.user_mean * 10**9, \
                        r.system_mean * 10**9, \
                        r.wall_mean * 10**9))
        self.stream.write("\n")
