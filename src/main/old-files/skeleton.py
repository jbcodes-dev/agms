from abc import ABC


class BaseSystem(ABC):

    class SubSystem(ABC):
        """ Humidity Regulation / Lighting / Irrigation """

        class Module(ABC):
            """ Sensor / Relay """

            def __init__(self, name, desc):
                self._name = name
                self._desc = desc

            @property
            def name(self):
                return self._name

            @property
            def desc(self):
                return self._desc

        def __init__(self, name, desc):
            self._name = name
            self._desc = desc
            self._modules = {}

        @property
        def name(self):
            return self._name

        @property
        def desc(self):
            return self._desc

        @property
        def modules(self):
            return self._modules

        def add_module(self, module):
            self._modules[module.name] = module

    def __init__(self, name):
        self._name = name
        self._subsystems = {}

    @property
    def name(self):
        return self._name

    @property
    def subsystems(self):
        return self._subsystems

    def add_subsystem(self, subsystem):
        self._subsystems[subsystem.name] = subsystem

