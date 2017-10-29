# find-political-donors

### Approach to Problem

##### Data Extraction
In order to create the two requested outputs I decided to take a modular approach. 
My first step was to read in the data. Since the data is coming in as a stream my program
reads each line until there are no longer and lines containing data. The data of interest is then
extracted from the full line and stored for processing.

After each line is read and stored I decided to perform number of checks to see if the data 
conforms to the requirements of the problem. If any of the tests fail that line of data is ignored. 
These requirements differ slightly for the medianval_by_zip and medianvals_by_date scripts.

#### medianvals_by_zip.py

Once the data is extracted and checked I decided that in order to calculate the running median,
count, and total I should store the donation amounts in a dictionary with the format 
{cmte_id:{zip_code:[donation amounts]}. This allows each donation amount to be attributed to the 
appropriate cmte_id and zipcode and then the new median, count, and total to be calculated and output
as a new row in the output file.

#### medianvals_by_date.py

The approach for medianvals_by_date was similar to medianvals_by_zip using a similarly structure dictionary, 
{cmte_id:{transaction_date:[donation amounts]} the median value, total number of donations, and total amount of
the donations for that cmte_id and date were calculated and one row for each cmte_id and date was written out to 
the output file.



### Dependencies

numpy\
argparse\
os