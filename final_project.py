import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import math

# Funtcion to read the volcano dataset
def load_data():
    return pd.read_csv('C:/Users/WALSH_COLI/Documents/volcanoes(1).csv')
# Volcano dataframe
df = load_data()
# Removes link column from dataframe because it is unnecessary
df.drop(columns = "Link", inplace = True)
# Title for the streamlit page
st.title("Volcanoes: By Colin Walsh")
# Header for the volcano map
st.subheader("Volcano Map")
# Creating a new dataframe with only columns relevant to creating the volcano map and charts
df1 = df[["Volcano Name", "Latitude", "Longitude", "Country", "Last Known Eruption"]]
# Renaming Longitude and Latitude columns so that it is accepted by streamlit's map function
df1.rename(columns = {"Latitude":"latitude","Longitude":"longitude"}, inplace = True)
# List with a blank item for a list of countries
# The list of countries will appended to the list
# There is a blank value in the list as a default wherein no countries have selected so that all countries are included until one is selected
countryList = [""]
# For loop to populate the country list with unique countries from the volcano dataset
for i in range(len(df1)):
    if df1.at[i, "Country"] not in countryList:
        countryList.append(df1.at[i, "Country"])
# Sorts country list alphabetically
countryList.sort()
# Creates a widget on the side bar that is a drop down menu of all the countries to select from
country = st.sidebar.selectbox("Country", countryList)
# For loop convert strings in last known eruption column into integers
# Suffixes are removed and BCE years will become negative
# Unknown years will be set to the earliest year
# Unknown years are set to a placeholder of -10000 because it needs to be an integer that is not the minimum value and a last known erupted year
for i in range(len(df1)):
    if "BCE" in df1.at[i, "Last Known Eruption"]:
        df1.at[i, "Last Known Eruption"] = df1.at[i, "Last Known Eruption"].replace(" BCE", "")
        df1.at[i, "Last Known Eruption"] = int(df1.at[i, "Last Known Eruption"])
        df1.at[i, "Last Known Eruption"] = df1.at[i, "Last Known Eruption"] * -1
    elif "CE" in df1.at[i, "Last Known Eruption"]:
        df1.at[i, "Last Known Eruption"] = df1.at[i, "Last Known Eruption"].replace(" CE", "")
        df1.at[i, "Last Known Eruption"] = int(df1.at[i, "Last Known Eruption"])
    elif "Unknown" in df1.at[i, "Last Known Eruption"]:
        df1.at[i, "Last Known Eruption"] = df1.at[i, "Last Known Eruption"].replace("Unknown", "-10000")
        df1.at[i, "Last Known Eruption"] = int(df1.at[i, "Last Known Eruption"])
# Determines the earliest known eruption
earliestEruption = df1["Last Known Eruption"].min()
# Determines the most recent eruption
lastestEruption = df1["Last Known Eruption"].max()
# For loop to convert the unknown eruptions to the earliest known eruptions
for i in range(len(df1)):
    if df1.at[i, "Last Known Eruption"] == -10000:
        df1.at[i, "Last Known Eruption"] = earliestEruption
# Creates a widget on the sidebar that is a slider for the range of years for the volcanoes last known eruptions
year_filter = st.sidebar.slider("Eruption Year Range", earliestEruption, lastestEruption, earliestEruption)
# Creates a new dataframe filtered by year range selected in the slider
filtered_data = df1[df1["Last Known Eruption"] >= year_filter]
# If statement that filters the countries
# If no country is selected the map shows volcanoes from all countries
if country == "":
    filtered_data1 = filtered_data
# Creates a new dataframe filtered by the selected country
else:
    filtered_data1 = filtered_data[filtered_data["Country"] == country]
# Maps the volcanoes based on the filtered data
st.map(filtered_data1)
# Header for the barplot of eruptions per country
st.subheader("Eruptions Per Country")
# Empty dictionary for the count of volcanoes in a country
volcano_count = {}
# List of every country in the volcano data which is filtered by the last known eruption
country_list = list(filtered_data["Country"])
# For loop to populate the volcano count dictionary with the country list and the count of each country
for i in range(len(country_list)):
    volcano_count[country_list[i]] = country_list.count(country_list[i])
# Sorts the dictionary by largest value, or the highest count of volcanoes
sorted_volcano_count = dict(sorted(volcano_count.items(), key=lambda x: x[1], reverse=True))
labels = list(sorted_volcano_count.keys())   # List of Countries
count = list(sorted_volcano_count.values())   # List of how many volcanoes are in each country for the specified time period
# Sets the style of the chart to a white grid
sns.set_theme(style = "whitegrid")
# Plots a bar chart of 20 countries with the most volcanoes
sns.barplot(labels[0:20], count[0:20], color = "red")
# Rotates labels 90 degrees to make them legible
plt.xticks(rotation = 90)
plt.xlabel('Country')
plt.ylabel('Eruptions')
# Code to avoid a warning showing up in streamlit
st.set_option('deprecation.showPyplotGlobalUse', False)
# Plots the chart in streamlit
st.pyplot()
# Sidebar widget that has a number input for latitude being in the range of -90 to 90 with four decimal places
latitude = st.sidebar.number_input("Latitude", -90.0, 90.0, step = 1., format = "%.4f")
# Sidebar widget that has a number input for longitude being in the range of -180 to 180 with four decimal places
longitude = st.sidebar.number_input("Longitude", -180.0, 180.0, step = 1., format = "%.4f")
# Function to calculate the distance between two sets of coordinates
def distance_calculator(df1):
    # Link to coordinate to miles multiplier https://www.usgs.gov/faqs/how-much-distance-does-a-degree-minute-and-second-cover-your-maps?qt-news_science_products=0#qt-news_science_products
    # Multiplier - One latitudinal degree is 69 miles
    latitudeToMiles = 69
    # Multiplier - One longitudinal degree is 54.6 miles
    longitudeToMiles = 54.6
    # Empty list to be filled with the distance from the entered coordinates
    distanceList = []

    # For loop to calculate the distance from the volcano to the inputted coordinates and adding it to a list
    for i in range(len(df1)):
        distance = math.sqrt((((df1.at[i, "latitude"] - latitude) * latitudeToMiles)) ** 2
                    + (((df1.at[i, "longitude"] - longitude) * longitudeToMiles)) ** 2)
        distanceList.append(distance)
    return distanceList
# Creates a new dataframe by adding the distance list to the volcano dataframe
df2 = df1.assign(Distance = distance_calculator(df1))
# Sorts the rows in the dataframe by distance so that the closest volcanoes are at the top
df2 = df2.sort_values("Distance")
# Returns the ten closest volcanoes
filtered_data2 = df2[df2["Last Known Eruption"] >= year_filter]
# Header for the nearest volcano dataframe
st.subheader("Nearest Volcanoes")
# Displays the ten closest volcanoes to the selected coordinates
st.dataframe(filtered_data2.head(10))
# Header for the distance and last known eruption scatter plot
st.subheader("Distance and Last Known Eruption")
# Sets the style of the grid to dark
sns.set_style("darkgrid")
# Creates a scatter plot of the distance and last known eruption for the ten closest volcanoes
sns.scatterplot(data = filtered_data2.head(10), x = "Last Known Eruption", y = "Distance", marker = '^', color = "red")
plt.xlabel("Last Known Eruption Year")
plt.ylabel("Distance (Miles)")
st.pyplot()


