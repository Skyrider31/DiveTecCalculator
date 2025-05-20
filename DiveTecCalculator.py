import tkinter as tk
from tkinter import messagebox, simpledialog

DEFAULT_PPO2 = 1.4
DEFAULT_PPO2_DECO = 1.6
DEFAULT_N2 = 0.79

# Couleurs personnalisées
PRIMARY_BG = "#000000"
PRIMARY_FG = "#00FF00"

# Message d'erreur cool
def show_error(msg):
    messagebox.showerror("💥 Oups !", f"⚠️ Une erreur s'est produite:\n\n{msg}\n\n🤿 Replonge et réessaye !")

def safe_askfloat(title, prompt):
    try:
        return simpledialog.askfloat(title, prompt)
    except Exception:
        show_error("Ce champ nécessite un nombre. Essaie avec un chiffre 😉")
        return None

# Calculs de base

def prof_to_pa(depth):
    return depth / 10 + 1

def calc_pp(pa, oxy):
    return pa * oxy

def calc_sac(pa, volume, time, bar):
    return (bar * volume) / time / pa

def calc_ead(pa, oxygen):
    ppn2 = pa * (1 - oxygen)
    return ((ppn2 / DEFAULT_N2) - 1) * 10

def calc_best_nitrox(pa, ppo2_max):
    return (ppo2_max / pa) * 100

def calc_trimix(pa, ppo2=DEFAULT_PPO2, end_pa=None):
    if not end_pa:
        end_pa = prof_to_pa(30)
    fraction_n2 = end_pa / pa
    helium_fraction = 1 - fraction_n2
    oxygen_fraction = min(ppo2 / pa, 0.21)
    if oxygen_fraction + helium_fraction > 1:
        oxygen_fraction = 1 - helium_fraction
    nitrogen_fraction = 1 - helium_fraction - oxygen_fraction
    return int(oxygen_fraction*100), int(helium_fraction*100), int(nitrogen_fraction*100)

# Fonctions d'affichage/calcul utilisateur

def show_info(text):
    messagebox.showinfo("Résultat", text)

def calc_pp_display():
    d = safe_askfloat("Profondeur", "Profondeur (m) ?")
    o2 = safe_askfloat("Oxygène", "% Oxygène ?")
    if d is not None and o2 is not None:
        pa = prof_to_pa(d)
        pp = calc_pp(pa, o2 / 100)
        alert = "\nAttention: dépasse 1.4 bar!" if pp > 1.4 else ""
        show_info(f"PpO2: {pp:.2f} bar{alert}")

def calc_max_depth():
    o2 = safe_askfloat("Oxygène", "% Oxygène ?")
    if o2 is not None:
        nx = o2 / 100
        d1 = ((DEFAULT_PPO2 / nx) - 1) * 10
        d2 = ((DEFAULT_PPO2_DECO / nx) - 1) * 10
        show_info(f"Profondeur max (1.4): {d1:.2f} m\nProfondeur max (1.6): {d2:.2f} m")

def calc_ead_display():
    d = safe_askfloat("Profondeur", "Profondeur ?")
    o2 = safe_askfloat("Oxygène", "% Oxygène ?")
    if d is not None and o2 is not None:
        pa = prof_to_pa(d)
        ead = calc_ead(pa, o2 / 100)
        show_info(f"Profondeur équivalente air: {ead:.2f} m")

def calc_sac_display():
    d = safe_askfloat("Profondeur", "Profondeur ?")
    v = safe_askfloat("Volume", "Volume total de tes bouteilles ?")
    t = safe_askfloat("Temps", "Temps à la profondeur mentionné?")
    b = safe_askfloat("Bar", "Combien de bar consommé ?")
    if None not in (d, v, t, b):
        pa = prof_to_pa(d)
        sac = calc_sac(pa, v, t, b)
        show_info(f"SAC: {sac:.2f} L/min")

