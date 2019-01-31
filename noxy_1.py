import csv
import os

import pandas as pd
from datetime import datetime

from amfutils.instrument import AMFInstrument
from netCDF4 import Dataset

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
            :return: a Pandas DataFrame of the noxy data
        """
    
        noxy = pd.DataFrame()
        for infile in infiles:
            with open(infile, 'rt') as f:
                noxy = pd.concat([noxy,pd.read_csv(f)])

        #Timeseries.
        noxy['TheTime'] = pd.to_datetime('1899-12-30') + pd.to_timedelta(noxy.TheTime,'D') #Excel-ish time (decimal days since 1900-01-01, 1-indexed)
        #may not be correct for Jan-March01 1900 as Excel incorrectly thinks 1900
        #was a leap year
        noxy.set_index('TheTime', inplace=True)

        #set start and end times
        self.time_coverage_start = noxy.index[0].strftime(self.timeformat)
        self.time_coverage_end = noxy.index[-1].strftime(self.timeformat)

        self.rawdata = noxy
        return noxy

    def netcdf(self, output_dir):
        """
        Takes a dataframe (self.rawdata) with NOxy data and outputs a 
        well-formed NetCDF using appropriate conventions.

        :param output_dir: string contaiing path to output directory

        """

        self.setup_dataset('nox-noxy-concentration',1)

        #lat/long
        self.land_coordinates()
    
        #add all remaining attribs
        self.dataset.setncatts(self.raw_metadata)
    
        self.dataset.close()


if __name__ == '__main__':
    args = Noxy1.arguments().parse_args()
    nx = Noxy1(args.metadata) 

    try:
        os.makedirs(args.outdir,mode=0o755)
    except OSError:
         #Dir already exists, probably
         pass
    else:
        print ("Successfully create directory %s" % args.outdir)
    nx.get_noxy_data(args.infiles)
    nx.netcdf(output_dir=args.outdir)

