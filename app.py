import streamlit as st
import pandas as pd
import preprocess
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("athlete_events.csv")
region_df = pd.read_csv("noc_regions.csv")

st.sidebar.header("Olympics Analysis")
df = preprocess.preprocess(df, region_df)
user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal_Tally', 'Overall_Analysis',
     'Country-wise_Analysis', 'Athlete Wise Analysis')
)


if user_menu == "Medal_Tally":
    st.sidebar.header("Medal Tally")
    years, countries = helper.countries_year_list(df)
    selected_year = st.sidebar.selectbox("Select year", years)
    selected_country = st.sidebar.selectbox("Select country", countries)
    medal_tally = helper.get_medal_tally(df, selected_year, selected_country)
    if selected_year == "Overall" and selected_country == "Overall":
        st.title("Overall Tally")
    if selected_year == "Overall" and selected_country != "Overall":
        st.title("Overall performance of " + selected_country)
    if selected_year != "Overall" and selected_country == "Overall":
        st.title("Overall performance in " + str(selected_year))
    if selected_year != "Overall" and selected_country != "Overall":
        st.title("Overall performance of " +
                 selected_country + " in " + str(selected_year))
    st.table(medal_tally)


if user_menu == "Overall_Analysis":
    editions = df["Year"].unique().shape[0] - 1
    cities = df["City"].unique().shape[0]
    sports = df["Sport"].unique().shape[0]
    events = df["Event"].unique().shape[0]
    athletes = df["Name"].unique().shape[0]
    nations = df["region"].unique().shape[0]
    st.title("Top Stats")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Cities")
        st.title(cities)
    with col3:
        st.header("Events")
        st.title(events)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Athletes Participated")
        st.title(athletes)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Sports")
        st.title(sports)
    nations_overtime = helper.data_overtime(df, "region")
    nations_overtime = nations_overtime.rename(
        columns={"index": "Year", "Year": "Number_of_countries"})
    fig1 = px.line(nations_overtime, x="Year", y="Number_of_countries")
    st.title("Participating nations over the years")
    st.plotly_chart(fig1)

    events_overtime = helper.data_overtime(df, "Event")
    events_overtime = events_overtime.rename(
        columns={"index": "Editions", "Year": "Number_of_events"})
    fig2 = px.line(events_overtime, x="Editions", y="Number_of_events")
    st.title("Events conducted over the years")
    st.plotly_chart(fig2)

    st.title("No.of.Events.Overtime")
    fig, ax = plt.subplots(figsize=(25, 25))
    x = df.drop_duplicates(["Year", "Sport", "Event"])
    ax = sns.heatmap(x.pivot_table(index="Sport", columns="Year",
                     values="Event", aggfunc="count").fillna(0).astype(int), annot=True)
    st.pyplot(fig)

    st.title("Most successful Athletes")
    sport_list = df["Sport"].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, "Overall")
    sport_name = st.selectbox("Select a sport", sport_list)
    x = helper.most_sucessful(df, sport_name)
    st.table(x)

if user_menu == "Country-wise_Analysis":
    country_list = df["region"].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.selectbox("Select a country", country_list)
    country_df = helper.year_wise_medal_tally(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title("Medal tally Over the years of " + selected_country)
    st.plotly_chart(fig)

    st.title(selected_country + " Excels in the following sports")
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    top_10df = helper.most_sucessful_countrywise(df, selected_country)
    st.title("Top 15 athletes of " + selected_country)
    st.table(top_10df)
