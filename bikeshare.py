import datetime
import time
import pandas as pd
import numpy as np
CITY_DATA = { 'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv'}
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
    while True:
        city =  input("Select city (Chicago, New York City, Washington): ").lower()
        if city.title() not in ["Chicago", "New York City", "Washington"]:
            print("Try again. Please write the full city name.")
        else:
            break
        
        # get user input for month (all, january, february, ... , june)      
    while True:
        month = input("Enter month (January through June, in letters), or \'All\': ").lower()
        if month.title() not in ["All", "January", "February", "March", "April", "May", "June"]:
            print("Please enter a valid month, or select \'All\'.")
        else:
            break
        
        # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Enter day of week (Sunday through Saturday, in letters), or \'All\': ").lower()
        if day.title() not in  ["All", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
            print("Please enter a valid day of week, or select \'All\'.")
        else:
            break
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
    
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # display the most common month
    df["Month"] = df["Start Time"].dt.month_name()
    common_month = df["Month"].mode()[0]
    print("The most common month is {}.".format(common_month))

    # display the most common day of week
    df["Day"] = df["Start Time"].dt.weekday_name
    common_day = df["Day"].mode()[0]
    print("The most common day of the week is: {}".format(common_day))
    
    # display the most common start hour    
    df["Start Hour"] = df["Start Time"].dt.hour
    common_hour = df["Start Hour"].mode()[0]
    print("The most common start hour is: {}:00".format(common_hour))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    # display most commonly used start station
    start_station = df["Start Station"].mode()[0]
    print("The most common start station is: {}".format(start_station))

    # display most commonly used end station
    end_station = df["End Station"].mode()[0]
    print("The most common end station is: {}".format(end_station))

    # display most frequent combination of start station and end station trip  
    freq_stations = df.groupby(['Start Station','End Station']).size().nlargest(1)
    fs = list(freq_stations.index[0])
    print("The most frequent station combination is:\n    Start Station: {}\n    End Station: {}.\n    Total trips between these stations: {}".format(fs[0], fs[1], freq_stations[0]))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):      
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time 
    total_dur = int(df["Trip Duration"].sum())
    print("The total amount of time travelled is: {} (hh:mm:ss).".format(datetime.timedelta(seconds=total_dur)))
    
    # display mean travel time
    mean_dur = int(df["Trip Duration"].mean())
    print("The mean travel time is: {} (hh:mm:ss).".format(datetime.timedelta(seconds=mean_dur)))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types 
    user_counts = dict(df["User Type"].value_counts())
    print("The counts of user type are:")
    for key, value in user_counts.items():
        print(key, value)

    # Display counts of gender  
    if "Gender" not in df.columns.values:
        print("Gender data: Sorry, no gender data available for this city.")
    else:
        gender_counts = dict(df["Gender"].value_counts())
        print("The gender count is:")
        for key, value in gender_counts.items():
            print(key, value)

    # Display earliest, most recent, and most common year of birth  
    if "Birth Year" not in df.columns.values:
        print("Age data: Sorry, no age data available for this city.")
    else:
        min_bday = df["Birth Year"].min()
        min_bday_counter = sum(1 if x == min_bday else 0 for x in df["Birth Year"])
        print("The earliest year of birth is {}, with {} occurrences.".format(int(min_bday), min_bday_counter))
        old_counter = sum(1 if x <= 1917 else 0 for x in df["Birth Year"])
        print("    * Note: This data contains {} entries of people over age 100, suggesting that the data may not be exact".format(old_counter))
        max_bday = df["Birth Year"].max()
        max_bday_counter = sum(1 if x == max_bday else 0 for x in df["Birth Year"])
        print("The latest year of birth is {}, with {} occurrences.".format(int(max_bday), max_bday_counter))
        common_bday = df["Birth Year"].mode()[0]
        common_bday_counter = sum(1 if x == common_bday else 0 for x in df["Birth Year"] )
        print("The most common year of birth is {}, with {} occurrences.".format(int(common_bday), common_bday_counter))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    ''' this function display 5 rows of data from the csv file for the selected city.'''

    data = 0
    invalid_message =("Invalid entry. Please enter \'yes\' or \'no.\'")
    
    # Display an error message if the entry is incorrect
    while True:
        data_rows = input("Would you like to see 5 lines of raw data? Enter \'yes\' or \'no\': ")
        if data_rows.lower() != ['yes', 'no']:
            print(invalid_message)
        if data_rows.lower() == 'no':
            break
        # Display the first five rows at the request of the user    
        if data_rows.lower() == 'yes':
            data += 5
            print(df.iloc[data : data + 5])
           
            # Display five successive rows at a time at user request
            more_data_rows = input("Would you like to view 5 more lines of data? Enter \'yes\' or \'no\': ")
            if more_data_rows != ['yes', 'no']:
                print(invalid_message)
            if more_data_rows.lower() == 'no':
                break
            if more_data_rows.lower() == 'yes':
                data += 5
                print(df.iloc[data : data + 5])

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
if __name__ == "__main__":
	main()