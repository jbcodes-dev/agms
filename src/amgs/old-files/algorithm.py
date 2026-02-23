class Algorithm:
    def __init__(self):
        self._air_data = None
        self._soil_data = None
        self._light_data = None

        self._actions = None

    @property
    def air_data(self):
        return self._air_data
    
    @air_data.setter
    def air_data(self, air_zip):
        self._air_data = air_zip

    @property
    def soil_data(self):
        return self._soil_data
    
    @soil_data.setter
    def soil_data(self, soil_zip):
        self._soil_data = soil_zip

    @property
    def light_data(self):
        return self._light_data
    
    @light_data.setter
    def light_data(self, light_zip):
        self._light_data = light_zip

    @property
    def actions(self):
        return self._actions
    
    @actions.setter
    def actions(self, new_actions):
        self._actions = new_actions

    def cleanup(self):
        """ Prepare for next calculation """
        self.air_data = None
        self.soil_data = None
        self.light_data = None
        self.actions = None

    def process(self):
        """ Process fuzzified data to produce results """

        action_set = {
            "fans": None,
            "pump": None,
            "light": None
        }

        # TODO: implement rule-based fuzzy algorithm for the Humidity Regulation System
        # TODO: implement a timer-based activation algorithm for the Irrigation System
        # TODO: implement a time-of-day based activation algorithm for the Lighting System

        ### All values are placeholders and will be changed. ###

        # air data eval
        if self.air_data["air_temp"] >= 22.0 or self.air_data["air_humidity"] >= 70.0:
            action_set["fans"] = True

        else:
            action_set["fans"] = False


        # soil data eval
        if self.soil_data["soil_moisture"] <= 35.0:
            action_set["pump"] = True

        elif self.soil_data["soil_moisture"] >= 50.0:
            action_set["pump"] = False

        else:
            action_set["pump"] = True
            

        # light data eval
        
        if "05:59" <= self.light_data["time"] <= "18:00":
            action_set["light"] = False

        else:
            action_set["light"] = True

        # apply actions
        self.actions = action_set
    