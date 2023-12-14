import re
import subprocess

from abc import ABC, abstractmethod


class Cpu(ABC):

    @abstractmethod
    def get_load(self):
        pass

    @abstractmethod
    def get_temperature(self):
        pass


class Memory(ABC):

    @abstractmethod
    def get_total(self):
        pass

    @abstractmethod
    def get_used(self):
        pass

    @abstractmethod
    def get_free(self):
        pass


class Factory(ABC):

    @abstractmethod
    def create_cpu(self):
        pass

    @abstractmethod
    def create_memory(self):
        pass


class LinuxCpu(Cpu):

    def get_load(self):
        
        command = "cat /proc/loadavg"

        output = subprocess.run(command, stdout=subprocess.PIPE, shell=True, text=True).stdout

        load = float(output.split()[0].strip())

        return load

    def get_temperature(self):

        command = "vcgencmd measure_temp"

        output = subprocess.run(command, stdout=subprocess.PIPE, shell=True, text=True).stdout

        temperature = float(re.search(r'\d+\.\d+', output).group())

        return temperature
    

class LinuxMemory(Memory):

    def get_total(self):
        
        command = "free -b"

        output = subprocess.run(command, stdout=subprocess.PIPE, shell=True, text=True).stdout

        memory = int(output.split('\n')[1].split()[1].strip())

        return memory

    def get_used(self):
        return self.get_total() - self.get_free()

    def get_free(self):
        
        command = "free -b"

        output = subprocess.run(command, stdout=subprocess.PIPE, shell=True, text=True).stdout

        memory = int(output.split('\n')[1].split()[3].strip())

        return memory


class WindowsCpu(Cpu):

    def get_load(self):
        
        command = "wmic cpu get loadpercentage"

        output = subprocess.run(command, stdout=subprocess.PIPE, shell=True, text=True).stdout

        load = float(output.split('\n\n')[1].strip()) / 100

        return load

    def get_temperature(self):

        command = "wmic /namespace:\\\\root\\cimv2 path Win32_PerfFormattedData_Counters_ThermalZoneInformation get Temperature"

        output = subprocess.run(command, stdout=subprocess.PIPE, shell=True, text=True).stdout

        temperature = float(output.split('\n\n')[1].strip()) - 273

        return temperature
    

class WindowsMemory(Memory):

    def get_total(self):
        
        command = "wmic memorychip get capacity"

        output = subprocess.run(command, stdout=subprocess.PIPE, shell=True, text=True).stdout

        memory_units = [int(value.strip()) for value in output.split('\n\n')[1:] if value.strip()]

        memory = sum(memory_units)

        return memory

    def get_used(self):
        return self.get_total() - self.get_free()

    def get_free(self):
        
        command = "wmic OS get FreePhysicalMemory"

        output = subprocess.run(command, stdout=subprocess.PIPE, shell=True, text=True).stdout

        memory = int(output.split('\n\n')[1].strip()) * 1024

        return memory


class LinuxFactory(Factory):

    def create_cpu(self):
        return LinuxCpu()

    def create_memory(self):
        return LinuxMemory()
    

class WindowsFactory(Factory):

    def create_cpu(self):
        return WindowsCpu()

    def create_memory(self):
        return WindowsMemory()


FACTORIES = {

    'posix': {
        'name': "Linux",
        'factory': LinuxFactory
    },

    'nt': {
        'name': "Windows",
        'factory': WindowsFactory
    }

}
