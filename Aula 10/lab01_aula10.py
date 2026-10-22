"""Aula 10 - Motor de inferência Mamdani e superfície 3D (AC-3, Sprint 2)."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# ---------------------------------------------------------------- universos
imp_u = np.arange(0, 100.1, 0.5)
exp_u = np.arange(0, 10.01, 0.05)
urg_u = np.arange(0, 100.1, 0.5)


def construir_sistema(critica="trimf", defuzz="centroid"):
    """critica: 'trimf' ou 'trapmf' (forma da Urgência Crítica).
    defuzz: 'centroid', 'mom', 'som', 'lom', 'bisector'."""
    impacto = ctrl.Antecedent(imp_u, "impacto")
    explor = ctrl.Antecedent(exp_u, "explorabilidade")
    urg = ctrl.Consequent(urg_u, "urgencia", defuzzify_method=defuzz)

    impacto["baixo"] = fuzz.trimf(imp_u, [0, 0, 40])
    impacto["medio"] = fuzz.trimf(imp_u, [20, 50, 80])
    impacto["alto"] = fuzz.trimf(imp_u, [60, 100, 100])

    explor["baixa"] = fuzz.trimf(exp_u, [0, 0, 4])
    explor["moderada"] = fuzz.trimf(exp_u, [2, 5, 8])
    explor["alta"] = fuzz.trimf(exp_u, [6, 10, 10])

    if critica == "trapmf_estreito":   # trapézios estreitos encostados nas duas pontas
        urg["baixa"] = fuzz.trapmf(urg_u, [0, 0, 2, 30])
    else:
        urg["baixa"] = fuzz.trimf(urg_u, [0, 0, 30])
    urg["media"] = fuzz.trimf(urg_u, [15, 40, 65])
    urg["alta"] = fuzz.trimf(urg_u, [50, 70, 90])
    if critica == "trapmf":   # plateau de 100% nas bordas
        urg["critica"] = fuzz.trapmf(urg_u, [75, 90, 100, 100])
    elif critica == "trapmf_estreito":
        urg["critica"] = fuzz.trapmf(urg_u, [70, 98, 100, 100])
    else:
        urg["critica"] = fuzz.trimf(urg_u, [70, 100, 100])

    # Matriz 3x3 (linha = impacto, coluna = explorabilidade)
    matriz = {
        ("baixo", "baixa"): "baixa", ("baixo", "moderada"): "baixa", ("baixo", "alta"): "media",
        ("medio", "baixa"): "media", ("medio", "moderada"): "alta", ("medio", "alta"): "alta",
        ("alto", "baixa"): "critica", ("alto", "moderada"): "critica", ("alto", "alta"): "critica",
    }
    regras = [ctrl.Rule(impacto[i] & explor[e], urg[u]) for (i, e), u in matriz.items()]
    assert len(regras) == 9
    return ctrl.ControlSystem(regras), (impacto, explor, urg)


def avaliar(sim, i, e):
    sim.input["impacto"] = i
    sim.input["explorabilidade"] = e
    sim.compute()
    return float(sim.output["urgencia"])


def superficie(sim, n=41):
    xs = np.linspace(0, 100, n)
    ys = np.linspace(0, 10, n)
    Z = np.zeros((n, n))
    for a, i in enumerate(ys):          # linhas = explorabilidade
        for b, j in enumerate(xs):      # colunas = impacto
            Z[a, b] = avaliar(sim, j, i)
    return xs, ys, Z


def plot_superficie(ax, xs, ys, Z, titulo):
    X, Y = np.meshgrid(xs, ys)
    s = ax.plot_surface(X, Y, Z, cmap="viridis", edgecolor="none")
    ax.set_xlabel("Impacto (%)")
    ax.set_ylabel("Explorabilidade (0-10)")
    ax.set_zlabel("Urgência (%)")
    ax.set_zlim(0, 100)
    ax.set_title(titulo)
    ax.view_init(elev=28, azim=-125)
    return s


if __name__ == "__main__":
    configs = {
        "Centroide + trimf (base)": ("trimf", "centroid"),
        "Abordagem A: Centroide + trapmf": ("trapmf", "centroid"),
        "Abordagem B: MOM + trimf": ("trimf", "mom"),
        "Abordagem C: trapmf estreito + centroide": ("trapmf_estreito", "centroid"),
    }
    sims, resultados = {}, {}
    print(f"{'Configuração':36s} {'(0,0)':>8s} {'(100,10)':>9s} {'(50,5)':>8s}")
    for nome, (forma, met) in configs.items():
        sistema, _ = construir_sistema(forma, met)
        sim = ctrl.ControlSystemSimulation(sistema)
        sims[nome] = sim
        r = [avaliar(sim, 0, 0), avaliar(sim, 100, 10), avaliar(sim, 50, 5)]
        resultados[nome] = r
        print(f"{nome:42s} {r[0]:8.2f} {r[1]:9.2f} {r[2]:8.2f}")

    # --- Funções de pertinência de saída (centroide x trapézio)
    fig, axs = plt.subplots(1, 3, figsize=(16, 3.6), sharey=True)
    for ax, forma in zip(axs, ["trimf", "trapmf", "trapmf_estreito"]):
        _, (_, _, urg) = construir_sistema(forma, "centroid")
        for termo in urg.terms:
            ax.plot(urg_u, urg[termo].mf, label=termo)
        ax.set_title(f"Urgência — crítica = {forma}")
        ax.set_xlabel("Urgência (%)")
        ax.legend()
    plt.tight_layout()
    plt.savefig("pertinencia_urgencia.png", dpi=130)
    plt.close()

    # --- Superfícies comparativas
    fig = plt.figure(figsize=(22, 5.5))
    zs = {}
    for k, (nome, sim) in enumerate(sims.items(), 1):
        xs, ys, Z = superficie(sim)
        zs[nome] = Z
        ax = fig.add_subplot(1, 4, k, projection="3d")
        plot_superficie(ax, xs, ys, Z, nome)
    plt.tight_layout()
    plt.savefig("comparacao_superficies.png", dpi=130)
    plt.close()

    # --- Superfície final (Abordagem A: trapmf + centroide)
    nome_final = "Abordagem A: Centroide + trapmf"
    xs, ys, Z = superficie(sims[nome_final], n=51)
    fig = plt.figure(figsize=(8, 6.5))
    ax = fig.add_subplot(111, projection="3d")
    s = plot_superficie(ax, xs, ys, Z, "Superfície de Decisão — Urgência (Mamdani, trapmf + centroide)")
    fig.colorbar(s, shrink=0.6, label="Urgência (%)")
    plt.tight_layout()
    plt.savefig("superficie_decisao.png", dpi=150)
    plt.close()

    # métrica de suavidade: maior salto entre vizinhos da malha
    print("\nMaior salto entre pontos vizinhos da malha (41x41):")
    for nome, Z in zs.items():
        salto = max(np.abs(np.diff(Z, axis=0)).max(), np.abs(np.diff(Z, axis=1)).max())
        print(f"  {nome:42s} {salto:6.2f}   [min={Z.min():.2f}, max={Z.max():.2f}]")

    # --- Extra: calibração linear da saída (Centroide + trapmf)
    Z = zs["Abordagem A: Centroide + trapmf"]
    z0, z1 = Z[0, 0], Z[-1, -1]
    Zc = (Z - z0) / (z1 - z0) * 100
    salto = max(np.abs(np.diff(Zc, axis=0)).max(), np.abs(np.diff(Zc, axis=1)).max())
    print(f"\nCalibração linear (A): (0,0)={Zc[0,0]:.2f} (100,10)={Zc[-1,-1]:.2f} "
          f"(50,5)={Zc[20,20]:.2f} maior salto={salto:.2f}")
