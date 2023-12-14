import uuid

from datetime import datetime as dt
from abc import ABC, abstractmethod

from messengers import MESSENGERS
from utils import get_weather
from config import API_KEYS, OPENWEATHERAPP_API_KEY, WEATHER_UNITS


class Command(ABC):

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def log(self):
        pass


class AddTaskCommand(Command):

    def __init__(self, scheduler, receiver, city, messenger, units, interval):

        self.__scheduler = scheduler
        
        self.__receiver = receiver
        self.__city = city
        self.__messenger = messenger.lower()
        self.__units = units.lower()
        self.__interval = interval

        self.__success = None
        self.__error_message = None

    def execute(self):

        try:

            if self.__messenger not in API_KEYS:
                raise Exception(f"Invalid messenger \"{self.__messenger}\"")
            
            if self.__units not in WEATHER_UNITS:
                raise Exception(f"Invalid units \"{self.__units}\"")

            def function():

                weather_result = get_weather(OPENWEATHERAPP_API_KEY, self.__city, self.__units)

                if not weather_result['success']:
                    print(f"[{dt.now().strftime('%d-%m-%Y %H:%M:%S')}] {weather_result['error']}")
                    return

                weather = weather_result['weather']

                message = f"Weather in {self.__city.title()}:\n\n" \
                    f"Temperature: {weather['temperature']} {WEATHER_UNITS[self.__units]['temperature']}\n" \
                    f"Pressure: {weather['pressure']} hPa\n" \
                    f"Humidity: {weather['humidity']} %\n" \
                    f"Wind Speed: {weather['wind_speed']} {WEATHER_UNITS[self.__units]['wind_speed']}"

                success = MESSENGERS[self.__messenger].send_message(API_KEYS[self.__messenger], self.__receiver, message)

                print(f"[{dt.now().strftime('%d-%m-%Y %H:%M:%S')}] {'Success' if success else 'Failed'}.")

            task_id = str(uuid.uuid4())

            self.__scheduler.add_job(func=function, trigger='interval', seconds=self.__interval, id=task_id)

            self.__success = True

            return {
                'success': self.__success,
                'task_id': task_id
            }

        except Exception as exception:

            self.__success = False

            self.__error_message = f"{type(exception).__name__}: {exception}"

            return {
                'success': self.__success,
                'error': {
                    'type': type(exception).__name__,
                    'message': str(exception)
                }
            }

    def log(self):

        if self.__success:
            print(f"Task added successfully for {self.__city.title()} every {self.__interval} seconds")

        elif not self.__success:
            print(f"Task not added for {self.__city.title()}. Error: {self.__error_message}")

        else:
            print("Add task command not executed")


class ModifyTaskCommand(Command):

    def __init__(self, scheduler, task_id, interval):

        self.__scheduler = scheduler

        self.__task_id = task_id
        self.__interval = interval

        self.__success = None
        self.__error_message = None

    def execute(self):

        try:

            self.__scheduler.reschedule_job(self.__task_id, trigger='interval', seconds=self.__interval)

            self.__success = True

            return {
                'success': self.__success
            }

        except Exception as exception:

            self.__success = False

            self.__error_message = f"{type(exception).__name__}: {exception}"

            return {
                'success': self.__success,
                'error': {
                    'type': type(exception).__name__,
                    'message': str(exception)
                }
            }
        
    def log(self):

        if self.__success:
            print(f"Task {self.__task_id} modified successfully")

        elif not self.__success:
            print(f"Task {self.__task_id} not modified. Error: {self.__error_message}")

        else:
            print("Modify task command not executed")


class RemoveTaskCommand(Command):

    def __init__(self, scheduler, task_id):

        self.__scheduler = scheduler

        self.__task_id = task_id

        self.__success = None
        self.__error_message = None

    def execute(self):

        try:

            self.__scheduler.remove_job(self.__task_id)

            self.__success = True

            return {
                'success': self.__success
            }

        except Exception as exception:

            self.__success = False

            self.__error_message = f"{type(exception).__name__}: {exception}"

            return {
                'success': self.__success,
                'error': {
                    'type': type(exception).__name__,
                    'message': str(exception)
                }
            }

    def log(self):

        if self.__success:
            print(f"Task {self.__task_id} removed successfully")

        elif not self.__success:
            print(f"Task {self.__task_id} not removed. Error: {self.__error_message}")

        else:
            print("Remove task command not executed")


class CommandExecutor:

    def set_command(self, command):
        self.__command = command

    def execute_command(self):

        result = self.__command.execute()

        self.__command.log()

        return result
