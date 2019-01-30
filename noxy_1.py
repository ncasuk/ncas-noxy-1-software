import csv

import pandas as pd

from amfutils.instrument import AMFInstrument

class Noxy1 (AMFInstrument):
    """
    Class to convert the CVAO NOxy instrument's CSV output
    into well-formed NetCDF conforming to AMF conventions
    """

    progname = __file__

    amf_variables_file = "nox-noxy-concentration.xlsx - Variables - Specific.csv"

    def get_noxy_data(self, infiles):
        """
            Example good dataline:

43486.73331940,3258.928,263341000,4.863012,3212.747,0,1842471,,,21.15406,1715.183,0,-2.716240,0,,,,0,,0,,,,0.3925973,12.15292,,0,100.6249,2.687422,0,0,0,0,-29.14398,35.44047,2.936691,992.7882,1000.000,,,,0,0,0,0,0,34.95440,,,,,,0,,,,,,,,,,0.8799786,,62.94314,,-1.106045,,,,,,,,,,,,,,0,62.94314,,39470.70,,-1.106045,0,,0.2579111,6.189275,,6.189275

            :param infiles: list(-like) of data filenames
            :return: a Pandas DataFrame of the sonic data
        """
    
        noxy = pd.DataFrame()
        for infile in infiles:
            with open(infile, 'rt') as f:
                noxy = pd.concat([noxy,pd.read_csv(f)])

        return noxy
noxy = Noxy1('noxy_meta_data')
print(noxy.get_noxy_data(['NOxy_all_1hz_190121_174035','NOxy_all_1hz_190122_181916']))
