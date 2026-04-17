"""
Author: Jake Brown
ID: 001239595
Purpose: class definition for fuzzy-logic airflow algorithm module.
"""

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
        self.temperature['cold'] = skf.trimf(self.temperature.universe, [16.0, 16.0, 20.0])
        self.temperature['norm'] = skf.trimf(self.temperature.universe, [20.0, 22.0, 24.0])
        self.temperature['hot'] = skf.trimf(self.temperature.universe, [22.0, 28.0, 28.0])

        # humidity membership functions
        self.humidity['cold'] = skf.trimf(self.humidity.universe, [0.0, 0.0, 70.0])
        self.humidity['norm'] = skf.trimf(self.humidity.universe, [50.0, 70.0, 80.0])
        self.humidity['hot'] = skf.trimf(self.humidity.universe, [70.0, 100.0, 100.0])

        # fans membership functions
        self.fans['off'] = skf.trimf(self.fans.universe, [0, 0, 50])
        self.fans['half'] = skf.trimf(self.fans.universe, [25, 50, 75])
        self.fans['full'] = skf.trimf(self.fans.universe, [50, 100, 100])


    def create_rules(self):
        # rules
        self.rules.append(ctrl.Rule(self.temperature['cold'] | self.humidity['cold'], self.fans['off']))
        self.rules.append(ctrl.Rule(self.temperature['norm'] | self.humidity['hot'], self.fans['half']))
        self.rules.append(ctrl.Rule(self.temperature['hot'] | self.humidity['hot'], self.fans['full']))

    
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


if __name__ == '__main__':
    alg = AirflowAlgorithm()

    print(alg.compute(17.8, 70.0))

