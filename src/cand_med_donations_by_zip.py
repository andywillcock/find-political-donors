import os
import numpy as np

filepath = os.getcwd()+"/itcont.txt"
def medianvals_by_zip(filepath):


    with open(filepath,'r') as f:
        records_dt = np.dtype([('CMTE_ID','|S10'),('ZIP_CODE', '|S10'),('TRANS_DT',np.int64),('TRANS_AMT',np.int64),
                               ('OTHER_ID', '|S10'),('MEDIAN_AMT_BY_ZIP',np.int64),('DONATION_COUNT',np.int64),('TOTAL_AMT',np.int64)])
        records = np.recarray((1,),dtype=records_dt)
        for line in f.readlines():
            record = line.strip('\n').split('|')
            relevant_data = [ record[i] for i in [0, 10, 13, 14, 15] ]
            relevant_data.extend((relevant_data[3],1,relevant_data[3]))
            relevant_data[1] = relevant_data[1][0:5]

            if relevant_data[0] == '' or len(relevant_data[1]) != 5 or relevant_data[3] == '' or relevant_data[4] != '':
                continue


    print records
medianvals_by_zip(filepath)