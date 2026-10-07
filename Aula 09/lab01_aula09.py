# Aqui uso subprocess porque "!pip" só funciona em notebook, não em arquivo .py.
import subprocess, sys
try:
    import skfuzzy
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "scikit-fuzzy"])
    import skfuzzy

import os
import numpy as np                 
import skfuzzy as fuzz             
import matplotlib.pyplot as plt    

os.makedirs("imagens", exist_ok=True)

x_servico   = np.arange(0, 11, 0.1)  
x_qualidade = np.arange(0, 11, 0.1)   
x_gorjeta   = np.arange(0, 26, 0.1)   


servico_ruim  = fuzz.trimf(x_servico, [0, 0, 5])
servico_aceit = fuzz.trimf(x_servico, [0, 5, 10])
servico_exc   = fuzz.trimf(x_servico, [5, 10, 10])


qual_ruim     = fuzz.trimf(x_qualidade, [0, 0, 5])
qual_razoavel = fuzz.trimf(x_qualidade, [0, 5, 10])
qual_otima    = fuzz.trimf(x_qualidade, [5, 10, 10])


gorj_baixa = fuzz.trimf(x_gorjeta, [0, 0, 13])
gorj_media = fuzz.trimf(x_gorjeta, [0, 13, 25])
gorj_alta  = fuzz.trimf(x_gorjeta, [13, 25, 25])

# Gráficos 
fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))

ax0.plot(x_servico, servico_ruim,  "b", linewidth=1.5, label="Ruim")
ax0.plot(x_servico, servico_aceit, "g", linewidth=1.5, label="Aceitável")
ax0.plot(x_servico, servico_exc,   "r", linewidth=1.5, label="Excelente")
ax0.set_title("Serviço")
ax0.legend()

ax1.plot(x_qualidade, qual_ruim,     "b", linewidth=1.5, label="Ruim")
ax1.plot(x_qualidade, qual_razoavel, "g", linewidth=1.5, label="Razoável")
ax1.plot(x_qualidade, qual_otima,    "r", linewidth=1.5, label="Ótima")
ax1.set_title("Qualidade da comida")
ax1.legend()

ax2.plot(x_gorjeta, gorj_baixa, "b", linewidth=1.5, label="Baixa")
ax2.plot(x_gorjeta, gorj_media, "g", linewidth=1.5, label="Média")
ax2.plot(x_gorjeta, gorj_alta,  "r", linewidth=1.5, label="Alta")
ax2.set_title("Gorjeta (%)")
ax2.legend()


for ax in (ax0, ax1, ax2):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_ylabel("Pertinência")

plt.tight_layout()                                              
plt.savefig("imagens/lab01_funcoes_pertinencia.png", dpi=150)  
plt.show()                                                      


serv = 9.8
print(f"Fuzzificação do serviço = {serv}")
print("  Ruim      :", round(float(fuzz.interp_membership(x_servico, servico_ruim,  serv)), 3))
print("  Aceitável :", round(float(fuzz.interp_membership(x_servico, servico_aceit, serv)), 3))
print("  Excelente :", round(float(fuzz.interp_membership(x_servico, servico_exc,   serv)), 3))

