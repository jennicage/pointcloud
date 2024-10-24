#!/usr/bin/env python
# coding: utf-8

# # Streamlit App : Point Clouds on a Map

# python -m streamlit run app.py
# 
# http://localhost:8501

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib
import streamlit as st
from streamlit_jupyter import StreamlitPatcher, tqdm
from datetime import datetime, date, timedelta
import plotly.express as px
from scipy.spatial import ConvexHull


# In[ ]:


# visualization of points on the map base

def datapoints_map(dff):
    points = dff[['longitude', 'latitude']].values
    hull = ConvexHull(points)
    hull_points = points[hull.vertices]
    hull_points = np.append(hull_points, [hull_points[0]], axis=0)

    fig = px.scatter_mapbox(dff, lat='latitude', lon='longitude',
                            color_discrete_sequence=['deeppink'], zoom=15, height=600)

    fig.update_traces(marker=dict(size=2.5, opacity=0.9))

    fig.add_trace(px.line_mapbox(
        pd.DataFrame(hull_points, columns=['longitude', 'latitude']),
        lat='latitude', lon='longitude').data[0])

    fig.update_layout(mapbox_style="open-street-map")
    return fig


# In[ ]:


st.title("Point Cloud Visualization")
st.subheader ("Case Friskalanlahti", divider='rainbow')


# In[ ]:


uploaded_file = st.file_uploader("Choose file")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, parse_dates=['aika'])

    # set locked date range 
    start_lock = datetime(2024, 6, 4).date() 
    end_lock = datetime(2024, 9, 24).date()   

    # use date_input with a locked date range
    start_date = st.date_input('Start', start_lock, min_value=start_lock, max_value=end_lock, key=5)
    end_date = st.date_input('End', end_lock, min_value=start_lock, max_value=end_lock, key=6)

    otos = df[(df['aika'].dt.date >= start_date) & (df['aika'].dt.date <= end_date)]
    
    # generate the map
    fig = datapoints_map(otos)

    # display the map in the Streamlit app
    st.plotly_chart(fig)
else:
    st.write('No file, no go')

