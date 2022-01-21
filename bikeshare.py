import time
import pandas as pd
import numpy as np
from datetime import timedelta
import plotly.express as px
import plotly.graph_objects as go

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
     # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # convert the End Time column to datetime
    df['End Time'] = pd.to_datetime(df['End Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

   
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    # Drop this column called 'Unnamed: 0'
    df = df.drop('Unnamed: 0', axis=1)


    return df

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    INPUT:
        df - filtered dataframe
    OUTPUTS:
        total_travel_time (int) - total trips time in seconds
        average_time (float) - average trip time in seconds
        longest_trip_duration (int) - longest trip time in seconds
        fastest_trip_duration (int) - shortest trip time in seconds
        longest_trip (str)  - longest trip
        fastest_trip (str)  - shortest trip
    """


    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    average_time =  df['Trip Duration'].mean()
    longest_trip_duration =  df['Trip Duration'].max()
    fastest_trip_duration =  df['Trip Duration'].min()
    df['trip'] = df['Start Station']  +  '---' + df['End Station']
    longest_trip = df[df['Trip Duration'] == longest_trip_duration].iloc[0]['trip']
    fastest_trip = df[df['Trip Duration'] == fastest_trip_duration].iloc[0]['trip']

    return total_travel_time, average_time, longest_trip_duration, fastest_trip_duration, longest_trip, fastest_trip    


def user_stats(df):
    """Displays statistics on bikeshare users.
    INPUT:
        df - filtered dataframe
    OUTPUTS:
        df_user_type      - dataframe of user types counts
        earliest_usage    - oldest datetime at which the Bikeshare was used
        most_recent_usage - latest datetime at which the Bikeshare was used
        fig               -  an instance of the user types bar chart
    """

    

    # Display counts of user types
    # Get the counts of user types as a dataframe
    df_user_type= df['User Type'].value_counts().to_frame()
    df_user_type.insert(0, 'user_types', df_user_type.index)
    df_user_type= df_user_type.reset_index().drop('index', axis=1)
    df_user_type.rename(columns={'User Type': 'frequency'} , inplace=True)
    
    
    
    # Display the user type Graphically
    
    fig =px.bar(df_user_type, y="frequency", x="user_types", color="user_types", title="The Bikeshare for the User Types ")
    
    # Display earliest, most recent, and most common year of birth
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    earliest_usage = df[df['Start Time'] ==df['Start Time'].min()]
    # Get the specific time
    
    earliest_usage = earliest_usage.iloc[0]['Start Time']
    print('=='*50)
    #mode = df['Birth Year'].mode()
    #  Dataframe containing most recent month
    
    most_recent_usage = df[df['End Time'] ==df['End Time'].max()]
    # Get the cell
    most_recent_usage = most_recent_usage.iloc[0]['End Time']

    return df_user_type, earliest_usage, most_recent_usage, fig
    
    
    
    
    



def time_stats(df):
    """Getting statistics on the most frequent times of travel.
    '\nCalculating The Most Frequent Times of Travel in {}...\n'
    INPUT:
        df - the filtered dataframe above
    OUTPUTS:
    pop_month(int) - Most popular month of Usage
    pop_day_of_week (str)- Most popular day of the week 
    pop_hour (int) - Most popular hour of usage
    count_of_most_popular_month (int) - Number of times of usage in the \
        most popular month

    """


    # Get the most common month

    df = df.copy()
    #  most popular month 
    pop_month = df['month'].mode()[0]
    count_of_most_popular_month = df[df['month'] == pop_month].shape[0]

    pop_day_of_week = df['day_of_week'].mode()[0]
    
    # Get the most common start hour of the day
    pop_hour = df['Start Time'].dt.hour.mode()[0]
    
    return pop_month, pop_day_of_week, pop_hour, count_of_most_popular_month


def station_stats(df, num_stations= 10):
    """Get statistics on the most popular stations and trip.
    INPUTS:
        df - the filtered dataframe above
        num_stations (int) - number of most popular stations to visualize
    OUTPUTS:
        popular_start_station (str) - Most popular start station
        popular_end_station (str) - Most Popular end station
        pop_trip (str)  -      Most popular trip
        df_pop_trip     -  dataframe of num_stations most popular stations
    """
    # Get the most popular station
    popular_start_station = df['Start Station'].mode()[0]
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]

    # Get most frequent combination of start station and end station trip
    # Broadcast the separator between start and end stations
    df['trip'] = df['Start Station'] + "---" + df['End Station']
    pop_trip = df['trip'].mode()[0]
    # Separate trip by start and end stations
    #[start, end] = df['trip'].mode().str.split('---')[0]
    # Define a dataframe for trip statistics
    df_pop_trip = df['trip'].value_counts().to_frame()
    df_pop_trip.insert(0, 'trips', df_pop_trip.index)
    df_pop_trip = df_pop_trip.reset_index()
    df_pop_trip = df_pop_trip.rename(columns = {'trip': 'frequency'})
    
    #df_pop_trip['trip'] = df_pop_trip.drop('index', axis = 1)
    df_pop_trip = df_pop_trip.iloc[: num_stations, :]
    #df_pop_trip.drop('index', axis=1, inplace=True)

    return popular_start_station, popular_end_station, pop_trip, df_pop_trip
   


    


