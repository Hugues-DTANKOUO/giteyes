# GitEyes

Bienvenue dans **GitEyes** - Transformez la documentation GitHub en une expérience de lecture interactive semblable à un livre !

GitEyes est un projet éducatif qui offre une interface épurée et sans distraction pour parcourir, lire et interagir avec la documentation hébergée sur des dépôts GitHub. C'est parfait pour étudier des bases de code et de la documentation technique avec une lisibilité améliorée.

![Logo GitEyes](/src/giteyes/static/images/giteyes-logo.svg)

## 📚 Aperçu du Projet

GitEyes propose :

- **Transformation du Contenu GitHub :** Conversion de la documentation des dépôts en format livre lisible
- **Navigation Arborescente :** Navigation intuitive à travers les structures de fichiers des dépôts
- **Rendu Markdown :** Rendu élégant des fichiers markdown avec coloration syntaxique
- **Fonctionnalité de Recherche :** Trouvez du contenu spécifique à travers plusieurs dépôts
- **Marque-pages :** Enregistrez votre documentation préférée pour un accès rapide
- **Mode Sombre/Clair :** Basculez entre les modes de lecture pour un confort visuel optimal

## 🌟 Exemple Concret

Essayez de consulter cette ressource populaire d'Ingénierie des Données avec GitEyes pour une expérience de lecture plus confortable :

[Data Engineering Cookbook par Andreas Kretz](http://127.0.0.1:8000/andkret/Cookbook/blob/master/README.md)

## ⚙️ Implémentation Actuelle

1. **Fonctionnalités Principales :**
   - Analyse des dépôts et extraction de contenu
   - Navigation hiérarchique de la documentation
   - Conversion Markdown vers HTML avec style amélioré
   - Mode Sombre/Clair pour une lecture confortable
   - Suivi de progression à travers les documents

2. **Interface Web :**
   - Backend FastAPI avec templates Jinja2
   - Design responsive pour la lecture sur ordinateur et mobile
   - Expérience de lecture épurée, sans distraction
   - Taille de police et préférences de lecture personnalisables

## 🛠 Stack Technologique

- **Backend :**
  - Python 3.10+
  - FastAPI pour le framework web
  - Bibliothèque Requests pour les opérations HTTP
  - BeautifulSoup pour l'analyse HTML (si nécessaire)

- **Frontend :**
  - HTML/CSS pour la mise en page et le style
  - JavaScript pour l'interactivité
  - Markdown-it pour le rendu
  - Highlight.js pour la coloration syntaxique du code

- **Outils de Développement :**
  - Poetry pour la gestion des dépendances
  - Ruff pour le linting
  - MyPy pour la vérification des types

## 🚀 Démarrage

### 1. Prérequis
Vous avez besoin de Python 3.10 ou ultérieur et Poetry. Installez Poetry avec :
```bash
curl -sSL https://install.python-poetry.org | python3
```

### 2. Cloner le Dépôt
```bash
git clone https://github.com/Hugues-DTANKOUO/giteyes.git
cd giteyes
```

### 3. Installer les Dépendances
```bash
poetry install
```

### 4. Configuration (Optionnel)
Pour personnaliser le comportement de l'application :
```bash
# La configuration se fait via des variables d'environnement
export GITEYES_DEBUG=True  # Activer le mode débogage
```

### 5. Serveur de Développement
Démarrez le serveur de développement local :
```bash
poetry run server
```

### 6. Accès Local
Visitez [http://127.0.0.1:8000](http://127.0.0.1:8000) dans votre navigateur.

## 📂 Fonctionnalités Clés

1. **Explorateur de Dépôts**
   - Parcourez les dépôts et leur structure de répertoires
   - Filtrez par types de fichiers et répertoires
   - [Voir l'Implémentation](/src/giteyes/explorer.py)

2. **Rendu de Contenu**
   - Rendu Markdown avec coloration syntaxique
   - Support des images et diagrammes
   - [Voir l'Implémentation](/src/giteyes/renderer.py)

3. **Moteur de Recherche**
   - Recherche en texte intégral dans la documentation
   - Navigation rapide vers les résultats de recherche
   - [Voir l'Implémentation](/src/giteyes/search.py)

4. **Préférences Utilisateur**
   - Expérience de lecture personnalisable
   - Suivi de l'historique et marque-pages
   - [Voir l'Implémentation](/src/giteyes/preferences.py)

## 🤝 Contribuer

Les contributions sont les bienvenues ! Consultez notre [Guide de Contribution](CONTRIBUTING.md) pour des détails sur :
- Configuration du projet
- Flux de travail de développement
- Directives de style de code
- Exigences de test

Façons de contribuer :
- Amélioration de l'analyse des dépôts
- Amélioration de l'expérience de lecture
- Expansion des types de contenu supportés
- Ajout de capacités de recherche
- Correction de bugs

## 🧑‍💻 À propos de l'Auteur

Maintenu par **Hugues Dtankouo**, un Développeur Full Stack Senior avec une vaste expérience en Python.

📧 **Contact :** [huguesdtankouo@gmail.com](mailto:huguesdtankouo@gmail.com)  
🔗 **LinkedIn :** [Hugues Dtankouo](https://www.linkedin.com/in/dtankouo)  
🔗 **GitHub :** [Hugues-DTANKOUO](https://github.com/Hugues-DTANKOUO)  

## 📄 Licence & Documentation

- **Licence :** [Licence MIT](LICENSE)
- **Journal des Modifications :** [CHANGELOG.md](CHANGELOG.md)

## 🚧 État du Projet

Il s'agit d'un projet en phase initiale avec des fonctionnalités de base implémentées. Les plans futurs incluent :
- Authentification utilisateur pour les dépôts privés
- Mode de lecture hors ligne
- Recherche avancée de contenu
- Version application mobile
- Annotations et surlignages communautaires

Les contributions et retours d'expérience sont grandement appréciés !

## 🎯 Focus Actuel

Le projet se concentre actuellement sur :
1. Amélioration de l'algorithme d'analyse pour différentes structures de dépôts
2. Amélioration de l'interface de lecture
3. Ajout de plus d'extraction de métadonnées
4. Support de plus de types de contenu au-delà du Markdown