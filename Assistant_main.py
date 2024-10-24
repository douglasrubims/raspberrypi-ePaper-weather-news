# -*- coding:utf-8 -*-

from PIL import Image, ImageDraw
from weather import *
from news import *
from display import *
import json
from dotenv import load_dotenv
import os
import time
import threading

load_dotenv()

debug = int(os.getenv("DEBUG"))
api_key_weather = os.getenv("WEATHER_API_KEY")
api_key_news = os.getenv("NEWS_API_KEY")
lat = os.getenv("LOCATION_LATITUDE")
lon = os.getenv("LOCATION_LONGITUDE")

if debug == 0:
    from epd7in5b_V2 import EPD
else:
    pass

# Semaphore to control access to display updates
display_semaphore = threading.Semaphore(1)

def map_resize(val, in_mini, in_maxi, out_mini, out_maxi):
    if in_maxi - in_mini != 0:
        out_temp = (val - in_mini) * (out_maxi - out_mini) // (in_maxi - in_mini) + out_mini
    else:
        out_temp = out_mini
    return out_temp

def update_time():
    if debug == 0:
        epd2 = EPD()

    while True:
        current_time = time.strftime("%H:%M", time.localtime()) + "H"
        print(f"Updating current time to: {current_time}")  # Log the current time update
        print("Drawing current time on display")  # Log display update
        # display.draw_partial.text((400 - font24.getsize(current_time)[0] // 2, 400), current_time, fill=0, font=font24)
        display.draw_partial.text((100, 100), current_time, fill=0, font=font24)
        if debug == 0:
            epd2.init()
            print("Drawing current time on display partial")  # Log display update
            # Xstart = 400 - font24.getsize(current_time)[0] // 2
            # Ystart = 400
            # Xend = 400 - font24.getsize(current_time)[0] // 2 + font24.getsize(current_time)[0]
            # Yend = 400 + font24.getsize(current_time)[1]
            Xstart = 100
            Ystart = 100
            Xend = 800
            Yend = 480
            print(f"Inserting current time on display partial at ({Xstart}, {Ystart}) to ({Xend}, {Yend})")  # Log display update
            with display_semaphore:  # Acquire semaphore before updating display
                epd2.display_Partial(epd2.getbuffer(display.im_partial), Xstart, Ystart, Xend, Yend)  # Update display with the time
                epd2.sleep()
            print("Display updated with current time")  # Log display update
            display.clear("partial")
        else:
            display.im_partial.show()
            print("Display shown in debug mode")  # Log debug display show
        time.sleep(60)  # Sleep for 1 minute before updating the time

