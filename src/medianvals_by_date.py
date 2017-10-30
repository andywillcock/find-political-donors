import argparse
import numpy as np
from datetime import datetime

def extract_data(line):
    """
    Checks for the proper format as described by the FEC Dictionary (21 values), extracts neccessary data from the full line of pipe
    separated values in the line from the input file, and appends three more items as place holders for the running
    median, donation count, and total donation amount.
    :param line: line of pipe separated values
    :return: record_data: list of [cmte_id, zip_code, transaction date, transaction amount, other_id]
    """
    record = line.strip('\n').split('|')
    # Check to see if the line of data is in the format described by the FEC data dictionary. Each line needs to have
    # 21 pipe-separated values
    if len(record) != 21:
        record_data = False
    else:
        # Extract cmte_id, zipcode, date, transaction amount, and other id from full line of data
        record_data = [record[i] for i in [0, 10, 13, 14, 15]]
        record_data.extend((record_data[3], 1, record_data[3]))
        # Strip any spaces from the zipcode data and extract the first five numbers
        record_data[1] = record_data[1].strip(" ")[0:5]
    return record_data

def check_date_data_requirements(line_of_data):
    """
    Check data for relevancy using the rules defined in the data considerations section
            Check that CMTE_ID exists
            Check that the date is the not empty, is the correct length, and the date is not in the future
            Check to make sure that the TRANSACTION_AMT is not empty
            Check to make sure that OTHER_ID is empty
            If any of these are true the row is skipped
    :param line_of_data: relevant data extracted from line of input data file
    :return: good_data = True if requirements are met, False if not
    """
    now = datetime.now()
    good_data = True
    if line_of_data[0] == '' or line_of_data[2] == '' or len(line_of_data[2].strip(" ")) != 8 \
        or datetime.strptime(line_of_data[2],'%m%d%Y') > now or line_of_data[3] == '' or line_of_data[4] != '':
        good_data = False
    return good_data

def update_donations(data,donations_dictionary):
    """
    Adds each line of data's donation amount to the appropriate cmte_id and date
    :param data: numpy recarry of one row of the data of interest.
    :param donations_dictionary: dictionary with the structure {cmte_id:{date:[donations]}}
    :return: data: numpy recarray of data with new calculated columns included
             donations_dictionary: dictionary with cmte_id's zip code updated with new donations from the input data
    """
    cmte_id = data.CMTE_ID.item()
    date = data.TRANS_DT.item()
    trans_amt = data.TRANS_AMT.item()

    # Fill in dictionary with each unique candidate/date and that date's transaction amounts
    if data.CMTE_ID.item() in donations_dictionary.keys():

        if date in donations_dictionary[cmte_id].keys():
            donations_dictionary[cmte_id][date].append(trans_amt)
        else:
            donations_dictionary[cmte_id][date] = [trans_amt]
    else:
        donations_dictionary[cmte_id] = {date:[trans_amt]}

    return data, donations_dictionary

def calculate_stats_by_date(donations_dictionary):
    """
    Calculates the median, total amount, and transaction count for each candidate by date and create
    :param donations_dictionary: dictionary with format {cmte_id:{date:[donations]}}
    :return: output records: list of lists - each being a row for a candidate and a date with the median donation
                             amount for that date, total number of donations, and total amount of the donations
    """
    output_records = []

    for cand in donations_dictionary.keys():
        for key in donations_dictionary[cand].keys():
            date = key
            median = int(round(np.median(donations_dictionary[cand][key]).item(), 0))
            total = int(sum(donations_dictionary[cand][key]))
            count = len(donations_dictionary[cand][key])
            row = [cand, date, str(median), str(count), str(total)]
            output_records.append(row)
    return output_records


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
        candidate_donations = {}

        # Read each line, split into a list using separator |, pull necessary data out, add placeholders for data
        # to be calculated, and filter zipcode data for the first 5 digits

        for line in f:
            # Extract relevant data from the line of data
            relevant_data = extract_data(line)

            # Check data for formatting and other requirements
            data_check = check_date_data_requirements(relevant_data)
            if data_check == False:
                continue

            # Create numpy recarray of relevant data for value easier accession
            relevant_data = np.rec.array(relevant_data, dtype=records_dt)

            relevant_data, candidate_donations = update_donations(relevant_data, candidate_donations)

        #Create output_array using loop. Loops thorugh each date for each candidate, creates a row for that candidate/date
        # and then filling the row with the appropriate statistics
        output_records = calculate_stats_by_date(candidate_donations)

        # Create numpy array of all records
        output_records = np.array(output_records,dtype = '|S10')

        # Sort output alphabetically by cmte_id and then chronologically by date
        ind = np.lexsort((output_records[:,1],output_records[:,0]))
        output_records = output_records[ind]

        # Output output_records array to the correct folder as medianvals_by_date.txt
        np.savetxt(output_filepath_dates, output_records, delimiter='|', fmt="%s")

    f.close()
    return output_records

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file',
                        help='filepath containing input data')
    parser.add_argument('output_file',
                        help='filepath to store output data')
    args = parser.parse_args()
    input_filepath = args.input_file
    output_filepath_dates = args.output_file
    medianvals_by_date(input_filepath, output_filepath_dates)