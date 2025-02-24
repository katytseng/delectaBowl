# SQL Connector and Database Table Setup
import mysql.connector
import pandas as pd

# Database Configuration
DB_CONFIG = {
    "host": "192.168.0.79",
    "user": "delectabowl",      
    "password": "D3lectabowl!*", 
    "database": "recipe_recommendation"      
}

# Connect to MySQL
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# Create Tables
TABLES = {
    "users": """
        CREATE TABLE IF NOT EXISTS users (
            user_id INT PRIMARY KEY
        );
    """,

    "recipes": """
        CREATE TABLE IF NOT EXISTS recipes (
            recipe_id INT PRIMARY KEY,
            name TEXT,
            minutes INT,
            contributor_id INT,
            submitted TEXT,
            tags TEXT,
            nutrition TEXT,
            steps TEXT,
            description TEXT,
            n_steps INT,
            n_ingredients INT
        );
    """,
    
    "interactions_train": """
        CREATE TABLE IF NOT EXISTS interactions_train (
            user_id INT,
            recipe_id INT,
            rating FLOAT,
            date TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id)
        );
    """,

    "interactions_test": """
        CREATE TABLE IF NOT EXISTS interactions_test (
            user_id INT,
            recipe_id INT,
            rating FLOAT,
            date TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id)
        );
    """,

    "interactions_validation": """
        CREATE TABLE IF NOT EXISTS interactions_validation (
            user_id INT,
            recipe_id INT,
            rating FLOAT,
            date TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id)
        );
    """,
    "ingredients": """
    CREATE TABLE IF NOT EXISTS ingredients (
    ingredient_id INT PRIMARY KEY,
    raw_ingr TEXT,
    processed TEXT,
    replaced TEXT
);
""",
    "recipe_ingredients": """
        CREATE TABLE IF NOT EXISTS recipe_ingredients (
            recipe_id INT,
            ingredient_id INT,
            FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id),
            FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id)
        );
    """

}

# Execute Table Creation
for table_name, table_sql in TABLES.items():
    cursor.execute(table_sql)
    print(f"Created table: {table_name}")

conn.commit()

