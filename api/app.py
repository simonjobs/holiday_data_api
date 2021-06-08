import flask
from flask import request, jsonify
import pandas as pd
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Import data from CSV
df_holiday = pd.read_csv('holiday_scraped.csv')

# Set simple description on home page
@app.route('/', methods=['GET'])
def home():
    return '''<h1>Holiday API</h1>
    <p>API for verifying holidays per country and date. <br> 
    Returns True if holiday and False if not. Also, summarizing <br> 
    the amount of holiday days per country and year.</p>'''


# End-point that can be used to fetch a summary of holidays per country
@app.route('/api/summary', methods=['GET'])
def api_summary():
    # Use pandas groupby function on the dataframe to count unique days per country
    # keeping iso code as well. 
    df_summary = df_holiday.groupby(['country', 'iso']).count()
     
    # Find and iterare through all unique years in dataframe adding a column to df_summary
    # for each year.
    for year in df_holiday.date.astype(str).str[:4].unique():
        df_tmp = df_holiday[df_holiday.date.astype(str).str[:4] == year]
        df_tmp = df_tmp.groupby(['country', 'iso']).count()
        df_summary[year] = df_tmp['date']
    
    # Format the new dataframe and drop all unwanted columns
    df_summary.reset_index(inplace=True)
    df_summary.drop(['holiday', 'date'], axis=1, inplace=True)
    df_summary = df_summary.reindex(sorted(df_summary.columns), axis=1)

    # Return a json of the dataframe organized by country.
    return df_summary.to_json(orient='records')

# End-point to fetch if a certain date in a certain country is a holiday
@app.route('/api', methods=['GET'])
def api_country():

    # Parse through received parameters
    params = request.args

    # Only continue if both country and date are sent
    # Currently minimal input control
    if 'iso' in request.args and 'date' in request.args:
        iso = params.get('iso').upper()
        date = params.get('date')

        # Get results for country and date
        query = df_holiday.loc[(df_holiday['iso'] == iso) & (df_holiday['date'] == date)]

        # If result is atleast one holiday return true, else false
        if len(query) > 0:
            return json.dumps(True)
        else:
            return json.dumps(False)
    else:
        return "Error: Insufficient parameters, please provide country and date."

if __name__ == "__main__":
    app.run()