def medal_tally(df):
    medal_tally = df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    medal_tally = medal_tally.groupby('region').sum(
    )[["Gold", "Silver", "Bronze"]].sort_values("Gold", ascending=False)

    medal_tally["total"] = medal_tally["Gold"] + \
        medal_tally["Silver"] + medal_tally["Bronze"]

    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['total'] = medal_tally['total'].astype('int')

    return medal_tally


def countries_year_list(df):
    years = df["Year"].unique().tolist()
    years.sort()
    years.insert(0, "Overall")
    countries = df["region"].dropna()
    countries = countries.unique()
    countries = countries.tolist()
    countries.sort()
    countries.insert(0, "Overall")

    return years, countries


def get_medal_tally(df, year, country):
    flag = 0
    medal_df = df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    if year == "Overall" and country == "Overall":
        temp_df = medal_df
    if year == "Overall" and country != "Overall":
        flag = 1
        temp_df = medal_df[medal_df["region"] == country]
    if year != "Overall" and country == "Overall":
        temp_df = medal_df[medal_df["Year"] == int(year)]
    if year != "Overall" and country != "Overall":
        temp_df = medal_df[(medal_df["region"] == country)
                           & (medal_df["Year"] == int(year))]
    if flag == 1:
        x = temp_df.groupby('Year').sum()[
            ["Gold", "Silver", "Bronze"]].sort_values("Year").reset_index()
    else:
        x = temp_df.groupby('region').sum()[["Gold", "Silver", "Bronze"]].sort_values(
            "Gold", ascending=False).reset_index()
    x["total"] = x["Gold"] + x["Silver"] + x["Bronze"]
    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x


def data_overtime(df, col):

    overtime_data = df.drop_duplicates(
        ["Year", col])["Year"].value_counts().reset_index().sort_values("index")
    return overtime_data


def most_sucessful(df, sport):
    temp_df = df.dropna(subset=["Medal"])

    if sport != "Overall":
        temp_df = temp_df[temp_df["Sport"] == sport]
    x = temp_df['Name'].value_counts().reset_index().merge(df, left_on="index", right_on="Name", how="left")[
        ["index", "Name_x", "Sport", "region"]].drop_duplicates()
    x.rename(columns={"index": "Athlete Name",
             "Name_x": "Medals"}, inplace=True)
    return x


def year_wise_medal_tally(df, country):
    temp_df = df.dropna(subset=["Medal"])
    temp_df = temp_df.drop_duplicates(
        subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"])
    new_df = temp_df[temp_df["region"] == country]
    final_df = new_df.groupby("Year").count()['Medal'].reset_index()
    return final_df


def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=["Medal"])
    temp_df = temp_df.drop_duplicates(
        subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"])
    new_df = temp_df[temp_df["region"] == country]
    pt = new_df.pivot_table(index="Sport", columns="Year",
                            values="Medal", aggfunc="count").fillna(0)
    return pt


def most_sucessful_countrywise(df, country):
    temp_df = df.dropna(subset=["Medal"])

    temp_df = temp_df[temp_df["region"] == country]
    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on="index", right_on="Name", how="left")[
        ["index", "Name_x", "Sport"]].drop_duplicates("index")
    x.rename(columns={"index": "Athlete Name",
             "Name_x": "Medals"}, inplace=True)
    return x
