import time
import mysql.connector

def search_patient_by_cpf(conn, cpf):
    """
    Busca um paciente pelo CPF diretamente no banco de dados para maior eficiência.

    Args:
        conn: Objeto de conexão com o banco de dados.
        cpf: O CPF do paciente a ser buscado.

    Returns:
        Uma lista de tuplas contendo os dados do paciente encontrado, ou uma lista vazia.
    """
    cursor = conn.cursor()
    query = "SELECT * FROM paciente WHERE CPF = %s"
    cursor.execute(query, (cpf,))
    result = cursor.fetchall()
    cursor.close()
    return result

def search_consulta(conn, patient_id=None, date=None, crm=None):
    """
    Busca consultas com base em filtros opcionais.

    Args:
        conn: Objeto de conexão com o banco de dados.
        patient_id (int, optional): ID do paciente.
        date (str, optional): Data da consulta (formato 'YYYY-MM-DD').
        crm (int, optional): CRM do médico.

    Returns:
        Uma lista de tuplas com os resultados da busca.
    """
    cursor = conn.cursor()
    query = "SELECT * FROM hospital.consulta WHERE 1=1"
    params = []
    
    if patient_id:
        query += " AND IdPac = %s"
        params.append(patient_id)
    if date:
        query += " AND Data = %s"
        params.append(date)
    if crm:
        query += " AND CRM = %s"
        params.append(crm)
        
    start_time = time.time()
    cursor.execute(query, tuple(params))
    result = cursor.fetchall()
    end_time = time.time()
    
    cursor.close()
    
    print(f"Tempo de execução da busca de consulta: {end_time - start_time:.6f} segundos")
    return result

def insert_consulta(conn, crm, idpac, idesp, data, horaincon, horafimcon, formapgto):
    """
    Insere uma nova consulta, buscando os dados desnormalizados para preencher a tabela.

    Args:
        conn: Objeto de conexão com o banco de dados.
        (outros args): Dados da consulta.
    """
    cursor = conn.cursor()

    try:
        # Buscar nome do médico
        cursor.execute("SELECT NomeM FROM medico WHERE CRM = %s", (crm,))
        nome_m = cursor.fetchone()[0]

        # Buscar nome da especialidade
        cursor.execute("SELECT NomeE FROM especialidade WHERE idEsp = %s", (idesp,))
        nome_e = cursor.fetchone()[0]

        # Buscar nome e idade do paciente
        cursor.execute("SELECT NomePac, Idade FROM paciente WHERE idpaciente = %s", (idpac,))
        result = cursor.fetchone()
        nome_paciente, idade_paciente = result if result else ("", None)

        # Inserir consulta com os dados completos
        query = """
        INSERT INTO hospital.consulta
        (CRM, IdPac, IdEsp, Data, HoraInCon, HoraFimCon, FormaPgto, NomeM, NomeE, NomePaciente, IdadePaciente)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            crm, idpac, idesp, data, horaincon, horafimcon, formapgto,
            nome_m, nome_e, nome_paciente, idade_paciente
        ))
        conn.commit()
    except mysql.connector.Error as e:
        conn.rollback()
        print(f"Erro ao inserir consulta: {e}")
        raise
    finally:
        cursor.close()
                    
def insert_patient(conn, nomepac, cpf, idade, sexo, telefonepac, endereco):
    """Insere um novo paciente no banco de dados."""
    cursor = conn.cursor()
    query = """
    INSERT INTO hospital.paciente (NomePac, CPF, Idade, Sexo, TelefonePac, Endereco)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    start_time = time.time()
    cursor.execute(query, (nomepac, cpf, idade, sexo, telefonepac, endereco))
    conn.commit()
    end_time = time.time()
    cursor.close()
    print(f"Tempo de execução da inserção de paciente: {end_time - start_time:.6f} segundos")

def delete_consulta(conn, idconsulta):
    """Deleta uma consulta do banco de dados pelo seu ID."""
    cursor = conn.cursor()
    query = "DELETE FROM hospital.consulta WHERE idconsulta = %s"
    
    start_time = time.time()
    cursor.execute(query, (idconsulta,))
    conn.commit()
    end_time = time.time()
    
    cursor.close()
    
    print(f"Tempo de execução da exclusão: {end_time - start_time:.6f} segundos")

def update_consulta_field(conn, idconsulta, field, value):
    """
    Atualiza um campo específico de uma consulta com validação para prevenir SQL Injection.
    """
    allowed_fields = ["Data", "HoraInCon", "HoraFimCon", "FormaPgto"]
    if field not in allowed_fields:
        raise ValueError(f"Campo '{field}' não é permitido para atualização.")

    cursor = conn.cursor()

    query = f"UPDATE hospital.consulta SET {field} = %s WHERE idconsulta = %s"
    
    start_time = time.time()
    cursor.execute(query, (value, idconsulta))
    conn.commit()
    end_time = time.time()
    
    cursor.close()
    
    print(f"Tempo de execução da atualização: {end_time - start_time:.6f} segundos")

def search_all_consults_by_cpf_normalizada(conn, cpf):
    """
    Busca todas as consultas de um paciente pelo CPF, juntando tabelas para obter dados completos.
    """
    cursor = conn.cursor()
    query = """
    SELECT c.idconsulta, p.NomePac, m.NomeM, c.Data, m.CRM, e.NomeE
    FROM hospital.consulta c
    JOIN hospital.paciente p ON c.IdPac = p.idpaciente
    JOIN hospital.medico m ON c.CRM = m.CRM
    JOIN hospital.especialidade e ON c.IdEsp = e.idEsp
    WHERE p.CPF = %s
    """
    
    start_time = time.time()
    cursor.execute(query, (cpf,))
    result = cursor.fetchall()
    end_time = time.time()
    
    cursor.close()
    
    print(f"Tempo de execução da busca de histórico: {end_time - start_time:.4f} segundos")
    return result

def get_medicos(conn):
    """Retorna uma lista de todos os médicos (CRM, NomeM)."""
    cursor = conn.cursor()
    cursor.execute("SELECT CRM, NomeM FROM medico ORDER BY NomeM")
    medicos = cursor.fetchall()
    cursor.close()
    return medicos

def get_especialidades(conn):
    """Retorna uma lista de todas as especialidades (idEsp, NomeE)."""
    cursor = conn.cursor()
    cursor.execute("SELECT idEsp, NomeE FROM especialidade ORDER BY NomeE")
    especialidades = cursor.fetchall()
    cursor.close()
    return especialidades