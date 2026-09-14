import requests, logging

logging.basicConfig(
    filename='weather.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def search_city(name):
    try:
        response = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={name}")
        response.raise_for_status()
        data = response.json()
        results = data.get("results", []) #returns empty list if data not found to avoid crash
        
        if not results:
            print(f"{name} not found.")
            return
        
        for i, place in enumerate(results):
            print(f"{i + 1}. {place["name"]} | {place.get("admin2", "(Area not found)")}, {place.get("admin1", "(Area not found)")}, {place.get("country", "(Country not found)")}")
            
        return results   
    except requests.exceptions.RequestException as e:
        msg = f"Failed to fetch data: {e}"
        print(msg)
        logging.error(msg)
        raise SystemExit(e)   
       
    
    
def get_weather(lat, long): #we have 2 separate api calls as the geocoding api does not have weather info
    try:
        response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&daily=temperature_2m_max,temperature_2m_min,weather_code&hourly=temperature_2m&timezone=auto")    
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        msg = f"Failed to fetch data: {e}"
        print(msg)
        logging.error(msg)
        raise SystemExit(e)      
    
def display(data): 
    temp = data["hourly"]["temperature_2m"]
    temp_avg = sum(temp)/len(temp)
    timezone = data["timezone"]    
    print(f"Average temperature: {temp_avg:.1f} | Timezone: {timezone}")

        
def warmest_coldest(data):
    daily = data["daily"]
    dates = daily["time"]
    highs = daily["temperature_2m_max"]
    lows = daily["temperature_2m_min"]
    
    highest_temp = None
    lowest_temp = None
    
    for date, temp in zip(dates, highs): #zipping the dates and temps together to compare them against each other to get warmest/coldest
        if highest_temp is None or temp > highest_temp:
            highest_temp = temp
            highest_date = date 
    
    for date, temp in zip(dates, lows):
        if lowest_temp is None or temp < lowest_temp:
            lowest_temp = temp
            lowest_date = date
            
    print(f"Warmest day: {highest_date}, Temp: {highest_temp} | Coldest day: {lowest_date}, Temp: {lowest_temp}")             
        
def rainy_days(data):
    daily = data["daily"]
    codes = daily["weather_code"]
    dates = daily["time"]
    
    rain_codes = {51, 53, 55, 61, 63, 65, 80, 81, 82} #the api uses numerical codes for different types of weather
    
    rainy_list = []
    
    for code, date in zip(codes, dates):
        if code in rain_codes:
            rainy_list.append(date)
    
    if len(rainy_list) > 0:         
        print("Rainy days: ")
        for date in rainy_list:
            print(f"{date}")
        print(f"{len(rainy_list)} rainy days in the next week.") 
        if len(rainy_list) > 4:
            print("Wow, your city is very rainy.")     
    else:
        print("No rainy days in the last week.")    
        
def sunny_days(data):
    daily = data["daily"] 
    codes = daily["weather_code"]
    dates = daily["time"]

    sun_codes = {0, 1, 2}        

    sunny_list = []

    for code, date in zip(codes, dates):
        if code in sun_codes:
            sunny_list.append(date)
        
    if len(sunny_list) > 0:
        print("Sunny days: ")
        for date in sunny_list:
            print(f"{date}")
        print(f"{len(sunny_list)} sunny days in the next week.")
    else: 
        print("No sunny days in the next week.")    
        
           

        

def menu():
    while True: 
        name = input("Enter city name to start: ")
        results = search_city(name)
        while not results:
            name = input("Enter a valid city name: ")
            results = search_city(name)
        
        choice = input("Enter city number from list: ")
        
        while not choice.isdigit() or int(choice) < 1 or int(choice) > len(results):
            choice = input("Enter city number from list: ")
        
        choice = int(choice)
        selected = results[choice - 1] #minus one to account for the enumerated display starting at 1 instead of 0
        lat = selected["latitude"]
        long = selected["longitude"]
        
        my_city = get_weather(lat, long)

        new_city = False
        logging.info(f"City: {selected["name"]} | Temp: {sum(my_city["hourly"]["temperature_2m"])/len(my_city["hourly"]["temperature_2m"]):.2f}")
        while True:
            choice = input(f"1. Display city details \n 2. Warmest/coldest day \n 3. Rainy days \n 4. Sunny days \n 5. New city \n 6. Quit | Enter option: ")
            
            while not choice.isdigit() or int(choice) not in (1, 2, 3, 4, 5, 6):
                choice = input("Enter a valid option from the menu: ")
                
            choice = int(choice) 
            
            if choice == 1:
                display(my_city)
            elif choice == 2:
                warmest_coldest(my_city)  
            elif choice == 3:
                rainy_days(my_city) 
            elif choice == 4:
                sunny_days(my_city)    
            elif choice == 5:
                new_city = True
                break
            elif choice == 6:
                print("Goodbye!")
                return
            
        if not new_city:
            break

                
menu()            
            
               