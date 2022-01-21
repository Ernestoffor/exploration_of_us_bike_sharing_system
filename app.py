from itertools import count
from math import dist
from turtle import title, width
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import time
import datetime

from bikeshare import load_data, time_stats, station_stats, trip_duration_stats, user_stats

st.set_page_config(layout="wide")
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

st.image("image/logo.jpg", width=100)
st.title("Exploration of US Bikeshare Data in Popular Cities")



with st.sidebar:
    city = st.selectbox("Select The City To Explore: ", ('Chicago', 'New York City', "Washington"))
    city = city.lower()
    st.write('')
    st.write('')
    month = st.selectbox("Choose Month:  ", ('all', 'january', 'february', 'march', 'april', 'may', 'june'))
    st.write('')
    st.write('')
    day = st.selectbox("Which Day are you interested in?:  ", ('all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'))
    st.write('')
    st.write('')
    df = load_data(city, month, day)
    st.write('')
    st.subheader("Important Descriptive Statistics of the Bikeshare")
    st.metric("Total times of Bikeshare Usage:", value= df.shape[0])
    popular_month, pop_day_of_week, pop_hour, count_of_most_popular_month = time_stats(df)
    st.metric(label="Most Popular Month:", value=popular_month)
    st.metric(label="Number of Times of Usage in Most Popular Month:", value=count_of_most_popular_month)
    st.metric(label="Most Popular Day of the Week:", value=pop_day_of_week)
    st.metric(label="Most Popular Hour of Usage:", value=pop_hour)

    st.write('')
    url = "https://github.com/Ernestoffor/"
    st.write("Check out the Project Github Repository [here](%s)" % url)
    twitter = 'https://twitter.com/ErnestOffor'
    st.markdown("[![Github](https://i.ibb.co/Kr8V2QZ/github-logo.png)]({})".format(url))

    st.write('')
    st.markdown("[![Twitter](https://i.ibb.co/7brL667/twitter-logo.jpg)](https://twitter.com/ErnestOffor)")
    


# Divide the Page into Two Columns
col1, col2 = st.columns(2)


with col1:
    popular_start_station, popular_end_station, pop_trip, df_pop_trip = station_stats(df, num_stations=10)
    with st.expander("View the Bar and Pie Charts of the 10 Most Popular Trips"):
        fig = px.bar(df_pop_trip, y="frequency", x="trips", color="trips", title="10 Most popular trips in {}".format(city))
        st.plotly_chart(fig)
        fig1 = px.pie(df_pop_trip, values='frequency', names='trips', title = "The 10 most Popular Trips")
        st.plotly_chart(fig1)

    st.subheader("View the Stations Crucial Information")
    st.write("Most Popular Start Station: ")
    st.write(popular_start_station) 
    st.write('')
    st.write("Most Popular End Station: ")
    st.write(popular_end_station)
    st.write('')
    st.write("Most Popular Trip: " )
    st.write(pop_trip)

    total_travel_time, average_time, longest_trip_duration, fastest_trip_duration, longest_trip, fastest_trip = trip_duration_stats(df)
    st.write('')
    st.markdown("**Trip Time Information**")
    st.metric("The Total Time for All Trips in Seconds: ", total_travel_time)
    st.metric("The Longest Trip Duration in Seconds: ", value= longest_trip_duration, delta=longest_trip_duration - average_time)
    st.metric("The Average Trip Duration in Seconds: ", value= average_time)
    st.metric("The Shortest Trip Duration in Seconds: ", value = fastest_trip_duration, delta=fastest_trip_duration - average_time)
    st.write('')
    st.write("The Fastest Trip: ")
    st.write(fastest_trip)
    st.write('')
    st.write("The Longest Trip: ")
    st.write(longest_trip)
    
    st.write('')
    st.write('')
    with st.expander('Hide/Show the raw data'):
        length = df.shape[0]
        st.session_state.start  = st.radio("Select the index to start with", (0, 0))
        st.session_state.interval = st.radio("Choose intervals", (5,5))
        con = st.selectbox("Do you want to load first 5 rows of the raw data?",
        ('No', 'Yes'))
        if con.lower() =='yes':
            st.write("The Raw Dataset from {} Bikeshare: ".format(city.title()))
            st.table(df.iloc[st.session_state.start: st.session_state.start + st.session_state.interval, :])

        
        #st.dataframe(df.iloc[st.session_state.start: st.session_state.start + st.session_state.interval, :])
        #while st.session_state.start < length:
        for i in range(0, length):
            st.session_state.key = i
            
            choice = st.selectbox("Do you want to load the next 5 rows of the raw data?",
        ('No', 'Yes'), key = st.session_state.key)
            
            if choice.lower() =='yes':
                st.session_state.start += st.session_state.interval
                st.write("The Next Five Rows of Raw Dataset from {} Bikeshare: ".format(city.title()))
                st.table(df.iloc[st.session_state.start: st.session_state.start + st.session_state.interval, :])
            else:
                break
               
       
with col2:
   st.header("Users Information")
   df_user_type, earliest_usage, most_recent_usage, fig = user_stats(df)
   
   st.plotly_chart(fig)
   st.write('')

   
   st.write('Earliest Usage of the Bikeshare: ')
   st.write(earliest_usage)
   st.write('')
   st.write('The Most Recent Usage of the Bikeshare')
   st.write(most_recent_usage)
   st.write('')
   

   if city.lower() != 'washington':
       # Convert the Gender series to dataframe
       gender= df['Gender'].value_counts().to_frame()
       gender.insert(0, 'gender', gender.index)
       gender= gender.reset_index().drop('index', axis=1)
       gender.rename(columns={'Gender': 'frequency'} , inplace=True)
       gender_count = df['Gender'].value_counts()
     
       st.write("The Gender Spread of the Users is as follows: ")
       st.table(gender)
    # Display the user gender Graphically
       fig1 = px.pie(gender, values='frequency', names='gender', title = "The Bikesare Users By Gender")
       st.plotly_chart(fig1)

       most_users_by_yob = df[df['Birth Year'] == df['Birth Year'].mode()[0]] # ['Birth Year'][:1]
       most_users_by_yob = most_users_by_yob.iloc[0]['Birth Year']
       avg_yob = df['Birth Year'].mean()
       num_of_most_users_by_yob = df[df['Birth Year'] == df['Birth Year'].mode()[0]].shape[0]
       st.metric('The most common users of the bikeshare  are born in: ', most_users_by_yob, delta=most_users_by_yob - avg_yob)
       
       #
       st.write('')
       st.metric("Number Of Users with Modal Year of Birth:", num_of_most_users_by_yob)


    