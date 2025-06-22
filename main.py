import queries, queriesMenu, popular_banco
import mysql.connector

def connect_to_database():
    try:
        print("Starting connection to database.")
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="bd123!"
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS hospital")
        cursor.execute("USE hospital")
        cursor.close()
        print("Everything set!")
        return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def criar_tabelas(conn):
    try:
        queries.create_tables(conn)
        queries.populate_db(conn)  # Popula dados estáticos
        print("Database created and populated successfully!")
    except Exception as e:
        print(f"Error creating tables or populating database: {e}")

def popular_banco_aleatoriamente(conn, n_pacientes, consultas_por_paciente):
    try:
        popular_banco.insert_random_pacientes(conn, n_pacientes)
        popular_banco.generate_random_consultas(conn, consultas_por_paciente)
    except Exception as e:
        print(f"Error populating database randomly: {e}")

if __name__ == "__main__":
    conn = connect_to_database()
    if conn:
        criar_tabelas(conn)
        
        # CONTROLE CENTRALIZADO DA VOLUMETRIA
        n_pacientes = 50000            # Pacientes
        consultas_por_paciente = 10     # Consultas por paciente
        
        popular_banco_aleatoriamente(conn, n_pacientes, consultas_por_paciente)
        conn.close()