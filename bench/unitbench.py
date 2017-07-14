'''
Copyright (c) 2011, Joseph LaFata
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the unitbench nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
from __future__ import division

import inspect
import math
import os
import re
import string
import sys
import time

if sys.version_info < (3, 0):
    maxint = sys.maxint
    fname = "func_name"
else:
    xrange = range
    maxint = sys.maxsize
    fname = "__name__"

if sys.platform == "win32":
    get_time = time.clock
else:
    get_time = time.time


class TimeSet(object):
    __slots__ = ["wall", "user", "system"]
    
    def __init__(self, wall, user, system):
        self.wall = wall
        self.user = user
        self.system = system
        

class BenchResult(object):
    """
    This contains the results of running a benchmark.
    
    It contains the mean, variance, standard deviation, minimum,
    and maximum.  Each of these attributes are available for
    user, wall, and system time.
    
    Times:
     * wall
     * user
     * system
     
    Statistics:
     * min
     * max
     * mean
     * variance
     * std_dev (standard deviation)
     
    Combine one of the times and one of the statistics to get
    the appropriate attribute.
    
    Examples:
     * wall_mean - Mean wall clock time
     * user_std_dev - Standard deviation of user time
     * system_variance - Variance of system (kernel) time
     * wall_min - Minimum wall clock time
     * and so on...
    """

    def __init__(self, name, value, times):
        self.name = name
        self.value = str(value)
        
        if len(times) == 0:
            return
        
        time_types = ["wall", "user", "system"]
        for type in time_types:
            minimum = maxint
            maximum = -maxint
            count = 0
            sum = 0
            sum_2 = 0
            
            mean = 0.0
            variance = 0.0
            std_dev = 0.0
            
            for t in times:
                currentTime = getattr(t, type)
                
                count += 1
                sum += currentTime
                sum_2 += currentTime ** 2
                minimum = min(currentTime, minimum)
                maximum = max(currentTime, maximum)
            
            if len(times) > 0:
                mean = sum / count
                variance = (sum_2 / count) - (mean ** 2)
                if variance < 0.0:
                    variance = 0.0
                std_dev = math.sqrt(variance)
            
            setattr(self, type+"_min", minimum)
            setattr(self, type+"_max", maximum)
            setattr(self, type+"_mean", mean)
            setattr(self, type+"_variance", variance)
            setattr(self, type+"_stddev", std_dev)
                
        
class Benchmark(object):
    """
    """
    
    def setup(self):
        "Hook method called once before every run of each benchmark."
        pass
    
    def teardown(self):
        "Hook method called once after every run of each benchmark."
        pass
        
    def input(self):
        """Hook method for providing the input to the benchmark.  None
        should not be passed into a benchmark function.  It is used
        as a marker that no arguments are present.
        
        A list containing only 0 is used as a default.
        """
        return [0]

    def repeats(self):
        "Hook method for the number of times to repeat the benchmark (default 7)"
        return 7
    
    def warmup(self):
        """Hook method for the number of warmup runs to do (default 1)
        
        The warmup will run for each benchmark function with each value.
        """
        return 1
    
    def run(self, reporter=None):
        """This should generally not be overloaded.  Runs the benchmark functions
        that are found in the child class.
        """
        if not reporter: reporter = ConsoleReporter()
        benchmarks = sorted(self._find_benchmarks())
        reporter.write_titles(map(self._function_name_to_title, benchmarks))
        
        for value in self.input():
            results = []
            for b in benchmarks:
                
                method = getattr(self, b)
                arg_count = len(inspect.getargspec(method)[0])
                
                if arg_count == 2:
                    results.append(self._run_benchmark(method, value))
                elif arg_count == 1:
                    results.append(self._run_benchmark(method))
                    
            reporter.write_results(str(value), results)
            
    def _run_benchmark(self, method, value=None):
        # warmup the function
        for i in xrange(self.warmup()):
            self.setup()
            try:
                if value != None:
                    method(value)
                else:
                    method()
            except:
                self.teardown()
                raise
        
        # run the benchmark
        times = []
        for i in xrange(self.repeats()):
            self.setup()
            
            try:                    
                start_user_system = os.times()
                start = get_time()
                
                if value != None:
                    method(value)
                else:
                    method()
                    
                end = get_time()
                end_user_system = os.times()
                
                t = TimeSet(end-start,
                            end_user_system[0]-start_user_system[0],
                            end_user_system[1]-start_user_system[1])
                times.append(t)
            except:
                self.teardown()
                raise
            
            self.teardown()
        return BenchResult(self._function_name_to_title(getattr(method, fname)), value, times)
    
    def _find_benchmarks(self):
        """Return a suite of all tests cases contained in testCaseClass"""
        def is_bench_method(attrname, prefix="bench"):
            return attrname.startswith(prefix) and hasattr(getattr(self.__class__, attrname), '__call__')
        return list(filter(is_bench_method, dir(self.__class__)))
    
    def _function_name_to_title(self, name):
        output = name
        if output.startswith("bench"):
            output = output[5:]
        if output.find("_") != -1:
            return string.capwords(output.replace("_", " ").strip())
        else:
            s1 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', output)
            return string.capwords(re.sub('([a-z0-9])([A-Z])', r'\1 \2', s1).strip())
    
class Reporter(object):
    """
    This is the base class for benchmark result reporting.  If
    you'd like to write a custom importer this is the class to extend.
    """
    
    def write_titles(self, titles):
        """
        Override this method if you'd like to write out the titles
        at the beginning of your reporter.  The CsvReporter uses
        this function to output the titles at the top of each column.
        Alternatively, the ConsoleReporter doesn't override this
        function because it doesn't need to output the titles of
        each benchmark.
        """
        pass
    
    def write_results(self, value, results):
        """
        Override this method to output the results of the benchmark
        run.  Value is the value passed into each benchmark.  Results
        is a list of BenchResult objects.  See the BenchResult documentation
        for the information it contains.
        """
        pass
    
class ConsoleReporter(Reporter):

    def __init__(self, output_stream=sys.stdout):
        self.stream = output_stream
        
    def write_results(self, value, results):
        self.stream.write("Value: {0:<33}{1:>10}{2:>10}{3:>10}\n".format(value, "user", "sys", "real"))
        self.stream.write("=" * 70 + "\n")
        for r in results:
            if (hasattr(r, "user_mean") and 
                hasattr(r, "system_mean") and hasattr(r, "wall_mean")):
                self.stream.write("{0:<40} {1:>9.4} {2:>9.4} {3:>9.4}\n".format(r.name, 
                    r.user_mean, r.system_mean, r.wall_mean))
        self.stream.write("\n")
        
class CsvReporter(Reporter):
    
    def __init__(self, output_stream=sys.stdout, time_type="wall"):
        self.stream = output_stream
        self.time_type = time_type
        
    def write_titles(self, titles):
        self.stream.write("Values," + ",".join(titles))
        self.stream.write("\n")
    
    def write_results(self, value, results):
        output = []
        for r in results:
            if hasattr(r, self.time_type+"_mean"):
                output.append(str(getattr(r, self.time_type+"_mean")))
        if len(output) > 0:
            self.stream.write(value + "," + ",".join(output))
            self.stream.write("\n")