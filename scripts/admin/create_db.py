import mysql.connector
from mysql.connector import errorcode

def create_database():
    try:
        # Connexion sans base de données spécifiée
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        cursor = db.cursor()
        
        # Création de la base de données ghu si elle n'existe pas
        print("Vérification/Création de la base de données 'ghu'...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS ghu DEFAULT CHARACTER SET 'utf8'")
        print("Base de données 'ghu' prête.")
        
        cursor.close()
        db.close()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Erreur : Mauvais utilisateur ou mot de passe.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Erreur : La base de données n'existe pas.")
        else:
            print(f"Erreur : {err}")

if __name__ == "__main__":
    create_database()
