# main.py
import queries
import popular_banco
import mysql.connector
from config import DB_CONFIG
import sys # Importar a biblioteca sys

def connect_to_database():
    """ Conecta-se ao MySQL e cria o banco de dados se não existir. """
    try:
        print("Iniciando conexão com o banco de dados.")
        conn_params_no_db = DB_CONFIG.copy()
        del conn_params_no_db['database']
        
        conn = mysql.connector.connect(**conn_params_no_db)
        cursor = conn.cursor()
        
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        cursor.execute(f"USE {DB_CONFIG['database']}")
        
        cursor.close()
        print("Conexão estabelecida e banco de dados 'hospital' selecionado.")
        return conn
    except mysql.connector.Error as e:
        print(f"Erro ao conectar com o banco de dados: {e}")
        return None

def setup_database(conn):
    """ Cria tabelas, dados estáticos, índices e triggers. """
    queries.create_tables(conn)
    queries.populate_db(conn)
    queries.create_indices(conn)
    queries.create_triggers(conn)
    print("Banco de dados configurado com sucesso (Tabelas, Índices, Triggers).")

def populate_database_randomly(conn, num_pacientes, consultas_por_paciente):
    """ Popula o banco com dados aleatórios de pacientes e consultas. """
    print("\nIniciando inserção de dados aleatórios...")
    popular_banco.insert_random_pacientes(conn, num_pacientes)
    popular_banco.generate_random_consultas(conn, consultas_por_paciente)
    print("\nBanco de dados populado com dados aleatórios com sucesso!")

if __name__ == "__main__":
    conn = None
    try:
        conn = connect_to_database()
        if conn:
            # 1. Configura a estrutura do banco
            setup_database(conn)
            
            # 2. Define a volumetria e popula com dados aleatórios
            n_pacientes = 50000
            consultas_por_paciente = 10
            populate_database_randomly(conn, n_pacientes, consultas_por_paciente)
            
    except Exception as e:
        # --- CORREÇÃO ---
        # Interrompe a execução em caso de erro fatal
        print(f"\n--- ERRO FATAL ---")
        print(f"A execução foi interrompida devido a um erro durante a configuração.")
        print(f"ERRO: {e}")
        sys.exit(1) # Sai do programa com um código de erro
        
    finally:
        if conn and conn.is_connected():
            conn.close()
            print("Conexão com o banco de dados fechada.")