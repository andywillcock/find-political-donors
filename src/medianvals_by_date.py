import os
import numpy as np
import datetime
import sys

def check_date_data_requirements(line_of_data):
    """
    Check data for relevancy using the rules defined in the data considerations section
            Check that CMTE_ID exists
            Check that the date is the not empty, is the correct length, and the year is not greater than the present year
            Check to make sure that the TRANSACTION_AMT is not empty
            Check to make sure that OTHER_ID is empty
            If any of these are true the row is skipped
    :param line_of_data: relevant data extracted from line of input data file
    :return: good_data = True if requirements are met, False if not
    """
    now = datetime.datetime.now()
    good_data = True
    if line_of_data[0] == '' or line_of_data[2] == '' or len(line_of_data[2].strip(" ")) != 8 \
        or int(line_of_data[2][-4:]) > now.year or line_of_data[3] == '' or line_of_data[4] != '':
        good_data = False
    return good_data

def medianvals_by_date(input_filepath, output_filepath_dates):
    """
    Opens input file of individual political contributions as a stream, reads each line of data, calculates the median,
    total number of donations, and total donation amounts for each candidate by date. Writes out a pipe separated txt
    file with each newline including the candidate ID number, date, and calculated statistics for each unique date
    for a candidate

    :param input_ filepath: path to data file for input
    :param output_filepath_dates: path for .txt file output
    :return: output_records: numpy array of candidate ID number, date, and calculated statistics. Each row is a unique
    date for a given candidate
    """

    with open(input_filepath, 'r') as f:

        # Define variable types of each possible column
        records_dt = np.dtype([('CMTE_ID', '|S10'), ('ZIP_CODE', '|S10'), ('TRANS_DT', '|S10'), ('TRANS_AMT', np.float64),
                               ('OTHER_ID', '|S10'), ('MEDIAN_AMT_BY_DATE', np.int64), ('DONATION_COUNT', np.int64),
                               ('TOTAL_AMT', np.int64)])

        # Read data file line by line and add relevant data to a dictionary.
        # Dictionary Structure = { CMTE_ID : {TRANS_DT : [TRANS_AMT,TRANS_AMT]}, CMTE_ID : {TRANS_DT : [TRANS_AMT(s)]}, etc. }
        candidates = {}

        # Read each line, split into a list using separator |, pull necessary data out, add placeholders for data
        # to be calculated, and filter zipcode data for the first 5 digits

        for line in f:
            record = line.strip('\n').split('|')
            relevant_data = [record[i] for i in [0, 10, 13, 14, 15]]
            relevant_data.extend((relevant_data[3], 1, relevant_data[3]))
            relevant_data[1] = relevant_data[1][0:5]

            data_check = check_date_data_requirements(relevant_data)
            if data_check == False:
                continue


            # Create numpy recarray of relevant data for value easier accession
            relevant_data = np.rec.array(relevant_data, dtype=records_dt)

            # Fill in dictionary with each unique candidate/date and that date's transaction amounts
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

        #Create output_array using loop. Loops thorugh each date for each candidate, creates a row for that candidate/date
        # and then filling the row with the appropriate statistics
        output_records = []
        for cand in candidates.keys():
            for key in candidates[cand].keys():
                date = key
                median = int(round(np.median(candidates[cand][key]).item(),0))
                total = int(sum(candidates[cand][key]))
                count = len(candidates[cand][key])
                row = [cand,date,str(median),str(count),str(total)]
                output_records.append(row)

        # Create numpy array of all records
        output_records = np.array(output_records,dtype = '|S10')

        # Output output_records array to the correct folder as medianvals_by_date.txt
        np.savetxt(output_filepath_dates, output_records, delimiter='|', fmt="%s")

    return output_records

if __name__ == '__main__':
    input_filepath = sys.argv[1]
    output_filepath_dates = sys.argv[2]
    medianvals_by_date(input_filepath, output_filepath_dates)