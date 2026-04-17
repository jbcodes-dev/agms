"""
Author: Jake Brown
ID: 001239595
Purpose: class definition for fuzzy-logic irrigation algorithm module.
"""

import numpy as np
import skfuzzy as skf
from skfuzzy import control as ctrl


class IrrigationAlgorithm:
    def __init__(self):
        self.soil_temperature = None
        self.soil_moisture = None
        self.pump = None
        self.rules = []
        self.pump_ctrl = None
        self.pump_sim = None

        self.setup()

    def setup(self):
        # define inputs
        self.soil_temperature = ctrl.Antecedent(np.arange(15.0, 28.0, 0.1), 'soil_temperature')
        self.soil_moisture = ctrl.Antecedent(np.arange(0.0, 1015.0, 0.1), 'soil_moisture')

        # define output
        self.pump = ctrl.Consequent(np.arange(0.0, 101.0, 1.0), 'pump')

        # define membership functions
        self.create_mf()

        # define rules
        self.create_rules()

        # setup fuzzy control system
        self.create_system()


    def create_mf(self):
        # soil temperature membership functions
        self.soil_temperature['cold'] = skf.trimf(self.soil_temperature.universe, [15.0, 15.0, 20.0])
        self.soil_temperature['norm'] = skf.trimf(self.soil_temperature.universe, [20.0, 22.0, 24.0])
        self.soil_temperature['hot'] = skf.trimf(self.soil_temperature.universe, [22.0, 28.0, 28.0])

        # soil moisture membership functions
        self.soil_moisture['low'] = skf.trimf(self.soil_moisture.universe, [300.0, 300.0, 600.0])
        self.soil_moisture['med'] = skf.trimf(self.soil_moisture.universe, [375.0, 600.0, 800.0])
        self.soil_moisture['high'] = skf.trimf(self.soil_moisture.universe, [600.0, 1015.0, 1015.0])

        # pump membership functions
        self.pump['short'] = skf.trimf(self.pump.universe, [0.0, 0.0, 50.0])
        self.pump['medium'] = skf.trimf(self.pump.universe, [25.0, 50.0, 75.0])
        self.pump['long'] = skf.trimf(self.pump.universe, [50.0, 100.0, 100.0])


    def create_rules(self):
        # rules
        self.rules.append(ctrl.Rule(self.soil_temperature['cold'] | self.soil_moisture['low'], self.pump['short']))
        self.rules.append(ctrl.Rule(self.soil_temperature['norm'] | self.soil_moisture['high'], self.pump['medium']))
        self.rules.append(ctrl.Rule(self.soil_temperature['hot'] | self.soil_moisture['high'], self.pump['long']))


    def create_system(self):
        # define control system
        self.pump_ctrl = ctrl.ControlSystem([self.rules[0], self.rules[1], self.rules[2]])
        self.pump_sim = ctrl.ControlSystemSimulation(self.pump_ctrl)


    def compute(self, soil_temperature, soil_moisture):
        self.pump_sim.input['soil_temperature'] = soil_temperature
        self.pump_sim.input['soil_moisture'] = soil_moisture

        self.pump_sim.compute()

        if self.pump_sim.output['pump'] <= 35.0:
            return 'short'

        elif 35.0 <= self.pump_sim.output['pump'] <= 65.0:
            return 'medium'

        else:
            return 'long'



if __name__ == '__main__':
    alg = IrrigationAlgorithm()

    print(alg.compute(22.0, 650.0))        
