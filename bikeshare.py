# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 18:53:08 2020

@author: SEAY
"""

import time
import pandas as pd
import numpy as np

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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_list = ["chicago", "new york city", "washington"]
    city = input("What city would you like to explore bikeshare data? Please enter chicago, new york city, or washington: ").lower()
    while city not in city_list:
        print("Oops! It looks like the city you selected isn't on our list. Let's try again.")
        city = input("What city would you like to explore bikeshare data? Please enter chicago, new york city, or washington: ").lower()
    
    print("Sounds good! We'll explore bike data in", city.title())

    # TO DO: get user input for month (all, january, february, ... , june)
    month_list = ["all", "january", "february", "march", "april", "may", "june"]
    month = input("What month do you want to analyze? Please enter either all, january, february, march, april, may, june: ").lower()
    while month not in month_list:
        print("Oops! It looks like the month you selected isn't on our list. Let's try again.")
        month = input("What month do you want to analyze? Please enter either all, january, february, march, april, may, june: ").lower()
        
    if month == "all":
        print("Ok, we'll investigate data for all months available.")
    else:
        print("Ok, we'll investigate for the month of", month.title())
    

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day_list = ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    day = input("What day of the week do you want to investigate? Please enter either all, monday, tuesday, wednesday, thursday, friday, saturday, or sunday: ").lower()
    while day not in day_list:
        print("Oops! It looks like the day of week you selected isn't on our list. Let's try again.")
        day = input("What day of the week do you want to investigate? Please enter either all, monday, tuesday, wednesday, thursday, friday, saturday, or sunday: ").lower()
    
    if day == "all":
        print("Ok, we'll investigate data for all days of the week.")
    else:
        print("Ok, we'll investigate data for", day.title())

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

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    
    Input: df = the filtered (based on user inputs) bikeshare dataframe.
    
    Outputs: prints to screen the most common month, day, and hour for bicycling. 
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    df['month'] = pd.DatetimeIndex(df['Start Time']).month
    popular_month = df['month'].mode().values[0]
    month_spelled = ['january', 'february', 'march', 'april', 'may', 'june']
    print("The most popular month for bikesharing:", month_spelled[popular_month-1].title())

    # TO DO: display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.day_name()
    popular_day = df['day_of_week'].mode().values[0]
    print("The most popular day of the week for bikesharing:", popular_day)

    # TO DO: display the most common start hour
    df['hour_of_day'] = df['Start Time'].dt.hour
    popular_hour = df['hour_of_day'].mode().values[0]
    print("The most popular time (hour, military time) of the day for bikesharing:", popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    
    Input: df = the filtered (based on user inputs) bikeshare dataframe.
    
    Outputs: prints to screen start/end station stats.
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode().values[0]
    print("The most popular starting station:", popular_start_station)

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode().values[0]
    print("The most popular ending station:", popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    df['Start Plus End'] = "The most Popular Start/End Station combination was: " + df['Start Station'] + " / " + df['End Station']
    print(df['Start Plus End'].value_counts().index[0])
    print("This Start/End Station combination was used a total of", df['Start Plus End'].value_counts()[0], "times for the city, month(s), day(s) selected.")
    #print(df.groupby(['Start Station', 'End Station'])['Start Station', 'End Station'].count())#.values[0])
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    
    Input: df = the filtered (based on user inputs) bikeshare dataframe.
    
    Outputs: prints to screen the total and average trip duration for the given study period.
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print("The total travel time (minutes) for the city, month(s), day(s) selected was: ", df['Trip Duration'].sum() / 60, "minutes!")

    # TO DO: display mean travel time
    print("The average travel time (minutes) per bike ride for the city, month(s), day(s) selected was: ", df['Trip Duration'].mean() / 60, "minutes!")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users.
    
    Input: df = the filtered (based on user inputs) bikeshare dataframe.
    
    Outputs: prints to screen user characteristics (gender, birth year).
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("The different user types and number of bike ride occurrences for each are listed here:")
    print(df.groupby(['User Type'])['User Type'].count())

    # TO DO: Display counts of gender
    if city != 'washington': # skipping step if Washington was selected, since data doesn't include gender (better solution to this in next if statement)
        print("The different gender types and number of bike ride occurrences for each are listed here:")
        print(df.groupby(['Gender'])['Gender'].count())

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df: # a different (and more efficient way than the count of gender display above to skip over if Washington was selected.
        print("The oldest chap to ride a bike was born in:", df['Birth Year'].min())
        print("The youngest guy/gal to ride a bike was born in:", df['Birth Year'].max())
        print("The most common birth year of bike riders was:", df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def raw_data(df):
    """Displays 5 line blocks of the raw data at the users discretion
    
    Input: df = the filtered (based on user inputs) bikeshare dataframe.
    
    Outputs: chunks (5 rows) of the raw dataframe output to screen until the user says to stop.
    """
    show_me_data = input('Would you like to view some of the raw data (5 lines worth)? Yes or No: ').lower()
    yes_or_no = ["yes", "no"]
    while show_me_data not in yes_or_no:
        print("Oops! That isn't a valid entry. Let's try again.")
        show_me_data = input('Would you like to view some of the raw data (5 lines worth)? Yes or No: ').lower()
        
    lines = 0
    while show_me_data != "no" and lines < (df.shape[0]-5):
        print(df[lines:lines+5])#.head(5))
        lines += 5
        show_me_data = input('Would you like to view 5 more lines? Yes or No: ').lower()
        
        while show_me_data not in yes_or_no:
            print("Oops! That isn't a valid entry. Let's try again.")
            show_me_data = input('Would you like to view some of the raw data (5 lines worth)? Yes or No: ').lower()
    
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

