# My Todo App with FastAPI and MongoDB

## Description

Ce projet est une application de gestion de tâches (Todo) développée avec FastAPI, un framework web moderne et rapide pour Python, et MongoDB, une base de données NoSQL flexible et scalable. L'application permet de créer, lire, mettre à jour et supprimer des tâches Todo, offrant ainsi une gestion complète des tâches.

## Fonctionnalités

- **Création de tâches (POST /todos)** : Permet aux utilisateurs de créer de nouvelles tâches avec un titre et un état d'avancement.
- **Lecture de toutes les tâches (GET /todos)** : Récupère et affiche la liste de toutes les tâches enregistrées.
- **Lecture d'une tâche par ID (GET /todos/{id})** : Récupère et affiche les détails d'une tâche spécifique en utilisant son identifiant unique.
- **Mise à jour de tâches (PUT /todos/{id})** : Permet aux utilisateurs de mettre à jour le titre et l'état d'avancement d'une tâche spécifique.
- **Suppression de tâches (DELETE /todos/{id})** : Permet aux utilisateurs de supprimer une tâche spécifique de la base de données.

## Technologies Utilisées

- **FastAPI** : Framework web moderne et performant pour développer des APIs avec Python.
- **MongoDB** : Base de données NoSQL flexible et scalable pour le stockage des tâches.
- **Motor** : Driver asynchrone pour MongoDB, permettant une communication efficace avec la base de données.
- **Pydantic** : Utilisé pour la validation et la sérialisation des données, garantissant l'intégrité des données échangées via l'API.
- **Uvicorn** : Serveur ASGI rapide pour servir l'application FastAPI.

## Prérequis

- Python 3.9+
- MongoDB en cours d'exécution (localement ou dans un conteneur)
- `poetry` pour la gestion des dépendances

## Installation

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/votre-utilisateur/my-todo-app.git
   cd my-todo-app

2. Installer les dépendances :
    ```bash
    poetry install

3. Configurez les variables d'environnement en créant un fichier .env à la racine du projet :
   ```bash
   MONGO_INITDB_ROOT_USERNAME=root
   MONGO_INITDB_ROOT_PASSWORD=mySecureDbPassword1
   MONGO_URI=mongodb://root:mySecureDbPassword1@localhost:27017/

## Utilisation

1. Démarrez l'application FastAPI :
 ```bash
poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --log-level debug --reload
  ```
2. Accédez à la documentation interactive de l'API :

  Ouvrez votre navigateur et accédez à http://localhost:8000/docs pour utiliser l'interface Swagger UI et tester les différents endpoints de l'API.


   
