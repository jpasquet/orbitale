import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# 1. Configuration de l'orbite
rayon_orbite = 1.0
theta_orbite = np.linspace(0, 2 * np.pi, 200)
x_orbite = rayon_orbite * np.cos(theta_orbite)
y_orbite = rayon_orbite * np.sin(theta_orbite)

# 2. Initialisation de la figure
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal')
ax.grid(True, linestyle=':', alpha=0.6)
ax.set_title("Animation du Modèle de Rutherford : Hydrogène", fontsize=12, fontweight='bold')

# Tracer les éléments fixes
ax.plot(x_orbite, y_orbite, color="blue", linestyle="--", linewidth=1.5, label="Orbite")
ax.scatter(0, 0, color="red", s=300, label="Noyau (Proton)", zorder=3)

# Initialiser l'élément mobile (l'électron)
electron_plot = ax.scatter([], [], color="darkblue", s=100, label="Électron", zorder=4)
ax.legend(loc="upper right")

# 3. Fonction d'initialisation de l'animation
def init():
    electron_plot.set_offsets(np.empty((0, 2)))
    return electron_plot,

# 4. Fonction de mise à jour (appelée à chaque image / frame)
def update(frame):
    # Calcul de l'angle en fonction du numéro de la frame
    angle = frame * 0.05
    x = rayon_orbite * np.cos(angle)
    y = rayon_orbite * np.sin(angle)
    
    # Mettre à jour la position de l'électron
    electron_plot.set_offsets([[x, y]])
    return electron_plot,

# 5. Création et lancement de l'animation
# frames=126 permet de faire un tour complet (2 * pi / 0.05 ≈ 126)
ani = animation.FuncAnimation(
    fig, update, frames=126, init_func=init, blit=True, interval=30, cache_frame_data=False
)

plt.show()
