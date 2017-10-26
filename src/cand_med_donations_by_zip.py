import os
import numpy as np
import datetime

filepath = '/Users/ATW/find-political-donors/input/itcont.txt'

def medianvals_by_zip(filepath):

    with open(filepath,'r') as f:
        records_dt = np.dtype([('CMTE_ID','|S10'),('ZIP_CODE', '|S10'),('TRANS_DT','|S10'),('TRANS_AMT',np.float64),
                               ('OTHER_ID', '|S10'),('MEDIAN_AMT_BY_ZIP',np.int64),('DONATION_COUNT',np.int64),('TOTAL_AMT',np.int64)])
        records = np.recarray((1,),dtype=records_dt)
        candidates = {}
        for line in f.readlines():
            record = line.strip('\n').split('|')
            relevant_data = [ record[i] for i in [0, 10, 13, 14, 15] ]
            relevant_data.extend((relevant_data[3],1,relevant_data[3]))
            relevant_data[1] = relevant_data[1][0:5]

            if relevant_data[0] == '' \
                    or len(relevant_data[1]) != 5 \
                    or relevant_data[3] == '' \
                    or relevant_data[4] != '':
                continue

            relevant_data = np.rec.array(relevant_data,dtype=records_dt)

            if relevant_data.CMTE_ID.item() in candidates.keys():

                if relevant_data.ZIP_CODE.item() in candidates[relevant_data.CMTE_ID.item()].keys():
                    candidates[relevant_data.CMTE_ID.item()][relevant_data.ZIP_CODE.item()].append(relevant_data.TRANS_AMT.item())
                else:
                    candidates[relevant_data.CMTE_ID.item()][relevant_data.ZIP_CODE.item()] = [relevant_data.TRANS_AMT.item()]
            else:
                candidates[relevant_data.CMTE_ID.item()] = {relevant_data.ZIP_CODE.item():[relevant_data.TRANS_AMT.item()]}

            relevant_data.MEDIAN_AMT_BY_ZIP = round(np.median(candidates[relevant_data.CMTE_ID.item()][relevant_data.ZIP_CODE.item()]).item(), 0)
            relevant_data.TOTAL_AMT = np.sum(candidates[relevant_data.CMTE_ID.item()][relevant_data.ZIP_CODE.item()])
            relevant_data.DONATION_COUNT = len(candidates[relevant_data.CMTE_ID.item()][relevant_data.ZIP_CODE.item()])

            records = np.vstack((records, relevant_data))

            output_records = np.hstack((records['CMTE_ID'], records['ZIP_CODE'], records['MEDIAN_AMT_BY_ZIP'],
                                        records['DONATION_COUNT'], records['TOTAL_AMT']))
            output_records = np.delete(output_records, (0), axis=0)

            np.savetxt(os.path.dirname(os.getcwd())+'/output/medianvals_by_zip.txt',
                       output_records, delimiter='|', fmt="%s")

    f.close()

medianvals_by_zip(filepath)

def medianvals_by_date(filepath):

    with open(filepath, 'r') as f:

        # Define variable types of each possible column
        records_dt = np.dtype([('CMTE_ID', '|S10'), ('ZIP_CODE', '|S10'), ('TRANS_DT', '|S10'), ('TRANS_AMT', np.float64),
                               ('OTHER_ID', '|S10'), ('MEDIAN_AMT_BY_DATE', np.int64), ('DONATION_COUNT', np.int64),
                               ('TOTAL_AMT', np.int64)])

        # Read data file line by line and add relevant data to a dictionary.
        # Dictionary Structure = { CMTE_ID : {TRANS_DT : [TRANS_AMT(s)]}, CMTE_ID : {TRANS_DT : [TRANS_AMT(s)]}, etc. }
        candidates = {}

        # Read each line, split into a list using separator |, pull necessary data out, add placeholders for data
        # to be calculated, and filter zipcode data for the first 5 digits
        for line in f.readlines():
            record = line.strip('\n').split('|')
            relevant_data = [record[i] for i in [0, 10, 13, 14, 15]]
            relevant_data.extend((relevant_data[3], 1, relevant_data[3]))
            relevant_data[1] = relevant_data[1][0:5]
            now = datetime.datetime.now()

            # Check data for relevancy using the rules defined in the data considerations section
            # Check that CMTE_ID exists
            # Check that the date is the not empty, is the correct length, and the year is not greater than the present year
            # Check to make sure that the TRANSACTION_AMT is not empty
            # Check to make sure that OTHER_ID is empty
            # If any of these are true the row is skipped
            if relevant_data[0] == '' \
                    or relevant_data[2] == '' or len(relevant_data[2]) != 8 or int(relevant_data[2][-4:]) > now.year  \
                    or relevant_data[3] == '' \
                    or relevant_data[4] != '':

                continue

            # Create numpy recarray of relevant data for value easier accession
            relevant_data = np.rec.array(relevant_data, dtype=records_dt)

            # Fill in dictionary with each unique candidate/zip code and that zip codes transactions
            if relevant_data.CMTE_ID.item() in candidates.keys():

                if relevant_data.TRANS_DT.item() in candidates[relevant_data.CMTE_ID.item()].keys():
                    candidates[relevant_data.CMTE_ID.item()][relevant_data.TRANS_DT.item()].append(
                        relevant_data.TRANS_AMT.item())
                else:
                    candidates[relevant_data.CMTE_ID.item()][relevant_data.TRANS_DT.item()] = [
                        relevant_data.TRANS_AMT.item()]
            else:
                candidates[relevant_data.CMTE_ID.item()] = {
                    relevant_data.TRANS_DT.item(): [relevant_data.TRANS_AMT.item()]}

        #Create Outputfile using loop to go through each date for each candidate create a row for that candidate/date
        # and then filling the row with the appropriate stats
        output_records = []
        for cand in candidates.keys():
            for key in candidates[cand].keys():
                date = key
                median = int(round(np.median(candidates[cand][key]).item(),0))
                total = int(sum(candidates[cand][key]))
                count = len(candidates[cand][key])
                row = [cand,date,str(median),str(count),str(total)]
                output_records.append(row)

        output_records = np.array(output_records,dtype = '|S10')

        np.savetxt(os.path.dirname(os.getcwd()) + '/output/medianvals_by_date.txt', output_records,
                   delimiter='|', fmt="%s")

    f.close()

medianvals_by_date(filepath)