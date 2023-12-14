from factories import FACTORIES


class SystemStateMonitor:

    def __init__(self, factory, messenger):

        self.__factory = factory
        self.__messenger = messenger

    def send_system_state_message(self, api_key, receiver):

        cpu, memory = self.__factory.create_cpu(), self.__factory.create_memory()

        message = f"System information ({self.get_os_name()}):\n\n" + \
            f"CPU Temperature: {cpu.get_temperature()} °C\n" + \
            f"CPU Usage: {cpu.get_load() * 100}%\n\n" + \
            f"Total Memory: {memory.get_total() / 1024 / 1024 / 1024:.3f} GB\n" + \
            f"Used Memory: {memory.get_used() / 1024 / 1024 / 1024:.3f} GB\n" + \
            f"Free Memory: {memory.get_free() / 1024 / 1024 / 1024:.3f} GB"
        
        return self.__messenger.send_message(api_key, receiver, message)


    def get_os_name(self):

        for _os in FACTORIES.values():
            if isinstance(self.__factory, _os['factory']):
                return _os['name']

        return None
