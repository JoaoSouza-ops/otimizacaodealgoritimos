# Mesma regra do pip atividade 1
import subprocess, sys
try:
    import skfuzzy
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "scikit-fuzzy"])
    import skfuzzy

import os
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl   
import matplotlib.pyplot as plt

os.makedirs("imagens", exist_ok=True)

qualidade = ctrl.Antecedent(np.arange(0, 11, 1), "qualidade")
servico   = ctrl.Antecedent(np.arange(0, 11, 1), "servico")
gorjeta   = ctrl.Consequent(np.arange(0, 26, 1), "gorjeta")


qualidade.automf(3, names=["ruim", "razoavel", "otima"])
servico.automf(3,   names=["ruim", "aceitavel", "excelente"])


gorjeta["baixa"] = fuzz.trimf(gorjeta.universe, [0, 0, 13])
gorjeta["media"] = fuzz.trimf(gorjeta.universe, [0, 13, 25])
gorjeta["alta"]  = fuzz.trimf(gorjeta.universe, [13, 25, 25])


regra1 = ctrl.Rule(servico["excelente"] | qualidade["otima"], gorjeta["alta"])
regra2 = ctrl.Rule(servico["aceitavel"],                      gorjeta["media"])
regra3 = ctrl.Rule(servico["ruim"] & qualidade["ruim"],       gorjeta["baixa"])


sistema_gorjeta = ctrl.ControlSystem([regra1, regra2, regra3])
simulador = ctrl.ControlSystemSimulation(sistema_gorjeta)


simulador.input["qualidade"] = 6.5
simulador.input["servico"]   = 9.8

simulador.compute()

resultado = simulador.output["gorjeta"]
print(f"Gorjeta recomendada: {resultado:.2f}%")


qualidade.view(sim=simulador)
plt.savefig("imagens/lab02_qualidade.png", dpi=150)
servico.view(sim=simulador)
plt.savefig("imagens/lab02_servico.png", dpi=150)
gorjeta.view(sim=simulador)
plt.savefig("imagens/lab02_gorjeta.png", dpi=150)
plt.show()
