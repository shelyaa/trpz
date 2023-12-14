import os

from datetime import datetime as dt

from apscheduler.schedulers.background import BackgroundScheduler

from messengers import MESSENGERS
from factories import FACTORIES
from monitor import SystemStateMonitor
from config import API_KEYS, SEND_MESSAGE_EVERY


def execute(function):

    def executor():

        success = function()

        print(f"[{dt.now().strftime('%d-%m-%Y %H:%M:%S')}] {'Success' if success else 'Failed'}.")

    return executor


def main():

    success = False

    messengers = list(MESSENGERS.keys())

    while not success:

        try:

            print("\nChoose messenger:\n\t" + '\n\t'.join([str(i + 1) + ': ' + messengers[i] for i in range(len(messengers))]))

            messenger_index = int(input("Messenger: ")) - 1

            try:
                messenger = messengers[messenger_index]
            except IndexError:
                print("\nInvalid messenger\n")
                continue

            receiver = input("Enter receiver: ")

            os_name = os.name

            factory = FACTORIES[os_name]['factory']()

            monitor = SystemStateMonitor(factory, MESSENGERS[messenger])

            print(f"\nOperating system: {monitor.get_os_name()}\n")
            
            scheduler = BackgroundScheduler()

            scheduler.add_job(
                func=execute(lambda: monitor.send_system_state_message(API_KEYS[messenger], receiver)),
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
