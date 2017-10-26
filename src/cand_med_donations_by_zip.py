import os
import numpy as np

filepath = os.getcwd()+"/itcont.txt"
def medianvals_by_zip(filepath):


    with open(filepath,'r') as f:
        records_dt = np.dtype([('CMTE_ID','|S10'),('ZIP_CODE', '|S10'),('TRANS_DT',np.int64),('TRANS_AMT',np.float64),
                               ('OTHER_ID', '|S10'),('MEDIAN_AMT_BY_ZIP',np.int64),('DONATION_COUNT',np.int64),('TOTAL_AMT',np.float64)])
        records = np.recarray((1,),dtype=records_dt)
        candidates = {}
        for line in f.readlines():
            record = line.strip('\n').split('|')
            relevant_data = [ record[i] for i in [0, 10, 13, 14, 15] ]
            relevant_data.extend((relevant_data[3],1,relevant_data[3]))
            relevant_data[1] = relevant_data[1][0:5]

            if relevant_data[0] == '' or len(relevant_data[1]) != 5 or relevant_data[3] == '' or relevant_data[4] != '':
                continue

            relevant_data = np.rec.array(relevant_data,dtype=records_dt)

            if relevant_data['CMTE_ID'].item() in candidates.keys():

                if relevant_data['ZIP_CODE'].item() in candidates[relevant_data['CMTE_ID'].item()].keys():
                    candidates[relevant_data['CMTE_ID'].item()][relevant_data['ZIP_CODE'].item()].append(relevant_data['TRANS_AMT'].item())
                else:
                    candidates[relevant_data['CMTE_ID'].item()][relevant_data['ZIP_CODE'].item()] = [relevant_data['TRANS_AMT'].item()]
            else:
                candidates[relevant_data['CMTE_ID'].item()] = {relevant_data['ZIP_CODE'].item():[relevant_data['TRANS_AMT'].item()]}

                # donation = relevant_data['TRANS_AMT'].tolist()
                # new_zip_donations = records[np.where((records["ZIP_CODE"] == relevant_data["ZIP_CODE"])
                #                                     & (records["CMTE_ID"] == relevant_data["CMTE_ID"]))]['TRANS_AMT'].tolist()

                # new_zip_donations.append(donation)

            relevant_data['MEDIAN_AMT_BY_ZIP'] = np.round(np.median(candidates[relevant_data['CMTE_ID'].item()][relevant_data['ZIP_CODE'].item()]), 0)
            relevant_data['TOTAL_AMT'] = np.sum(candidates[relevant_data['CMTE_ID'].item()][relevant_data['ZIP_CODE'].item()])
            relevant_data['DONATION_COUNT'] = len(candidates[relevant_data['CMTE_ID'].item()][relevant_data['ZIP_CODE'].item()])

            records = np.vstack((records, relevant_data))
            # if relevant_data['ZIP_CODE'] in records['ZIP_CODE']:
            #     donation = relevant_data['TRANS_AMT'].tolist()
            #     new_zip_donations = records[np.where((records["ZIP_CODE"] == relevant_data["ZIP_CODE"])
            #                                         & (records["CMTE_ID"] == relevant_data["CMTE_ID"]))]['TRANS_AMT'].tolist()
            #
            #     new_zip_donations.append(donation)
            #
            #     relevant_data['MEDIAN_AMT_BY_ZIP'] = np.round(np.median(new_zip_donations), 0)
            #     relevant_data['TOTAL_AMT'] = np.sum(new_zip_donations)
            #     relevant_data['DONATION_COUNT'] = len(new_zip_donations)


        

    # print records
medianvals_by_zip(filepath)