def calc_best_nx_display():
    d = safe_askfloat("Profondeur", "Profondeur ?")
    if d is not None:
        pa = prof_to_pa(d)
        nitrox = calc_best_nitrox(pa, DEFAULT_PPO2)
        msg = f"Meilleur Nitrox: {nitrox:.2f}%"
        if nitrox <= 21:
            msg += "\nProfondeur inadaptée au Nitrox"
        show_info(msg)

def calc_meilleur_trimix():
    d = safe_askfloat("Profondeur", "Profondeur de la plongée ?")
    pea = safe_askfloat("PEA", "Profondeur Équivalente Air souhaitée ?")
    if None not in (d, pea):
        pa = prof_to_pa(d)
        end_pa = prof_to_pa(pea)
        o2, he, n2 = calc_trimix(pa, DEFAULT_PPO2, end_pa)
        show_info(f">>>>>>>>>>>> Avec un maximum de 1.4 en PpO2 et une PEA de {pea} m, Il vous faut un Trimix {o2}/{he} TMX <<<<<<<<<<<")

def calc_gue_display():
    d = safe_askfloat("Profondeur", "Profondeur ?")
    if d is not None:
        pa = prof_to_pa(d)
        o2, he, n2 = calc_trimix(pa, 1.2)
        show_info(f"Trimix GUE recommandé:\nOxygène: {o2}%\nHélium: {he}%\nAzote: {n2}%")

def calc_gas_matching():
    vol1 = safe_askfloat("Gas Matching", "Volume bouteille plongeur #1 (Litre) ?")
    bar1 = safe_askfloat("Gas Matching", "Bar plongeur #1 ?")
    vol2 = safe_askfloat("Gas Matching", "Volume plongeur #2 (Litre) ?")
    bar2 = safe_askfloat("Gas Matching", "Bar plongeur #2 ?")

    if None in (vol1, bar1, vol2, bar2):
        return

    litre1 = vol1 * bar1
    litre2 = vol2 * bar2

    if vol1 < vol2:
        besoin_bar = litre2 / 3 / vol1
        tap1 = bar1 - besoin_bar / 2
        tap2 = bar2 - besoin_bar
    elif vol1 > vol2:
        besoin_bar = litre1 / 3 / vol2
        tap1 = bar1 - besoin_bar
        tap2 = bar2 - besoin_bar / 2
    else:
        besoin_bar = litre1 / 3 / vol1
        tap1 = tap2 = bar1 - besoin_bar

    messagebox.showinfo("Résultat Gas Matching",
        f"Plongeur 1 - TAP: {tap1:.2f} BAR\nPlongeur 2 - TAP: {tap2:.2f} BAR")

def create_gui_menu():
    def wrap(f):
        def inner():
            try:
                f()
            except Exception as e:
                show_error(str(e))
        return inner

    root = tk.Tk()
    root.title("Intrasub GUI")
    root.configure(bg=PRIMARY_BG)

    frame = tk.Frame(root, padx=20, pady=20, bg=PRIMARY_BG)
    frame.pack()

    buttons = [
        ("Pression Absolue", wrap(lambda: show_info(f"Pression Absolue: {prof_to_pa(safe_askfloat('Profondeur', 'Profondeur (m) ?')):.2f} bar"))),
        ("Pression Partielle Oxygène", wrap(calc_pp_display)),
        ("Profondeur Max d'un Gaz", wrap(calc_max_depth)),
        ("Profondeur Équivalente Air (PEA/EAD)", wrap(calc_ead_display)),
        ("Calcul SAC", wrap(calc_sac_display)),
        ("Gas Matching", wrap(calc_gas_matching)),
        ("Meilleur Nitrox", wrap(calc_best_nx_display)),
        ("Meilleur Trimix", wrap(calc_meilleur_trimix)),
        ("Trimix GUE", wrap(calc_gue_display)),
        ("Quitter", root.quit)
    ]

    for text, cmd in buttons:
        btn = tk.Button(frame, text=text, command=cmd, width=40, pady=5,
                        bg=PRIMARY_BG, fg=PRIMARY_FG,
                        activebackground="#111", activeforeground="#0f0")
        btn.pack(pady=2)

    root.mainloop()

if __name__ == '__main__':
    create_gui_menu()
