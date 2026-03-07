import numpy as np
import skfuzzy as skf
from skfuzzy import control as ctrl


class AirflowAlgorithm:
    def __init__(self):
        self.temperature = None
        self.humidity = None
        self.fans = None
        self.rules = []
        self.fan_ctrl = None
        self.fan_sim = None

        self.setup()

    def setup(self):
        # define inputs
        self.temperature = ctrl.Antecedent(np.arange(16.0, 28.0, 0.1), 'temperature')
        self.humidity = ctrl.Antecedent(np.arange(0.0, 101.0, 0.1), 'humidity')
        
        # define output
        self.fans = ctrl.Consequent(np.arange(0.0, 101.0, 1), 'fans')

        # define membership functions
        self.create_mf()

        # define rules
        self.create_rules()

        # setup fuzzy control system
        self.create_system()


    def create_mf(self):
        # temperature membership functions
        self.temperature['cold'] = skf.trimf(temperature.universe, [18.0, 18.0, 20.0])
        self.temperature['norm'] = skf.trimf(temperature.universe, [20.0, 22.0, 24.0])
        self.temperature['hot'] = skf.trimf(temperature.universe, [22.0, 28.0, 28.0])

        # humidity membership functions
        self.humidity['cold'] = skf.trimf(humidity.universe, [30.0, 30.0, 70.0])
        self.humidity['norm'] = skf.trimf(humidity.universe, [50.0, 70.0, 80.0])
        self.humidity['hot'] = skf.trimf(humidity.universe, [70.0, 90.0, 90.0])

        # fans membership functions
        self.fans['off'] = skf.trimf(fans.universe, [0, 0, 50])
        self.fans['half'] = skf.trimf(fans.universe, [25, 50, 75])
        self.fans['full'] = skf.trimf(fans.universe, [50, 100, 100])


    def create_rules(self):
        # rules
        self.rules.append(ctrl.Rule(temperature['cold'] | humidity['cold'], fans['off']))
        self.rules.append(ctrl.Rule(temperature['norm'] | humidity['hot'], fans['half']))
        self.rules.append(ctrl.Rule(temperature['hot'] | humidity['hot'], fans['full']))

    
    def create_system(self):
        # define control system
        self.fan_ctrl = ctrl.ControlSystem([self.rules[0], self.rules[1], self.rules[2]])
        self.fan_sim = ctrl.ControlSystemSimulation(self.fan_ctrl)


    def compute(self, temperature, humidity):
        self.fan_sim.input['temperature'] = temperature
        self.fan_sim.input['humidity'] = humidity

        self.fan_sim.compute()

        if self.fan_sim.output['fans'] <= 35.0:
            return 'off'

        elif 35.0 <= self.fan_sim.output['fans'] <= 65.0:
            return 'half'

        else:
            return 'full'

