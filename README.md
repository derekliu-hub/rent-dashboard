# Dashboard Showing Rent Data
Link to the dashboard app is [here](https://derekliu-rent-dashboard.streamlit.app/).

This repo contains the code and data used to build a Streamlit app that displays the change in average rent across the 50 largest cities in the US over a customizable time frame. There are three csv files here that serve as the data sources:
* "City_zori_uc_sfrcondomfr_sm_month.csv" contains the data from Zillow on the typical market rate rent across all kinds of homes for each city
* "CUUR0000SA0L2.csv" contains the data from the BLS on the Consumer Price Index for All Urban Consumers: All Items Less Shelter in U.S. City Average
* "CUUR0000SEHA.csv" contains the data from the BLS on the Consumer Price Index for All Urban Consumers: Rent of Primary Residence in U.S. City Average

All three data sets span from January 2015 to October 2024. They are not seasonally adjusted.