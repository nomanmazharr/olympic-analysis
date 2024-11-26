def country_year(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = df['region'].dropna().unique().tolist()
    country.sort()
    country.insert(0, 'Overall')
    return years, country


# Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal
def medal(df, year, country):
    medal_df = df.drop_duplicates(['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0

    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == year]
    if year == 'Overall' and country != 'Overall':
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['region'] == country) & (medal_df['Year'] == year)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Bronze', 'Gold', 'Silver']].reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Bronze', 'Gold', 'Silver']].reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    x['total'] = x['total'].astype('int')
    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    return x


def data_over_time(df, col):
    # Drop duplicates and count occurrences of 'Year'
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index()
    # Rename the columns to ensure 'index' is the correct column name
    nations_over_time.columns = ['index', col]  # Explicitly name the first column 'index'
    # Sort the DataFrame by 'index' (the year)
    nations_over_time = nations_over_time.sort_values('index')
    return nations_over_time


def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index()
    x.columns = ['index', 'Medals']  # 'index' is the name of the athlete, 'Medals' is the count
    x = x.head(15).merge(df, left_on='index', right_on='Name', how='left')[['index', 'Medals', 'Sport', 'region']].drop_duplicates('index')
    x.rename(columns={'index': 'Name'}, inplace=True)
    return x



def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df


def country_event_heatmap(df, country):
        temp_df = df.dropna(subset=['Medal'])
        temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
        new_df = temp_df[temp_df['region'] == country]
        pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count')
        return pt


def most_successful_countrywise(df, country):
    # Drop rows with missing Medal values
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    print("Columns in temp_df:", temp_df.columns)
    print("Columns in df:", df.columns)
    name_counts = temp_df['Name'].value_counts().reset_index()
    name_counts.columns = ['Name', 'Medals']  # Rename columns for clarity
    x = name_counts.head(10).merge(temp_df, on='Name', how='left')[['Name', 'Medals', 'Sport']].drop_duplicates('Name')
    return x


def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final