def main():
    ##################################################################################################################
    # FRAME
    display.draw_black.rectangle((5, 5, 795, 475), fill=255, outline=0, width=2)  # INNER FRAME
    display.draw_black.line((350, 5, 350, 290), fill=0, width=1)  # VERTICAL SEPARATION slim
    display.draw_black.line((5, 290, 795, 290), fill=0, width=1)  # HORIZONTAL SEPARATION

    # UPDATED AT
    display.draw_black.text((10, 8), "Atualizado em " + weather.current_time(), fill=0, font=font10)

    ###################################################################################################################
    # CURRENT WEATHER
    display.draw_icon(20, 35, "r", 75, 75,
                      weather.weather_description(weather.current_weather())[0])  # CURRENT WEATHER ICON
    display.draw_black.text((120, 15), weather.current_temp(), fill=0, font=font48)  # CURRENT TEMP
    display.draw_black.text((230, 15), weather.current_hum(), fill=0, font=font48)  # CURRENT HUM
    display.draw_black.text((245, 65), "Humidade", fill=0, font=font12)  # LABEL "HUMIDITY"
    display.draw_black.text((120, 75), weather.current_wind()[0] + " " + weather.current_wind()[1], fill=0, font=font24)

    display.draw_icon(120, 105, "b", 35, 35, "sunrise")  # SUNRISE ICON
    display.draw_black.text((160, 110), weather.current_sunrise(), fill=0, font=font16)  # SUNRISE TIME
    display.draw_icon(220, 105, "b", 35, 35, "sunset")  # SUNSET ICON
    display.draw_black.text((260, 110), weather.current_sunset(), fill=0, font=font16)  # SUNSET TIME

    ###################################################################################################################
    # HOURLY FORECAST
    display.draw_black.text((30, 140), "+3h", fill=0, font=font16)  # +3h LABEL
    display.draw_black.text((150, 140), "+6h", fill=0, font=font16)  # +6h LABEL
    display.draw_black.text((270, 140), "+12h", fill=0, font=font16)  # +12h LABEL
    # 3H
    display.draw_icon(25, 160, "r", 50, 50,
                      weather.weather_description(weather.hourly_forecast()["+3h"]["id"])[0])  # +3H WEATHER ICON
    display.draw_black.text((25, 210), weather.weather_description(weather.hourly_forecast()["+3h"]["id"])[1], fill=0,
                            font=font12)  # WEATHER DESCRIPTION +3h
    display.draw_black.text((30, 225), weather.hourly_forecast()["+3h"]["temp"], fill=0, font=font16)  # TEMP +3H
    display.draw_black.text((30, 240), weather.hourly_forecast()["+3h"]["pop"], fill=0, font=font16)  # POP +3H
    # +6h
    display.draw_icon(145, 160, "r", 50, 50,
                      weather.weather_description(weather.hourly_forecast()["+6h"]["id"])[0])  # +6H WEATHER ICON
    display.draw_black.text((145, 210), weather.weather_description(weather.hourly_forecast()["+6h"]["id"])[1], fill=0,
                            font=font12)  # WEATHER DESCRIPTION +6h
    display.draw_black.text((150, 225), weather.hourly_forecast()["+6h"]["temp"], fill=0, font=font16)  # TEMP +6H
    display.draw_black.text((150, 240), weather.hourly_forecast()["+6h"]["pop"], fill=0, font=font16)  # POP +6H
    # +12h
    display.draw_icon(265, 160, "r", 50, 50,
                      weather.weather_description(weather.hourly_forecast()["+12h"]["id"])[0])  # +12H WEATHER ICON
    display.draw_black.text((265, 210), weather.weather_description(weather.hourly_forecast()["+12h"]["id"])[1], fill=0,
                            font=font12)  # WEATHER DESCRIPTION +12h
    display.draw_black.text((270, 225), weather.hourly_forecast()["+12h"]["temp"], fill=0, font=font16)  # TEMP +12H
    display.draw_black.text((270, 240), weather.hourly_forecast()["+12h"]["pop"], fill=0, font=font16)  # POP +12H

    ###################################################################################################################
    # NEWS UPDATE
    news_selected = news.selected_title()
    display.draw_black.text((360, 10), "Notícias", fill=0, font=font24)

    line_height = 16  # Height of each line of text
    spacing_between_news = 13  # Additional space between news items
    y_base = 50

    print("Drawing news");

    for i, news_item in enumerate(news_selected):
        print(news_item);
        if i == 5:
            break

        if len(news_selected) == 1:
            display.draw_black.text((360, y_base), news_selected[0], fill=0, font=font14)
            break
        else:
            num_lines = min(3, len(news_item))  # Limits the number of lines to a maximum of 3
            for j in range(num_lines):
                text = news_item[j] if j < 2 else news_item[j] + "[...]"  # Adds '...' to the last line if there are more than 3 items
                display.draw_black.text((360, y_base + j * line_height), text, fill=0, font=font14)
            y_base += num_lines * line_height + spacing_between_news

    ###################################################################################################################
    # CLOCK
    current_time = time.strftime("%H:%M", time.localtime()) + "H"
    display.draw_text(400 - font48.getsize(current_time)[0] // 2, 400, current_time, font=font48, color="r")

    print("Updating screen...")
    if debug == 0:
        epd.display(epd.getbuffer(display.im_black), epd.getbuffer(display.im_red))
    else:
        display.im_black.show()

    display.clear("b")
    display.clear("r")

    return True


if __name__ == "__main__":
    global been_reboot
    been_reboot=1
    while True:
        try:
            weather = Weather(lat, lon, api_key_weather)
            news = News()
            break
        except:
            current_time = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
            print("INITIALIZATION PROBLEM- @" + current_time)
            time.sleep(2)
    if debug == 0:
        epd = EPD()

    first_run = True

    display = Display()

    while True:
        with display_semaphore:  # Acquire semaphore before updating display
            # Defining objects
            current_time = time.strftime("%d/%m/%Y %H:%M", time.localtime())
            print("Begin update @" + current_time)
            print("Creating display")
            if debug == 0:
                epd.init()
            # Update values
            weather.update()
            print("Weather Updated")
            news.update(api_key_news)
            print("News Updated")
            print("Main program running...")
            # main()
            if debug == 0:
                print("Going to sleep...")
                epd.sleep()
                print("Sleeping ZZZzzzzZZZzzz")
            print("Done")
            print("------------")
            if first_run:
                # Start the time update thread
                time_thread = threading.Thread(target=update_time)
                time_thread.daemon = True  # Daemonize thread
                time_thread.start()
                first_run = False
        time.sleep(1800)  # Sleep for 30 minutes before the next full update
