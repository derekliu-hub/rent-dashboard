import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.title('Rent Index Dashboard')

st.markdown('This dashboard displays the Zillow Observed Rent Index for any of the 50 largest cities in the US over a select time period. Zillow\'s metric seeks to measure the typical observed market rate rent across different cities while accounting for differences in the quality of the available rental stock. Details on the methodology are explained here: https://www.zillow.com/research/methodology-zori-repeat-rent-27092/')
st.markdown('The bottom bar chart displays the percent change in rent between the end and start dates for all the selected cities. Toggling the checkboxes reveals the change in rents in US cities as a whole and the change in the CPI for urban consumers excluding cost of housing.')

@st.cache_data
def load_zillow_data(rent_csv):
    df = pd.read_csv(rent_csv)[0:50]
    df = (df.drop(columns=['RegionID', 'SizeRank', 'RegionType', 'StateName', 'State', 'Metro', 'CountyName'])
            .set_index('RegionName')
            .transpose()
            .interpolate()
            .round(2)
            )
    return df

df = load_zillow_data('City_zori_uc_sfrcondomfr_sm_month.csv')

cities = sorted(df.columns)
selected_cities = st.sidebar.multiselect('Select Cities', cities, ['New York', 'Los Angeles', 'Chicago'])

dates = df.index
start_date = st.sidebar.selectbox('Select Start Date', dates, index=0)
end_date = st.sidebar.selectbox('Select End Date', dates, index=len(dates)-1)

df_plot = df[selected_cities][start_date:end_date]
df_plot = df_plot.reindex(sorted(df_plot.columns), axis=1)

show_cpi_rent = st.sidebar.checkbox('Display Change in CPI for Rent of Primary Residence in U.S. City Average')
show_cpi_exrent = st.sidebar.checkbox('Display Change in CPI for All Items Less Shelter in U.S. City Average')

if start_date >= end_date:
    st.write("Please pick an end date that comes after the start date")
else:
    st.subheader('Rent of Cities Over Time')
    fig = px.line(df_plot, labels={'index': 'Date', 'value': 'Average Rent (USD)', 'RegionName': 'City'})
    st.write(fig)

    if show_cpi_rent:
        cpi_rent = pd.read_csv('CUUR0000SEHA.csv')
        cpi_rent = cpi_rent.rename(columns={'CUUR0000SEHA': 'Average US City Rent'})
        cpi_rent['DATE'] = cpi_rent['DATE'].str[0:7]
        
        df_plot['DATE'] = df_plot.index.str[0:7]
        df_plot = df_plot.join(cpi_rent.set_index('DATE'), on='DATE')
        df_plot = df_plot.drop('DATE', axis=1)

    if show_cpi_exrent:
        cpi_exrent = pd.read_csv('CUUR0000SA0L2.csv')
        cpi_exrent = cpi_exrent.rename(columns={'CUUR0000SA0L2': 'CPI Excluding Shelter'})
        cpi_exrent['DATE'] = cpi_exrent['DATE'].str[0:7]
        
        df_plot['DATE'] = df_plot.index.str[0:7]
        df_plot = df_plot.join(cpi_exrent.set_index('DATE'), on='DATE')
        df_plot = df_plot.drop('DATE', axis=1)

    percent_change = (df_plot.loc[end_date] - df_plot.loc[start_date]) / df_plot.loc[start_date] * 100
    percent_change = percent_change.round(2).to_frame()
    percent_change["Color"] = np.where(percent_change.astype(float)<0, 'red', 'green')

    st.subheader('Percent Change')
    fig = go.Figure()
    fig.add_trace(go.Bar(x=percent_change[0], y=percent_change.index, orientation='h', marker_color=percent_change['Color']))
    fig.update_layout(xaxis_ticksuffix = '%', yaxis=dict(autorange="reversed"))
    st.write(fig)