import mysql.connector
import time

def connect_to_database():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="bd123!",
        database="hospital"
    )
    return conn

def search_patient_by_cpf(cpf):
    conn = connect_to_database()
    cursor = conn.cursor()
    # Busca todos os CPFs e compara limpo
    query = "SELECT * FROM paciente"
    cursor.execute(query)
    pacientes = cursor.fetchall()
    conn.close()
    
    cpf_limpo = "".join(filter(str.isdigit, str(cpf)))
    for paciente in pacientes:
        cpf_banco = "".join(filter(str.isdigit, str(paciente[2])))  # Supondo que paciente[2] é o CPF
        if cpf_banco == cpf_limpo:
            return [paciente]
    return []


def search_consulta(patient_id=None, date=None, crm=None):
    conn = connect_to_database()
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
    
    conn.close()
    
    print(f"Tempo de execução da consulta: {end_time - start_time:.10f} segundos")
    return result

def insert_consulta(crm, idpac, idesp, data, horaincon, horafimcon, formapgto):
    conn = connect_to_database()
    cursor = conn.cursor()

    # Buscar nome do médico
    cursor.execute("SELECT NomeM FROM medico WHERE CRM = %s", (crm,))
    result = cursor.fetchone()
    nome_m = result[0] if result else ""

    # Buscar nome da especialidade
    cursor.execute("SELECT NomeE FROM especialidade WHERE idEsp = %s", (idesp,))
    result = cursor.fetchone()
    nome_e = result[0] if result else ""

    # Buscar nome e idade do paciente
    cursor.execute("SELECT NomePac, Idade FROM paciente WHERE idpaciente = %s", (idpac,))
    result = cursor.fetchone()
    nome_paciente = result[0] if result else ""
    idade_paciente = result[1] if result else None

    # Inserir consulta com os campos obrigatórios
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
    conn.close()

                    
def insert_patient(nomepac, cpf, idade, sexo, telefonepac, endereco):
    conn = connect_to_database()
    cursor = conn.cursor()
    query = """
    INSERT INTO hospital.paciente (NomePac, CPF, Idade, Sexo, TelefonePac, Endereco)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    start_time = time.time()
    cursor.execute(query, (nomepac, cpf, idade, sexo, telefonepac, endereco))
    conn.commit()
    end_time = time.time()
    conn.close()
    print(f"Tempo de execução da inserção: {end_time - start_time:.10f} segundos")

def delete_consulta(idconsulta):
    conn = connect_to_database()
    cursor = conn.cursor()
    query = "DELETE FROM hospital.consulta WHERE idconsulta = %s"
    
    start_time = time.time()
    cursor.execute(query, (idconsulta,))
    conn.commit()
    end_time = time.time()
    
    conn.close()
    
    print(f"Tempo de execução da exclusão: {end_time - start_time:.10f} segundos")

def update_consulta_field(idconsulta, field, value):
    conn = connect_to_database()
    cursor = conn.cursor()
    query = f"UPDATE hospital.consulta SET {field} = %s WHERE idconsulta = %s"
    
    start_time = time.time()
    cursor.execute(query, (value, idconsulta))
    conn.commit()
    end_time = time.time()
    
    conn.close()
    
    print(f"Tempo de execução da atualização: {end_time - start_time:.10f} segundos")

def search_all_consults_by_cpf_normalizada(cpf):
    conn = connect_to_database()
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
    
    conn.close()
    
    print(f"Tempo de execução da consulta: {end_time - start_time:.4f} segundos")
    return result


def search_all_consults_by_cpf(cpf):
    conn = connect_to_database()
    cursor = conn.cursor()
    query = """
    SELECT idconsulta, NomePac, NomeM, Data, CRM, NomeE,
    FROM hospital.consulta_detalhada
    WHERE CPF = %s
    """
    
    start_time = time.time()
    cursor.execute(query, (cpf,))
    result = cursor.fetchall()
    end_time = time.time()
    
    conn.close()
    
    print(f"Tempo de execução da consulta: {end_time - start_time:.4f} segundos")
    return result

def get_medicos():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT CRM, NomeM FROM medico")
    medicos = cursor.fetchall()
    conn.close()
    return medicos

def get_especialidades():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT idEsp, NomeE FROM especialidade")
    especialidades = cursor.fetchall()
    conn.close()
    return especialidades