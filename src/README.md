This directory contains two python scripts, one for each required output. Instructions on running these scripts can be 
found in the project root README.md file

### medianvals_by_zip.py

Reads in individual donor data in the FEC specified format and outputs a pipe separated .txt file with the fields:

The recipient of the contribution (or CMTE_ID from the input file)\
Zip Code of where the contribution came from (or TRANSACTION_DT from the input file)\
Running median of contributions received by recipient from that zip code rounded to the nearest whole dollar\
Running total number of transactions received by recipient on that date\
Runnning otal amount of contributions received by recipient on that date


### medianvals_by_date.py

Reads in individual donor data in the FEC specified format and outputs a pipe separated .txt file with the fields

The recipient of the contribution (or CMTE_ID from the input file)\
Date of the contribution (or TRANSACTION_DT from the input file)\
Median of contributions received by recipient on that date rounded to the nearest whole dollar\
Total number of transactions received by recipient on that date\
Total amount of contributions received by recipient on that date
