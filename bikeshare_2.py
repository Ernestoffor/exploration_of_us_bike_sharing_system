import time
import pandas as pd
import numpy as np
from datetime import timedelta
import plotly.express as px
import plotly.graph_objects as go

pd.set_option("display.max_rows", None, "display.max_columns", None)

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Enter the city to filter:     ")
    if city.lower() not in CITY_DATA:
        print("Oops!!! City must be one of ['Chicago', 'New York City', 'Washington'].\n")
        city = input("Enter the city to filter again:     ")
    
    #while city.lower() in CITY_DATA:
    city = city.lower()
    month = input("Enter the month of interest:\n['all', 'january', 'february', 'march', 'april', 'may', 'june']    ")
    day = input("Enter the day of choice one of:\n\
        ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']     ")
        
    # Make the inputs Case agnostic
    month = month.lower()
    day = day.lower()

    print('-'*40)
    return city, month, day


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


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel ...\n')
    start_time = time.time()

    # display the most common month

    df = df.copy()
    pop_mo = df['month'].mode()[0]
    num_of_times_popular_month = df[df['month'] == pop_mo].value_counts().sum()
    
    print("The most popular month is {}".format(pop_mo))
    
    print('='*90)
    print("The bikeshare was used {} times in the month of {}".format(num_of_times_popular_month, pop_mo))
    # display the most common day of week
    pop_day_of_week = df['day_of_week'].mode()[0]
    print("The most popular day of the week is {}".format(pop_day_of_week))
    print('='*90)
    # display the most common start hour
    pop_hour = df['Start Time'].dt.hour.mode()[0]

    print("The most popular start hour is {}".format(pop_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('='*90)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip ...\n')
    start_time = time.time()

    # display most commonly used start station

    popular_start_station = df['Start Station'].mode()[0]
    print('='*50)
    print("The most popular start station in the city for US Bikeshare is {}".format( popular_start_station))
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('='*50)
    print("The most popular end station in the city is \n {}".format( popular_end_station))


    # display most frequent combination of start station and end station trip
    # Broadcast the separator between 
    df['trip'] = df['Start Station'] + "---" + df['End Station']
    pop_trip = df['trip'].mode()
    
    # Get the start and end of the most popular trip

    [start, end] = df['trip'].mode().str.split('---')[0]
    print('='*90)
    print('The most popular trip is {}'.format(pop_trip))
    print('='*90)
    print('The most popular trip is one that starts at\n {} station and ends at {} station'.format(start, end))
    print('='*90)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('='*90)


    




def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
        INPUT:
            df - the filtered dataframe
    """
    start_time = time.time()
    print('\nCalculating Trip Duration in ...\n')
    

    # display total travel time
    print('=='*50)
    
    total_travel_time = df['Trip Duration'].sum()
    print("The total time for the usage of the Bikeshare in the city is  \n {} {}".format(total_travel_time, 'seconds'))
    # display mean travel time
    print('=='*50)
    average_time = round(df['Trip Duration'].mean(), 2)
    #average_time_in_seconds = df['trip_duration'].mean().total_seconds()
    print("The average usage of the Bikeshare in the city is \n {}".format(average_time))
    print('=='*50)
    print("The average usage of the Bikeshare is \n {} seconds".format(average_time))
    print('=='*50)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('=='*50)

def user_stats(df, city):
    """Displays statistics on bikeshare users.
        INPUT:
            df - filtered dataframe
            city - The city to explore Bikeshare usage
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    # Get the counts of user types as a dataframe
    df_user_type= df['User Type'].value_counts().to_frame()
    df_user_type.insert(0, 'users_type', df_user_type.index)
    df_user_type= df_user_type.reset_index().drop('index', axis=1)
    df_user_type.rename(columns={'User Type': 'frequency'} , inplace=True)
    print("The Bikeshare User Types are shown below:\n {}".format(df_user_type))
    
    print('=='*50)
    
    # Display the user type Graphically
    fig = px.pie(df_user_type, values='frequency', names='users_type', title = "The Bikesare User Types")
    fig.show()
    
    
    
    print('=='*50)

    # Display earliest, most recent, and most common year of birth
    earliest_usage = df[df['Start Time'] ==df['Start Time'].min()]
    # Get the specific time
    
    earliest_usage = earliest_usage.iloc[0]['Start Time']
    print('=='*50)
    #mode = df['Birth Year'].mode()
    #  Dataframe containing most recent month
    
    most_recent_usage = df[df['End Time'] ==df['End Time'].max()]
    # Get the cell
    most_recent_usage = most_recent_usage.iloc[0]['End Time']
    print('The earliest usage of the bike was on \n {}'.format(earliest_usage))

    print('The most recent usage of the bike was on \n {}'.format(most_recent_usage))

    print('=='*50)

    if city.lower() != "washington":
        gender= df['Gender'].value_counts().to_frame()
        gender.insert(0, 'Sex', gender.index)
        gender= gender.reset_index().drop('index', axis=1)
        gender.rename(columns={'Gender': 'frequency'} , inplace=True)
    
        print("The Gender Spread of the Users is as follows:\n {}".format(gender))
    
        # Display the user gender Graphically
        fig1 = px.pie(gender, values='frequency', names='Sex', title = "The Bikesare Users By Gender")
        fig1.show()
    
        most_users_by_yob = df[df['Birth Year'] == df['Birth Year'].mode()[0]] # ['Birth Year'][:1]
        most_users_by_yob = most_users_by_yob.iloc[0]['Birth Year']
        num_of_most_users_by_yob = df[df['Birth Year'] == df['Birth Year'].mode()[0]].shape[0]
        print('The most common users of the bikeshare by year of birth are \
    those born in {} with total number of {} times usage'.format(most_users_by_yob, num_of_most_users_by_yob))

        print('=='*50)
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('=='*50)





def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
