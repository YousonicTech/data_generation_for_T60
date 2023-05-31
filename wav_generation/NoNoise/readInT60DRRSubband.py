import csv
import pandas as pd

import numpy as np


def readInT60DRRSubband(csv_file):

    data = pd.read_csv(csv_file)
    print(data)
    resultsScan = data.values
    results = {}
    results["testID"] = resultsScan[:,0]
    results["version"] = resultsScan[:,1]
    results["fs"]= resultsScan[:,2]
    results["room"] = resultsScan[:,3]

    results["sessionID"]= resultsScan[:,5]

    results["micPos"] = resultsScan[:,6]

    results["srcPos"] = resultsScan[:,7]

    # 为啥要用去除空格
    
    results["config"]= np.array([str(resultsScan[:,7][i]).replace(" ","") for i in range(len(resultsScan[:,7]))])
    
    results["recType"] = resultsScan[:,9]

    results["rirName"] = resultsScan[:,10]

    results["freqBand"]= resultsScan[:,11]

    results["centreFreq"] = resultsScan[:,12]

    results["channel"] = resultsScan[:,13]
    results["channel"] = results["channel"].astype(np.float32)

    results["DRR"] = resultsScan[:,14]

    results["DRRMean"]= resultsScan[:,15]

    results["T60AHM"] = resultsScan[:,16]

    results["T60AHMMean"] = resultsScan[:,19]

    results["DRRFullband"] = resultsScan[:,23]

    results["DRRFullbandMean"] = resultsScan[:,24]

    results["T60AHMFullband"]= resultsScan[:,25]

    results["T60AHMFullbandMean"] = resultsScan[:,28]

    return results

