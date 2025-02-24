#databasebuilder
import pandas as pd
import mysql.connector

DB_CONFIG = {
    "host": "192.168.0.79",
    "user": "delectabowl",      
    "password": "D3lectabowl!*", 
    "database": "recipe_recommendation"      
}

# Connect to MySQL
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

def load_csv_to_mysql(csv_file, table_name, columns=None):
    df = pd.read_csv(csv_file)

    # Keep only relevant columns
    if columns:
        df = df[columns]

    # Replace NaN with NULL for SQL
    df = df.where(pd.notnull(df), None)

    # Insert data row by row
    placeholders = ", ".join(["%s"] * len(df.columns))
    columns_str = ", ".join(df.columns)
    sql = f"INSERT IGNORE INTO {table_name} ({columns_str}) VALUES ({placeholders})"
    
    cursor.executemany(sql, df.values.tolist())
    conn.commit()
    print(f"Loaded data into {table_name}")

# 🔹 Load Data into MySQL (Update File Paths)
load_csv_to_mysql("dataset/interactions_train.csv", "interactions_train", columns=["user_id", "recipe_id", "rating", "date"])
load_csv_to_mysql("dataset/interactions_test.csv", "interactions_test", columns=["user_id", "recipe_id", "rating", "date"])
load_csv_to_mysql("dataset/interactions_validation.csv", "interactions_validation", columns=["user_id", "recipe_id", "rating", "date"])
load_csv_to_mysql("dataset/RAW_recipes.csv", "recipes", columns=["recipe_id", "name", "minutes", "contributor_id", "submitted", "tags", "nutrition", "steps", "description", "n_steps", "n_ingredients"])

# Extract Unique Users and Insert into `users` Table
print("🔹 Extracting unique users...")
df_users = pd.concat([
    pd.read_csv("dataset/interactions_train.csv")[["user_id"]],
    pd.read_csv("dataset/interactions_test.csv")[["user_id"]],
    pd.read_csv("dataset/interactions_validation.csv")[["user_id"]]
]).drop_duplicates()

load_csv_to_mysql(df_users, "users")

# Close MySQL Connection
cursor.close()
conn.close()
print("donezo")