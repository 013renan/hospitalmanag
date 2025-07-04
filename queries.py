# queries.py

import os
import mysql.connector

def _execute_sql_from_file(conn, file_path):
    """
    Função auxiliar para ler e executar um arquivo SQL que pode conter múltiplos comandos simples.
    """
    cursor = None
    try:
        cursor = conn.cursor()
        with open(file_path, 'r', encoding='utf-8') as file:
            sql_commands = file.read().split(';')

        for command in sql_commands:
            command = command.strip()
            if command:
                try:
                    cursor.execute(command)
                except mysql.connector.Error as e:
                    if e.errno in (1050, 1061, 1304):
                        print(f"Aviso: O objeto do comando '{command[:30]}...' já existe. Pulando.")
                    else:
                        print(f"Erro ao executar comando: {command[:50]}... - {e}")
                        raise
        
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Erro ao processar o arquivo {os.path.basename(file_path)}: {e}")
        raise
    finally:
        if cursor:
            cursor.close()

def create_tables(conn):
    """Cria todas as tabelas necessárias no banco de dados."""
    print("Criando tabelas...")
    file_path = os.path.join('queries', 'create_tables.sql')
    _execute_sql_from_file(conn, file_path)
    print("Tabelas criadas com sucesso!")

def populate_db(conn):
    """Popula o banco com dados estáticos (médicos, especialidades, etc.)."""
    print("Populando banco de dados com dados estáticos...")
    file_path = os.path.join('queries', 'populate_db.sql')
    _execute_sql_from_file(conn, file_path)
    print("Banco de dados populado com sucesso!")

def erase_db(conn):
    """Apaga todos os dados das tabelas do banco."""
    print("Apagando todos os dados do banco...")
    file_path = os.path.join('queries', 'erase_db.sql')
    _execute_sql_from_file(conn, file_path)
    print("Todos os dados foram apagados!")

def create_indices(conn):
    """Cria os índices no banco de dados para otimizar as consultas."""
    print("Criando índices para otimização...")
    file_path = os.path.join('queries', 'create_indices.sql')
    _execute_sql_from_file(conn, file_path)
    print("Índices criados com sucesso!")

def create_triggers(conn):
    """
    Cria os triggers no banco de dados, limpando explicitamente os resultados
    após cada execução para evitar o erro 'Commands out of sync'.
    """
    cursor = None
    try:
        print("Criando triggers para sincronização de dados...")
        cursor = conn.cursor()
        file_path = os.path.join('queries', 'create_triggers.sql')
        
        with open(file_path, 'r', encoding='utf-8') as file:
            delimiter = '--\n--'
            triggers_sql = file.read().split(delimiter)
        
        for trigger_sql in filter(None, [t.strip() for t in triggers_sql]):
            try:
                if trigger_sql.endswith(';'):
                    trigger_sql = trigger_sql[:-1]
                
                cursor.execute(trigger_sql)

            except mysql.connector.Error as e:
                if e.errno == 1304:
                    trigger_name = trigger_sql.split()[2]
                    print(f"Aviso: O trigger '{trigger_name}' já existe. Pulando.")
                else:
                    raise
            
            # --- CORREÇÃO FINAL ---
            # Este loop consome qualquer resultado pendente na conexão,
            # limpando-a para o próximo comando.
            while cursor.nextset():
                pass

        conn.commit()
        print("Triggers criados com sucesso!")
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Erro ao criar triggers: {e}")
        raise
    finally:
        if cursor:
            cursor.close()