# find-political-donors

### Approach to Problem

#### Data Extraction
In order to create the two requested outputs I decided to take a modular approach. 
My first step was to read in the data. Since the data is coming in as a stream my program
reads each line until there are no longer any lines containing data. The data of interest is then
extracted from the full line and stored for processing. I decided to first split the data into a list and checked to see
if it is in the proper FEC Dictionary format(i.e. there are 21 pipe-separated data points). Once this requirement is 
checked the necessary data is extracted and stored in a list for further processing.

After each line is read and stored I decided to perform number of checks to see if the data 
conforms to the requirements of the problem. If any of the tests fail that line of data is ignored. 
These requirements differ slightly for the medianval_by_zip and medianvals_by_date scripts. Included in the requirement
checks for medianvals_by_date is a check to see if the date is in the future, and thus, invalid. If all tests are passed
the list of data is stored in numpy recarray. (The decision to use a recarray is explained in the **Data Storage and 
Output** section of this readme file.)

#### medianvals_by_zip.py

Once the data is extracted and checked for any format errors. I decided that I needed a way to organize the data by 
cmte_id and zip code and then add transaction amounts as the data was read in. I decided to store the donation amounts 
for each cmte_id/zip_code in a dictionary with the format {cmte_id:{zip_code:[donation amounts]}. This allows each donation
amount to be attributed to the appropriate cmte_id and zipcode. The new median, count, and total are then calculated 
each time a new line of data is read. The new output table is then written out to the user-specified output file.

#### medianvals_by_date.py

The approach for medianvals_by_date was similar to medianvals_by_zip. After extracting and processing the data
I used a similarly structure dictionary: {cmte_id:{transaction_date:[donation amounts]}. This dictionary is then sorted
so that the CMTE_ID's are in alphabetical order and their dates are in chronological order. The median value, total number 
of donations, and total amount of the donations for each cmte_id and date are calculated each time a new row of data is 
read in. One row for each cmte_id and date is written out to the user-specified output file.

#### Data Storage and Output
Since the data being read in has both character and numerical data I decided to use a numpy recarray to store the data
that was read in. The recarray also allowed for easier accession and Numpy's savetotxt method also made writing the file
to the necessary ouput file much more efficient. 

### Run Instructions

Using the run.sh from the project root directory will run both medianvals_by_zip.py and medianvals_by_date.py
using the ~/find_political_donors/input/itcont.txt file as input and writing the results out to the
~/find_political_donors/output folder. The input file can be changed by editing the run.sh file.

From the command line the scripts can be run using:

python ./src/medianvals_by_zip.py input_file output_file\
**or**\
python ./src/medianvals_by_date.py input_file output_file>\
 
Either script can also be called without any arguments to see the usage message

### Dependencies

numpy\
argparse\
os
