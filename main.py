import os

from datetime import datetime as dt

from apscheduler.schedulers.background import BackgroundScheduler

from messengers import MESSENGERS
from utils import get_weather
from config import API_KEYS, OPENWEATHERAPP_API_KEY, WEATHER_UNITS, SEND_MESSAGE_EVERY


def execute(function):

    def executor():

        success = function()

        print(f"[{dt.now().strftime('%d-%m-%Y %H:%M:%S')}] {'Success' if success else 'Failed'}.")

    return executor


def main():

    success = False

    weather_units = list(WEATHER_UNITS.keys())

    messengers = list(MESSENGERS.keys())

    while not success:

        try:

            city = input("Enter city to get weather in: ")

            print("\nChoose unit:\n\t" + '\n\t'.join([str(i + 1) + ': ' + weather_units[i] for i in range(len(weather_units))]))

            weather_unit_index = int(input("Unit: ")) - 1

            try:
                weather_unit = weather_units[weather_unit_index]
            except IndexError:
                print("\nInvalid unit\n")
                continue

            print("\nChoose messenger:\n\t" + '\n\t'.join([str(i + 1) + ': ' + messengers[i] for i in range(len(messengers))]))

            messenger_index = int(input("Messenger: ")) - 1

            try:
                messenger = messengers[messenger_index]
            except IndexError:
                print("\nInvalid messenger\n")
                continue

            receiver = input("Enter receiver: ")

            weather_result = get_weather(OPENWEATHERAPP_API_KEY, city, weather_unit)

            if not weather_result['success']:
                print(f"\n{weather_result['error']}\n")
                continue

            weather = weather_result['weather']

            message = f"Weather in {city.title()}:\n\n" \
                f"Temperature: {weather['temperature']} {WEATHER_UNITS[weather_unit]['temperature']}\n" \
                f"Pressure: {weather['pressure']} hPa\n" \
                f"Humidity: {weather['humidity']} %\n" \
                f"Wind Speed: {weather['wind_speed']} {WEATHER_UNITS[weather_unit]['wind_speed']}"

            scheduler = BackgroundScheduler()

            scheduler.add_job(
                func=execute(lambda: MESSENGERS[messenger].send_message(API_KEYS[messenger], receiver, message)),
                trigger="interval",
                seconds=SEND_MESSAGE_EVERY
            )

            scheduler.start()

            success = True

        except Exception as exception:
            print(f"\n{type(exception).__name__}: {exception}\n")

    print("\nSuccess!\n")

    while True:
        pass


if __name__ == '__main__':
    main()


