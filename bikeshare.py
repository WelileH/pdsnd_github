import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
def check_input(word,word_list):
    """
    Checks for input spelling of word from word_list, asks for user to correct until right

    Args:
        (str) word - input to check if acceptable option
        (list) word_list - list of acceptable options to check input against
    Returns:
        (str) word - after spelling check ensured is acceptable option
    
    """
    right_input = True
    word = word.lower()
    word_list = [x.lower() for x in word_list]
    while right_input:
        if word in word_list:
            right_input = False
        else:
            word = input('>> Please check your spelling and try again with {} : \n>> '.format(word_list))
            word = word.lower()
    return word
            
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
    city = input('>> Please input your city option - either "Chicago","New York City" or "Washington": \n>>> ')
    city_list = ["Chicago", "New York City", "Washington"]
    city = check_input(city, city_list)
    # TO DO: get user input for month (all, january, february, ... , june)
    month = input(">> Please enter month (all, january, february, ... , june) to filter to: \n>>> ")
    month_list = ['All', 'January', 'February', 'March', 'April', 'May', 'June']
    month = check_input(month, month_list)
    
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input(">> Please enter the day of week (all, monday, tuesday, ... sunday) to filter to: \n>>> ")
    day_list = ['All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day = check_input(day, day_list)

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
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        month = months.index(month)+1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day)
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # no need to convert the Start Time column  in df to datetime
    #df['Start Time'] = pd.to_datetime(df['Start Time'])

    # TO DO: display the most common month
    # no need for 1. extract month from Start Time column to create a month column as it is already done in load_data()
    # 2. find most common month
    month_freq = df['month'].value_counts()
    popular_month = month_freq[month_freq==month_freq.max()].index[0]
    # 3. conver month integer to string name
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    common_month = months[popular_month-1]
    print("Most Common Month : {}".format(common_month.title()))

    # TO DO: display the most common day of week
    # no need for 1. extract day of week from Start Time column to cread day_of_week column as it is done in load_data()
    # 2. find most common day of week
    day_freq = df['day_of_week'].value_counts()
    popular_day = day_freq[day_freq==day_freq.max()].index[0]
    # 3. convert day integer to string name
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    common_day = days[popular_day-1]
    print("Most Common Day of Week : {}".format(common_day.title()))

    # TO DO: display the most common start hour
    # 1. extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # 2. find the most common hour (from 0 to 23)
    hour_freq = df['hour'].value_counts()
    popular_hour = hour_freq[hour_freq==hour_freq.max()].index[0]
    print("Most common hour of day : {}".format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station_freq = df['Start Station'].value_counts()
    popular_start_station = start_station_freq[start_station_freq==start_station_freq.max()].index[0]
    print("Most Commonly Used Start Station :\n  {}".format(popular_start_station))

    # TO DO: display most commonly used end station
    end_station_freq = df['End Station'].value_counts()
    popular_end_station = end_station_freq[end_station_freq==end_station_freq.max()].index[0]
    print("Most Commonly Used End Station :\n {}".format(popular_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    popular_station_combo = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print("Most Frequent Combination of Start and End Station Trip : \n \t(Start Station \t >=> \t End Station)\n{}".format(popular_station_combo))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total Travel Time in seconds: {:,}s from {:,} trips".format(total_travel_time,len(df['Trip Duration'])))
    print("Total Travel Time equivalently is: {:,}day(s) {:.0f}hr(s), {:.0f}min(s), {:.0f}sec(s)".format(total_travel_time//86400,(total_travel_time//86400)//3600, (total_travel_time%3600)//60, (total_travel_time%3600)%60))

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean Travel Time in seconds : {:,.3f}s from {:,} trips".format(mean_travel_time, len(df['Trip Duration'])))
    print("Mean Travel Time equivalently is: {:.0f}hr(s), {:.0f}min(s), {:.2f}sec(s)".format(mean_travel_time//3600, (mean_travel_time%3600)//60, (mean_travel_time%3600)%60))

    # Prompts user for option to view more comprehensive trip duration stats
    descriptive_view = input("\n>> Would you like to see more stats on Trip Duration? Enter Y=yes or N=no \n>>>")
    descriptive_options = ['y','n']
    descriptive_view = check_input(descriptive_view, descriptive_options)
    if descriptive_view=='y':
        print('Desciptive Statistics of Trip Duration Data (in seconds):\n',round(df['Trip Duration'].describe(),2))
        print()
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of User Types:")
    for i in range(len(user_types)):
        print("{} : {:,}".format(user_types.index[i], user_types[i]))
    print()

    # TO DO: Display counts of gender
    print("Counts of Users Based on Gender: ")
    try:
        gender_counts = df['Gender'].value_counts()
        for i in range(len(gender_counts)):
            print("{} : {:,}".format(gender_counts.index[i], gender_counts[i]))
        print()
        print("Analyzing User Type counts with Gender counts:\n", pd.crosstab(df['Gender'],df['User Type']))
        print()
    except KeyError as e:
        print("KeyError occurred: Sorry, but we cannot do {0} Analysis as we do not have data for {0} in chosen city\n".format(e))

    # TO DO: Display earliest, most recent, and most common year of birth
    print("User Stats based on Birth Year: ")
    try:
        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        most_common_year = df['Birth Year'].mode()[0]
        print("Earliest Year of Birth : {} ".format(int(earliest_year)))
        print("Most Recent Year of Birth : {}".format(int(most_recent_year)))
        print("Most Common Year of Birth : {}".format(int(most_common_year)))
    except KeyError as e:
        print("KeyError occurred: Sorry, but we cannot do {0} Analysis as we do not have data for {0} in chosen city\n".format(e))
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        totalstats = input('\n>> Would you like to see stats unfiltered by month or day for your city? Enter Y=yes or N=no. \n>>> ')
        totalstats_options = ['y', 'n']
        totalstats = check_input(totalstats, totalstats_options)
        if totalstats.lower()=='y':
            df2 = load_data(city, 'all', 'all')
            time_stats(df2)
            station_stats(df2)
            trip_duration_stats(df2)
            user_stats(df2)
        # Give user option to view raw data 5 lines at a time
        raw_data_display = input('\n>> Would you like to view 5 lines of raw data? Enter Y=yes or N=no. \n>>> ')
        display_options = ['y', 'n']
        raw_data_display = check_input(raw_data_display,display_options)
        if raw_data_display.lower()=='y':
            cont_display = True
            i = 0
            while cont_display:
                if city in ['chicago', 'new york city']:
                    print(df.iloc[i:i+5,:9])
                    more_display = input('\n>> Would you like to view next 5 lines of raw data? Enter Y=yes or N=no. \n>>> ')
                    more_display = check_input(more_display, display_options)
                    if more_display.lower()=='n':
                        cont_display = False
                    else:
                        i+=5
                else:
                    print(df.iloc[i:i+5,:7])
                    more_display = input('\n>> Would you like to view next 5 lines of raw data? Enter Y=yes or N=no. \n>>> ')
                    more_display = check_input(more_display, display_options)
                    if more_display.lower()=='n':
                        cont_display = False
                    else:
                        i+=5       
        # Giver user option to view report on missing values in our data set
        missing_value_report = input('\n>> Would you like to view how many missing value in our raw data? Enter Y=yes or N=no. \n>>> ')
        missing_value_report=check_input(missing_value_report, display_options)
        if missing_value_report=='y':
            if city in ['chicago', 'new york city']:
                print('Report of Missing Values in Data per column: \n',df.iloc[:,:9].isnull().sum())
            else:
                print('Report of Missing Values in Data per column: \n',df.iloc[:,:7].isnull().sum())
        # Give user option to restart
        restart = input('\n>> Would you like to restart? Enter Y=yes or N=no.\n>>> ')
        restart_options = ['y', 'n']
        restart=check_input(restart,restart_options)
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
