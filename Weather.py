
from tkinter import *
from tkinter import messagebox
from configparser import ConfigParser
import requests


# basic url and code I learnt from: https://www.youtube.com/watch?v=7JoMTQgdxg0&ab_channel=teachmesome
# urlfr has "&lang=fr" to change to API to collect the information in french
url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&lang=en'
urlfr = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&lang=fr' #mycode

# a file to retrieve the API and code I learnt from: https://www.youtube.com/watch?v=7JoMTQgdxg0&ab_channel=teachmesome
# the weather API is from: https://openweathermap.org/api
config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']

# this definition of get_weather(city) allows me to pick up the information from the api which I learnt from:
# I learnt from: https://www.youtube.com/watch?v=7JoMTQgdxg0&ab_channel=teachmesome
# the additional functions and information that I retrieved from what I learnt in the video
# were description, timezone, adjusted_timezone to add my own new found knowledge




def get_weather(city):
    result = requests.get(url.format(city, api_key))
    if result:
        json = result.json()
        # (City, Country, temp_celsius, temp_fahrenheit, icon, weather, description, adjusted_timezone)
        city = json['name']
        country = json['sys']['country']
        temp_kelvin = json['main']['temp']
        temp_celsius = temp_kelvin - 273.15
        temp_fahrenheit = (temp_kelvin - 273.15) * 9 / 5 + 32
        weather = json['weather'][0]['main']
        description = json['weather'][0]['description'] #mycode
        timezone = json['timezone'] #mycode
        adjusted_timezone = timezone / 3600 #mycode
        final = (city, country, temp_celsius, temp_fahrenheit, weather, description, adjusted_timezone)
        return final        
    else:
        return None

# picks up the information from the api in french
# only change is in line 50 from line 29
def get_weather_fr(city):
    result = requests.get(urlfr.format(city, api_key))
    if result:
        json = result.json()
        # (City, Country, temp_celsius, temp_fahrenheit, icon, weather, description, adjusted_timezone)
        city = json['name']
        country = json['sys']['country']
        temp_kelvin = json['main']['temp']
        temp_celsius = temp_kelvin - 273.15
        temp_fahrenheit = (temp_kelvin - 273.15) * 9 / 5 + 32
        weather = json['weather'][0]['main']
        description = json['weather'][0]['description'] #mycode
        timezone = json['timezone'] #mycode
        adjusted_timezone = timezone / 3600 #mycode
        final = (city, country, temp_celsius, temp_fahrenheit, weather, description, adjusted_timezone)
        return final        
    else:
        return None

# this search function allows to use the definition from get_weather(city) and retrieve the api information
# to display on the gui
# the extra spaces allows in location_lbl and description_lbl replace the background with white background
# example: if you were to look up "Vancouver" then "Hanoi", Hanoi will just overlap Vancouver and you would be able
# example: to see part of Vancouver behind Hanoi without the spaces "Va-Hanoi-er"
# therefore the spaces fixes this issue
# \u2103 is for degree celsius and \u2109 is for degree fahrenheit, which are universal codes that I found on
# https://en.wikipedia.org/wiki/Degree_symbol
# if the city cannot be found, it will pop up a error message
# example: if you were to type "asdf32452gad" it will not be able to find this city or town or country as it is
# not a valid option
# most of the code is from: https://www.youtube.com/watch?v=7JoMTQgdxg0&ab_channel=teachmesome
# the code unique (my code) from below is the added space to solve issue described above and
# timezone_lbl to display the timezone in UTC with the offset in hours
# the code is repeated in line 94 except it is search_fr and the function get_weather_fr picks up the urlfr instead of url


def search():
    city = city_text.get()
    weather = get_weather(city)
    if weather:
        location_lbl['text'] = '               {}, {}               '.format(weather[0], weather[1])
        temp_lbl['text'] = '{:.2f}\u2103, {:.2f}\u2109'.format(weather[2], weather[3])
        weather_lbl['text'] = weather[4]
        description_lbl['text'] = '     Description: {}        '.format(weather[5])
        timezone_lbl['text'] = 'Universal time zone offset by {} hours'.format(weather[6], weather [6])
    else:
        messagebox.showerror('Error', 'Cannot find city {}'.format(city))

def search_fr():
    city = city_text.get()
    weather = get_weather_fr(city)
    if weather:
        location_lbl['text'] = '               {}, {}               '.format(weather[0], weather[1])
        temp_lbl['text'] = '{:.2f}\u2103, {:.2f}\u2109'.format(weather[2], weather[3])
        weather_lbl['text'] = weather[4]
        description_lbl['text'] = '     Descriptif: {}        '.format(weather[5])
        timezone_lbl['text'] = 'Décalage du fuseau horaire universel de {} heures'.format(weather[6])
    else:
        messagebox.showerror('Error', 'Cannot find city {}'.format(city))


#this code is from: https://www.youtube.com/watch?v=7JoMTQgdxg0&ab_channel=teachmesome
# I learnt this from a previous group project, Rock Paper Scissors as well
#This is designed to make a GUI from tkinter
# app = Tk() allows to create a window
# app.title allows you to name the window
# app.geometry allows you to customize the window size where the first number '450' is the width,
# and the number '200' is the height and the 'x' is required to separate the numbers and is conventional
# app.configure(bg='white') allows you to customize the colour of the background otherwise its this dull grey colour


app = Tk()
app.title("Weather")
app.geometry('450x200')
app.configure(bg='white')

#this allows you to type a string in the search function which is define above in def Search():
city_text = StringVar()
city_entry = Entry(app, textvariable=city_text)
# to place it on the window screen *insert name*.pack()
# where name is the defined string
city_entry.pack()

# search button which allows you to enter the string for the lines 96-101 above
search_btn = Button(app, text='Search', width=12, command=search, bg='white')
search_btn.pack()

# the search button but in french
search_btn_fr = Button(app, text=' Cherche', width=12, command=search_fr, bg='white')
search_btn_fr.pack()

# location and country
location_lbl = Label(app, text='', font=('bold', 20), bg='white')
location_lbl.pack()

# image

temp_lbl = Label(app, text='', bg='white')
temp_lbl.pack()

weather_lbl = Label(app, text='', bg='white')
weather_lbl.pack()

description_lbl = Label(app, text='', bg='white')
description_lbl.pack()

timezone_lbl = Label(app, text='', bg='white')
timezone_lbl.pack()

french_description = Label (app, text='', bg='white')
french_description.pack()

#this allows the window to loop in this certain window and close it off
#this is essential for the GUI
app.mainloop()
