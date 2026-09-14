# Project Name
Console Based Weather App

## Description
A console based Python weather app with a menu, created using Open-Meteo's weather and geocoding APIs. Built to experiment with APIs, logging and various functions.

## Features
-Menu with multiple options
- Logging with date/time and success/error messages
- Search cities 
- Display city data
- Display warmest and coldest days in the upcoming week
- Display rainy/sunny days in the upcoming week (with count)

## How It Works
The search_city() function takes the user's city name input and calls the geocoding API which provides the latitude and longitude values. The get_weather() function then takes the lat/long values from the previous function to fetch the data from the weather API. The menu allows the user to choose from a variety of functions to display information about the chosen city's weather. Each city search is logged with city information and date/time. 

## Installation

```bash
git clone https://github.com/fblakesley/weather-app.git
cd weather-app
pip install -r requirements.txt

```

## Usage

```bash
python weather.py

```
Follow the prompts to search for a city, then choose from the menu to view weather details.

## Example

Enter city name to start: glasgow
1. Glasgow | Glasgow City, Scotland, United Kingdom
2. Glasgow | Barren, Kentucky, United States
3. Glasgow | Valley, Montana, United States
4. Glasgow | Rockbridge, Virginia, United States
5. Glasgow | Howard, Missouri, United States
6. Glasgow | Kanawha County, West Virginia, United States
7. Glasco | Cloud County, Kansas, United States
8. Glasgow | Cambria County, Pennsylvania, United States
9. Glasgow | New Castle County, Delaware, United States
10. Glasgow | (Area not found), Nickerie District, Suriname
Enter city number from list: 1
1. Display city details 
 2. Warmest/coldest day 
 3. Rainy days 
 4. Sunny days 
 5. New city 
 6. Quit | Enter option: 1
Average temperature: 13.9 | Timezone: Europe/London

## Technologies Used
Python, requests, logging

## Future Improvements
I may experiment with a web based version and/or adding more weather stats options.

## Author
F Blakesley
