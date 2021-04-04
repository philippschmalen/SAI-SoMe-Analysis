import streamlit as st
import pandas as pd
import plotly.express as px
from util.app_utilities import load_config, load_data
from datetime import datetime, tzinfo, date


st.title("Social media analysis @SAI")


# -- load config
config = load_config(filepath = "../settings.yml")
DATA_DIR           = config['data']['processed_dir']
PROCESSED_FILENAME = config['data']['processed_filename']

# -- load data
df = load_data(data_dir=DATA_DIR, filename=PROCESSED_FILENAME)
# -- process data
# date column: datetime format, remove timezone
df['date'] = pd.to_datetime(df['date']).dt.tz_localize(None) 




# -- choice by user

# choose platform
platform_options = df.platform.unique().tolist()
platform_selected = st.multiselect("Select platform(s)", 
							options=platform_options, 
							default=platform_options)
# choose time window
date_range = st.date_input("Date range (default: last 6 months)", 
	[df['date'].max() - pd.to_timedelta(180, unit='d'), 
	df['date'].max()])
# choose date detail level
date_unit_options = {'D': "daily", 'W': "weekly", 'M': "monthly"}
detail_level = st.selectbox("Detail level", 	options=list(date_unit_options.keys()), 
										format_func=lambda x: date_unit_options[x], 
										index=1)

# subset data for plot
	# date range
	# platform
	# date detail level
df_plot = (
	df.loc[
	df['date'].between(pd.to_datetime(date_range[0]), 
	pd.to_datetime(date_range[1])) & \
	df.platform.isin(platform_selected)
	]
		.groupby(['platform', pd.Grouper(key='date', freq=detail_level)])['value']
		.sum()
		.reset_index()
		.sort_values('date'))




# -- overall figure
st.write(f"""
		### Overall {df_plot.value.sum()} visits within the last {(date_range[-1]-date_range[0]).days} days.
	""")





# -- Line plot across time
fig = px.line(df_plot, x='date', y='value', color='platform', 
	labels={
		'date_grouping': "Date", 
		'value': 'Views'
	})

st.plotly_chart(fig)



# -- treemap of platform share
df_treemap = df_plot.groupby('platform').agg('sum').reset_index()
# calculate share
df_treemap['share'] = df_treemap.value/df_treemap.value.sum()*100
st.write("### Share of visits (for selected time and platforms)")

fig_tree = px.treemap(df_treemap, path=['platform'], values='share')
st.plotly_chart(fig_tree)





