# find-political-donors

### Approach to Problem

#### Data Extraction
In order to create the two requested outputs I decided to take a modular approach. By making a number of functions to 
complete the necessary data extraction and analysis I could easily test and change my programs as necessary. My first 
step was to create a way to read in the data. Since the data is to be treated as a data stream my program opens the file 
and reads each line individually until there are no longer any lines containing data. In both programs the 
extract_data(line) function extracts the full line of data and split into a list. The function then checks to see to see 
if the data is in the proper FEC Dictionary format (i.e. there are 21 pipe-separated data points). If this requirement 
is met the data from the necessary columns is extracted to a new list that is returned by the function for further 
processing. 

After each line of data is read and the necessary datapoints ahve been stored I decided to perform number of checks to 
see if the data conforms to the requirements of the problem. The programs use either check_zip_data_requirements(line_of_data) 
and check_date_data_requirements(line_of_data) to check for the output specific input considerations. If any of the 
tests fail that line of data is ignored and the next line is read/processed.

These input considerations differ slightly for the medianval_by_zip and medianvals_by_date scripts. Included in the 
requirement checks done by check_date_data_requirements(line_of_data) is a test to see if the date is future date, and 
thus, invalid. check_zip_data_requirements(line_of_data) performs a check to see if the zip code is present and in a 
valid format. If all tests are passed the list of data is stored in numpy recarray. (The decision to use a recarray is 
explained in the **Data Storage and Output** section of this ReadMe file.)

#### medianvals_by_zip.py

Once the data is extracted and checked for any format errors. I decided that I needed a way to organize the data by 
cmte_id and zip code and then add transaction amounts as the data was read in. I decided to store the donation amounts 
for each cmte_id/zip_code in a dictionary with the format {cmte_id:{zip_code:[donation amounts]}. The 
update_donations(data,donations_dictionary) function attributes each donation amount to the appropriate cmte_id and 
zipcode. The new median, transaction count, and transactions total are then calculated each time a new line of data is 
read and processed. The new row of data is then appended to the output table and then the new table iswritten out to the 
user-specified output file when run from the command line.

#### medianvals_by_date.py

The approach for medianvals_by_date was similar to medianvals_by_zip. After extracting and processing the data
I used a similarly structure dictionary: {cmte_id:{transaction_date:[donation amounts]}. The 
update_donations(data,donations_dictionary) function in this program attributes each transaction amount  a unique 
cmte_id/date combination for the entire file. 

Once all of the data has been entered into the correct CMTE_ID key and TRANSACTION_DATE sub-key in the candidates 
dictionary the median value, total number of donations, and total amount of the donations are calculated by 
calculate_stats_by_date(donations_dictionary) for each unique CMTE_ID/TRANSACTION_DATE combination. This information is 
then moved into a numpy array with each row having a unique CMTE_ID/TRANSACTION_DATE combination and that combinations
required calculated columns. The full array is then sorted alphabetically by CMTE_ID and chronologically by 
TRANSACTION_DATE. The full array is then written out to the user specified output file when run from the command line.

#### Data Storage and Output
Since the data being read in has both character and numerical data I decided to use a numpy recarray to store the data
that was read in. The recarray also allowed for easier accession and Numpy's savetotxt method also made writing the file
to the necessary output file much more efficient. 

### Run Instructions

Using the run.sh from the project root directory will run both medianvals_by_zip.py and medianvals_by_date.py
using the ~/find_political_donors/input/itcont.txt file as input and writing the results out to the
~/find_political_donors/output folder. The input/output file can be changed by editing the run.sh file.

From the command line the scripts can be run using:

python ./src/medianvals_by_zip.py input_file output_file\
**or**\
python ./src/medianvals_by_date.py input_file output_file>\
 
Either script can also be called without any arguments to see the usage message

### Dependencies

numpy\
argparse\
os
