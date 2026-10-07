!pip install matplotlib
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

temperatura = ctrl.Antecedent(np.arange(0, 41, 1), "temperatura")
velocidade = ctrl.Consequent(np.arange(0, 101, 1), "velocidade")

temperatura["frio"] = fuzz.trapmf(temperatura.universe, [0, 0, 15, 25])
temperatura["morno"] = fuzz.trimf(temperatura.universe, [15, 25, 35])
temperatura["quente"] = fuzz.trapmf(temperatura.universe, [25, 35, 40, 40])
 
velocidade["baixa"] = fuzz.trimf(velocidade.universe, [0, 0, 50])
velocidade["media"] = fuzz.trimf(velocidade.universe, [0, 50, 100])
velocidade["alta"] = fuzz.trimf(velocidade.universe, [50, 100, 100])
 
regras = [
    ctrl.Rule(temperatura["frio"], velocidade["baixa"]),
    ctrl.Rule(temperatura["morno"], velocidade["media"]),
    ctrl.Rule(temperatura["quente"], velocidade["alta"]),
]
 
sistema = ctrl.ControlSystem(regras)
ventilador = ctrl.ControlSystemSimulation(sistema)
 
for temp in [10, 20, 25, 30, 38]:
    ventilador.input["temperatura"] = temp
    ventilador.compute()
    print(f"{temp}°C -> ventilador a {ventilador.output['velocidade']:.0f}%")
 

import matplotlib.pyplot as plt
temperatura.view()
velocidade.view()
plt.show()
