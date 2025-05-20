# Intrasub GUI Dive Calculator

Une application graphique pour calculs de plongée technique (GUE, Nitrox, Trimix, SAC, Gas Matching) avec interface moderne en Tkinter (noir/vert fluo).

## 🌐 Fonctionnalités

* Calcul de la Pression Absolue
* Pression Partielle Oxygène
* Profondeur Max pour un Gaz donné
* Profondeur Equivalente Air (PEA / EAD)
* Surface Air Consumption (SAC)
* Meilleur Nitrox selon profondeur
* Meilleur Trimix avec PEA personnalisable
* Trimix recommandé selon les règles GUE
* Gas Matching entre 2 plongeurs

## ⚙️ Prérequis

* Python 3.x
* Tkinter (inclus par défaut dans Python standard)

## 📚 Installation

Cloner le repo ou télécharger le fichier `intrasub_gui.py`, puis exécutez :

```bash
python intrasub_gui.py
```

## 📆 Créer un exécutable Windows

1. Installer PyInstaller :

```bash
pip install pyinstaller
```

2. Générer le .exe :

```bash
pyinstaller --onefile --noconsole intrasub_gui.py
```

3. L'exécutable sera créé dans le dossier `dist/`.

## 🚀 Distribution

Vous pouvez partager le fichier `.exe` avec d'autres plongeurs sans qu'ils aient besoin de Python.

## 👋 Auteur

Ce projet a été conçu pour les plongeurs TEC soucieux de bien préparer leurs plongées.

---

Bonnes plongées et soyez prudents ! ⛵️🐟🚀
