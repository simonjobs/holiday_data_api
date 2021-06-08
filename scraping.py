import pandas as pd
import requests
from bs4 import BeautifulSoup

# Starting point for data collection
url = 'https://www.officeholidays.com/countries'

# Scrape list of all countries available on the site
r = requests.get(url)
html = r.text
soup = BeautifulSoup(html)
columns = soup.find_all('div', {"class": "four omega columns"})
countries = []
for column in columns:
    rows = column.find_all('li')
    for row in rows:
        countries.append(row.find('a').text[2:])

# Structure countries
countries_processed = []
for country in countries:
    country = country.replace(' ', '-')
    country = country.replace('é', 'e')
    countries_processed.append(country.lower())

# Clean data manually
countries_processed[25] = 'bonaire-st-eustatius-saba'
countries_processed[64] = 'swaziland'
countries_processed[149] = 'macedonia'
countries_processed[208] = 'uae'

# Function used to convert dates later
def convert_month(txt):
    dictionary = {'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
                  'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
                  'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'}
    
    for k, v in dictionary.items():
        if txt.lower() == k:
            return dictionary[k]

# Create lists of years to collect data from and create empty dataframe
years = list(range(2016,2023))
df = pd.DataFrame()

# Start loop to collect holidays for each country
for index, country in enumerate(countries_processed):
    for year in years:
        count = 0
        data = []

        # Create specific url for country and year
        tmp_url = url + '/' + country + '/' + str(year)
        
        # Navigate HTML and scrape the table
        r = requests.get(tmp_url)
        if r.status_code == 200:
            html = r.text
            soup = BeautifulSoup(html)
            table = soup.find('table', {'class': 'country-table'})
            if table:
                rows = table.find_all('tr')
                for row in rows[1:]:
                    cols = row.find_all('td')
                    cols = [ele.text.strip() for ele in cols]
                    data.append([ele for ele in cols if ele])

                # Fill temporary df with the scraped table
                df_tmp = pd.DataFrame(data)

                # Iterate over each row in the collected table and restructure data in series
                # before appending to df
                for i, row in df_tmp.iterrows():
                    tmp = pd.Series([str(year)+'-'+convert_month(row[1][:3])+'-'+row[1][-2:], row[2], countries[index]])
                    df = df.append(tmp, ignore_index=True)
    print(index,'/',len(countries))

# Rename columns for readability when proceeding
df.columns = ['date', 'holiday', 'country']

# Scrape ISO country codes in order to merge with holiday data
url = 'https://www.iban.com/country-codes'

r = requests.get(url)
html = r.text
soup = BeautifulSoup(html)
table = soup.find('table', {"class": "table table-bordered downloads tablesorter"})
rows = table.find_all('tr')
data = []
for row in rows[1:]:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])
    
df_iso = pd.DataFrame(data, columns=['country', 'iso-2', 'iso-3', 'code'])

# Merge drops about 40 countries due to overlaps and under-cleaned data, can be improved with manual work.
# We only want to keep the iso-3 column
df = pd.merge(df, df_iso, on=['country', 'country'])
df.drop(['iso-2','code'], axis=1, inplace=True)

# Change column names and finally save df as csv
df.columns = ['date', 'holiday', 'country', 'iso']
df.to_csv('api/holiday_scraped.csv', index=False)



