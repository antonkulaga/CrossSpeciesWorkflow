from typing import *
from dataclasses import dataclass, field
from pathlib import Path
import os, sys

@dataclass
class NetCglycData:
    """Class that parses NetCglyc prediction output data.

    Parameters
    ----------

    Attributes
    ----------
    predictedSites : Dictionary
        predictedSites [ protein name ][ start resid ] : array of entry dict
        entry dict has the following keys:

        # Common to all PTS predictors
            seq : string (stretch of the predicted sequence)
            start : starting residue id
            end : ending residue id
            isSignif : bool (is the method's specific scoring indicating a
                            potentially significant result)
            score : float (interpretation differs between methods)
            type : string (C-glyc)
            predictor : string (for cases where multiple predictors are available)

    Public Methods
    --------------
    parse( outputFile : path ) -> NetCglyc
        Parses the NetCglyc prediction output file and add the data inside the
        above attribute data structure.

    """

    predictedSites : dict = field(default_factory=dict)

    @staticmethod
    def parse(outputFile: Path) :

        data = NetCglycData()

        try:
            f = open(outputFile, 'r')

            lines = f.readlines()
            for line in lines:
                l = line.split()
                if l[0][0] != "#" :
                    protname = l[0]
                    if protname not in data.predictedSites:
                        data.predictedSites[ protname ] = {}

                    # not provided, but the prediction only reffers to
                    # tryptophan (W), therefore for consistency we added
                    # to preserve the fields structure
                    aa = "W"
                    start = int( l[3] )
                    end = int( l[4] )
                    score = round( float( l[5] ), 3)
                    isSignif = (l[7] == "W")

                    resid = start

                    if resid not in data.predictedSites[protname]:
                        data.predictedSites[protname][resid] = []

                    data.predictedSites[protname][resid].append({
                        "seq": aa,
                        "start": start,
                        "end": end,
                        "isSignif" : isSignif,
                        "score" : score,
                        "type": "C-Glyc",
                        "predictor": "netcglyc"
                    })


        except OSError as e:
            print("File error:", sys.exc_info()[0])
            raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return data


