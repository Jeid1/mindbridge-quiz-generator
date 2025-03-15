# Générateur de Quiz Multilingue

Ce projet est un générateur de quiz qui permet de créer des questions dans différentes langues (Français, Arabe, Anglais) et différents formats (choix multiples, vrai/faux, questions ouvertes).

## Configuration de l'environnement

1. Créez un environnement virtuel Python :
```bash
python -m venv venv
```

2. Activez l'environnement virtuel :
- Windows :
```bash
.\venv\Scripts\activate
```
- Linux/MacOS :
```bash
source venv/bin/activate
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

4. Configuration des variables d'environnement :
Créez un fichier `.env` à la racine du projet et ajoutez votre clé API OpenAI :
```
OPENAI_API_KEY=votre_clé_api
```

## Structure du projet

- `quiz_templates_multiple_lang.py` : Contient les templates pour générer des quiz dans différentes langues
- Les templates supportent :
  - Questions à choix multiples
  - Questions vrai/faux
  - Questions ouvertes
  - Support multilingue (FR, AR, EN)

## Utilisation

Le projet utilise LangChain pour générer des quiz personnalisés basés sur un contexte donné. 