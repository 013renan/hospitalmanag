import os

def check_database(conn):
    cursor = None
    try:
        cursor = conn.cursor()
        query = open(os.path.join('queries', 'database_check.sql')).read()
        cursor.execute(query)
        rows = cursor.fetchall()  # Consumir TODOS os resultados
        if rows and rows[0][0] == 1:
            print("Database is working")
        else:
            print("Database is not working")
    except Exception as e:
        print(f"Error checking database: {e}")
    finally:
        if cursor:
            cursor.close()

def create_tables(conn):
    cursor = None
    try:
        cursor = conn.cursor()
        # Tratar cada comando separadamente
        with open(os.path.join('queries', 'create_tables.sql'), 'r') as file:
            query = file.read()
            
        # Dividir em comandos separados por ponto e vírgula
        commands = query.split(';')
        
        for command in commands:
            command = command.strip()
            if command:  # Ignora strings vazias
                try:
                    cursor.execute(command)
                except Exception as e:
                    print(f"Error executing command: {command[:50]}... - {e}")
                    raise
        
        conn.commit()
        print("Tables Created!")
    except Exception as e:
        conn.rollback()
        print(f"Error creating tables: {e}")
        raise
    finally:
        if cursor:
            cursor.close()

def populate_db(conn):
    cursor = None
    try:
        cursor = conn.cursor()
        # Abordagem similar à função create_tables
        with open(os.path.join('queries', 'populate_db.sql'), 'r') as file:
            query = file.read()
            
        commands = query.split(';')
        
        for command in commands:
            command = command.strip()
            if command:
                try:
                    cursor.execute(command)
                except Exception as e:
                    print(f"Error executing command: {command[:50]}... - {e}")
                    raise
        
        conn.commit()
        print("Tables Populated!")
    except Exception as e:
        conn.rollback()
        print(f"Error populating database: {e}")
        raise
    finally:
        if cursor:
            cursor.close()

def erase_db(conn):
    cursor = None
    try:
        cursor = conn.cursor()
        with open(os.path.join('queries', 'erase_db.sql'), 'r') as file:
            query = file.read()
            
        commands = query.split(';')
        
        for command in commands:
            command = command.strip()
            if command:
                cursor.execute(command)
                
        conn.commit()
        print("All data deleted!")
    except Exception as e:
        conn.rollback()
        print(f"Error erasing database: {e}")
    finally:
        if cursor:
            cursor.close()

def fetch_somente_dermatologistas(conn):
    cursor = conn.cursor()
    query = open(os.path.join('queries', 'fetch_somente_dermatologistas.sql')).read()

    cursor.execute(query)
    rows = cursor.fetchall()
    print(rows)



def fetch_especialista_completo(conn):
    cursor = conn.cursor()
    query = open(os.path.join('queries', 'fetch_especialista_completo.sql')).read()

    cursor.execute(query)
    rows = cursor.fetchall()
    print(rows)


def fetch_consultas_house_cardiologia(conn):
    cursor = conn.cursor()
    query = open(os.path.join('queries', 'fetch_consultas_house_cardiologia.sql')).read()

    cursor.execute(query)
    rows = cursor.fetchall()
    print(rows)


def criar_indices(conn):
    cursor = conn.cursor()
    query = open(os.path.join('queries', 'criar_indices.sql')).read()
    cursor.execute(query)

def droppar_indices(conn):
    cursor = conn.cursor()
    query = open(os.path.join('queries', 'droppar_indices.sql')).read()
    cursor.execute(query)

def criar_tabela_nao_normalizada(conn):
    cursor = conn.cursor()
    query = open(os.path.join('queries', 'create_table_nao_normalizada.sql')).read()
    cursor.execute(query)

