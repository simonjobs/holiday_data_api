# Case Study - Data Engineering

## The project contains:  
One folder containing a flask api application with all neccesarry files to build a docker image  
One additional Python script for data collection.  
Two notebooks used when prototyping the scripts  
One readme  

* scrape: Used to scrape holiday dates and country codes in ISO format, combine the data and save in csv format  
* api: Flask application that can return:  
	   Wether a certain date in a certain country is a holiday  
	   A summary of number of holiday days per country and year in the 'database'  
 
## Getting started:  
To start scraping holiday data go to scrape.py directory and run "python3 scrape.py"  

To create docker image for API run "docker build --tag <NAME> <PATH>"  
When completed run docker image through "docker run -p 5000:5000 <NAME>"  
Browse to 0.0.0.0:5000 to check connectivity  


## API documentation:  
Possible end-points:  
	* /api  
	* /api/summary  

### /api  
Takes two parameters 'ISO' and 'date', a request will fail if not both parameters are set.  
Parameters values are not case sensitive.  
If there is a match in the 'database' on country and date "True" will be returned, else "False".  
ISO needs to be in ISO-3 format with three letters, full list on available countrys at the end of this page.  

Example requests:  
http://0.0.0.0:5000/api?country=swe&date=2021-12-24 - True  
http://0.0.0.0:5000/api?country=SWE&date=2021-12-24	- True  
http://0.0.0.0:5000/api?country=AFG&date=2021-02-02	- False // Not a holiday  
http://0.0.0.0:5000/api?country=bgr&date=1990-01-24 - False // No data on this year  
http://0.0.0.0:5000/api?country=XXX&date=1990-01-24 - False // No data on this country or year  

### /api/summary  
Returns a JSON with two permanent columns, country and iso as well as one country for each year in 'database'  


### Available countries by ISO:  
	   'AFG', 'ALB', 'DZA', 'ASM', 'AND', 'AGO', 'AIA', 'ATG', 'ARG',  
       'ARM', 'ABW', 'AUS', 'AUT', 'AZE', 'BHR', 'BGD', 'BRB', 'BLR',  
       'BEL', 'BLZ', 'BEN', 'BMU', 'BTN', 'BES', 'BIH', 'BWA', 'BRA',  
       'BGR', 'BFA', 'BDI', 'KHM', 'CMR', 'CAN', 'TCD', 'CHL', 'CHN',  
       'COL', 'CRI', 'HRV', 'CUB', 'CUW', 'CYP', 'DNK', 'DJI', 'DMA',  
       'ECU', 'EGY', 'SLV', 'GNQ', 'ERI', 'EST', 'SWZ', 'ETH', 'FJI',  
       'FIN', 'FRA', 'GUF', 'PYF', 'GAB', 'GEO', 'DEU', 'GHA', 'GIB',  
       'GRC', 'GRL', 'GRD', 'GLP', 'GUM', 'GTM', 'GGY', 'GIN', 'GNB',  
       'GUY', 'HTI', 'HND', 'HKG', 'HUN', 'ISL', 'IND', 'IDN', 'IRQ',  
       'IRL', 'IMN', 'ISR', 'ITA', 'JAM', 'JPN', 'JEY', 'JOR', 'KAZ',  
       'KEN', 'KIR', 'KWT', 'KGZ', 'LVA', 'LBN', 'LSO', 'LBR', 'LBY',  
       'LIE', 'LTU', 'LUX', 'MDG', 'MWI', 'MYS', 'MDV', 'MLI', 'MLT',  
       'MTQ', 'MRT', 'MUS', 'MEX', 'MCO', 'MNG', 'MNE', 'MSR', 'MAR',  
       'MOZ', 'MMR', 'NAM', 'NPL', 'NCL', 'NZL', 'NIC', 'NGA', 'NOR',  
       'OMN', 'PAK', 'PAN', 'PNG', 'PRY', 'PER', 'POL', 'PRT', 'PRI',  
       'QAT', 'ROU', 'RWA', 'BLM', 'KNA', 'LCA', 'VCT', 'WSM', 'SMR',  
       'SAU', 'SEN', 'SRB', 'SYC', 'SLE', 'SGP', 'SVK', 'SVN', 'SLB',  
       'SOM', 'ZAF', 'SSD', 'ESP', 'LKA', 'SUR', 'SWE', 'CHE', 'TJK',  
       'THA', 'TGO', 'TON', 'TTO', 'TUN', 'TUR', 'TKM', 'UGA', 'UKR',  
       'URY', 'UZB', 'VUT', 'WLF', 'YEM', 'ZMB', 'ZWE'  


### Known bugs and faults:  
* Merge in scrape.py causes data from around 40 countries to disappear e.g. USA due to naming differences between ISO name and scraped name. Can be fixed with manual work.  

