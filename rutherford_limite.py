import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import matplotlib.cm as cm

# 1. Configuration de la figure
fig, ax = plt.subplots(figsize=(7, 7))
ax.set_xlim(-1.3, 1.3)
ax.set_ylim(-1.3, 1.3)
ax.set_aspect('equal')
ax.grid(True, linestyle=':', alpha=0.5)

# Tracer le noyau au centre
ax.scatter(0, 0, color="red", s=300, label="Noyau (Proton)", zorder=5)

# Trajectoire de l'électron (la spirale noire)
trajectoire_line, = ax.plot([], [], color="black", linestyle="-", linewidth=1.5, alpha=0.6, label="Trajectoire de l'électron")
# L'électron
electron_plot = ax.scatter([], [], color="darkblue", s=100, label="Électron (-)", zorder=6)

# Le photon
photon_plot, = ax.plot([], [], marker="o", markersize=10, linestyle="None", label="Photon émis")

# Initialiser le texte dynamique à côté du photon
photon_text = ax.text(0, 0, "", fontsize=9, fontweight="bold", zorder=7)

ax.legend(loc="upper right")

# Variables pour suivre l'historique et l'état du photon
x_trajectoire, y_trajectoire = [], []
photon_state = {"active": False, "x": 0, "y": 0, "dx": 0, "dy": 0, "age": 0, "color": "red", "wl": 700}

# 2. Fonction pour déterminer la couleur et la longueur d'onde (λ) selon le rayon
def get_photon_properties(rayon):
    # Mapping physique simplifié :
    # Grand rayon = basse fréquence = grande longueur d'onde (Rouge : ~700 nm)
    # Petit rayon = haute fréquence = petite longueur d'onde (Violet : ~400 nm)
    wl = 400 + (rayon - 0.1) / 0.9 * 300
    wl = np.clip(wl, 380, 750) # Limites du spectre visible
    
    # Palette "turbo" inversée pour correspondre au spectre (Rouge en haut, Bleu/Violet en bas)
    cmap = cm.get_cmap('turbo')
    val = (wl - 380) / (750 - 380) # 0 = Violet/Bleu, 1 = Rouge
    
    return cmap(val), int(wl)

# 3. Fonction de mise à jour appelée à chaque frame
def update(frame):
    angle = frame * 0.15
    rayon = np.exp(-0.012 * frame)
    
    # Arrêt si l'électron percute le noyau
    if rayon < 0.05:
        rayon = 0.05
        ax.set_title("Effondrement total ! L'atome classique s'est écrasé.", color="darkred", fontsize=11, fontweight='bold')
    else:
        ax.set_title("L'effondrement du modèle classique", fontsize=11, fontweight='bold')

    # Position actuelle de l'électron
    x = rayon * np.cos(angle)
    y = rayon * np.sin(angle)
    
    # Mise à jour de l'électron et de sa trajectoire
    x_trajectoire.append(x)
    y_trajectoire.append(y)
    trajectoire_line.set_data(x_trajectoire, y_trajectoire)
    electron_plot.set_offsets([[x, y]])
    
    # --- Gestion de l'éjection de la boule et du texte ---
    if frame % 25 == 0 and not photon_state["active"] and rayon > 0.05:
        photon_state["active"] = True
        photon_state["x"] = x
        photon_state["y"] = y
        
        # Calcul de la couleur et de la longueur d'onde réelle en nanomètres
        color, wl = get_photon_properties(rayon)
        photon_state["color"] = color
        photon_state["wl"] = wl
        
        # Direction du déplacement
        norme = np.sqrt(x**2 + y**2)
        photon_state["dx"] = (x / norme) * 0.04
        photon_state["dy"] = (y / norme) * 0.04
        photon_state["age"] = 0

    # Si la boule de lumière se déplace
    if photon_state["active"]:
        photon_state["x"] += photon_state["dx"]
        photon_state["y"] += photon_state["dy"]
        photon_state["age"] += 1
        
        # Mettre à jour la position du point jaune/coloré
        photon_plot.set_data([photon_state["x"]], [photon_state["y"]])
        photon_plot.set_color(photon_state["color"])
        
        # Mettre à jour le texte à côté du photon (décalé de +0.05 sur l'axe X/Y pour la lisibilité)
        photon_text.set_position((photon_state["x"] + 0.05, photon_state["y"] + 0.05))
        photon_text.set_text(f"{photon_state['wl']} nm")
        photon_text.set_color(photon_state["color"])
        
        # Disparition après 20 frames
        if photon_state["age"] > 20 or np.abs(photon_state["x"]) > 1.3:
            photon_state["active"] = False
            photon_plot.set_data([], [])
            photon_text.set_text("")
    else:
        photon_plot.set_data([], [])
        photon_text.set_text("")

    return trajectoire_line, electron_plot, photon_plot, photon_text

# 4. Lancement de l'animation
ani = animation.FuncAnimation(
    fig, update, frames=300, blit=True, interval=30, repeat=False
)

plt.show()
