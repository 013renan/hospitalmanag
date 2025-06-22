
import random
from datetime import datetime, timedelta

def gerar_pacientes_aleatoriamente(n):
    nomes = ['Diego', 'Ana', 'Joao', 'Maria', 'Carlos', 'Fernanda', 'Luis', 'Paula', 'Pedro', 'Laura']
    sobrenomes = ['Silva', 'Santos', 'Oliveira', 'Pereira', 'Lima', 'Gomes', 'Ribeiro', 'Martins', 'Barbosa', 'Rocha']
    ruas = ['Rua dos Pinheiros', 'Avenida Paulista', 'Rua das Flores', 'Praca da Se', 'Rua Augusta', 'Avenida Brasil']

    pacientes = []
    for i in range(n):
        idpaciente = i
        NomePac = f"{random.choice(nomes)} {random.choice(sobrenomes)}"
        CPF = f"{random.randint(100, 999)}.{random.randint(100, 999)}.{random.randint(100, 999)}-{random.randint(10, 99)}"
        Idade = random.randint(1, 100)
        Sexo = random.choice(['M', 'F'])
        TelefonePac = f"{random.randint(1000000000, 9999999999)}"
        Endereco = f"{random.choice(ruas)}, {random.randint(1, 9999)}"
        print(f"Insert Paciente: {idpaciente}, {NomePac}, {CPF}, {Idade}, {Sexo}, {TelefonePac}, {Endereco}")
        pacientes.append((idpaciente, NomePac, CPF, Idade, Sexo, TelefonePac, Endereco))
    
    return pacientes

def insert_random_pacientes(conn, n):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM hospital.paciente")

    query = """
    INSERT INTO hospital.paciente (idpaciente, NomePac, CPF, Idade, Sexo, TelefonePac, Endereco)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    pacientes = gerar_pacientes_aleatoriamente(n)
    cursor.executemany(query, pacientes)

    conn.commit()

def gerar_dia_util(start, end):
    while True:
        random_date = start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))
        if random_date.weekday() < 5:  # 0 is Monday, 4 is Friday
            return random_date

def generate_random_consultas(conn, n):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM hospital.consulta")
    cursor.execute("DELETE FROM hospital.consulta_detalhada")

    query = """
    INSERT INTO hospital.consulta (CRM, IdPac, IdEsp, Data, HoraInCon, HoraFimCon, FormaPgto)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    start_date = datetime.strptime('2020-01-01', '%Y-%m-%d')
    end_date = datetime.strptime('2023-12-31', '%Y-%m-%d')
    
    for _ in range(n*10):
        try:
            CRM = random.choice(['123456', '789012', '345678'])
            IdPac = random.randint(1, n)
            IdEsp = random.randint(1, 10)
            date = gerar_dia_util(start_date, end_date)
            HoraInCon = (datetime.min + timedelta(minutes=random.randint(0, 1440))).time().strftime('%H:%M:%S')
            HoraFimCon = (datetime.min + timedelta(minutes=random.randint(0, 1440))).time().strftime('%H:%M:%S')
            FormaPgto = random.choice(['Cartao', 'Boleto', 'Dinheiro', '-'])

            params = (CRM, IdPac, IdEsp, date, HoraInCon, HoraFimCon, FormaPgto)
            print(f"Insert Consulta: {CRM}, {IdPac}, {IdEsp}, {date}, {HoraInCon}, {HoraFimCon}, {FormaPgto}")
            cursor.execute(query, params)
            conn.commit()
        except Exception as e:
            print(e)
            continue


    query = """
    INSERT INTO hospital.consulta_detalhada (idconsulta, NomePac, CPF, NomeM, Data, CRM, NomeE)
    SELECT c.idconsulta, p.NomePac, p.CPF, m.NomeM, c.Data, m.CRM, e.NomeE
    FROM hospital.consulta c
    JOIN hospital.paciente p ON c.IdPac = p.idpaciente
    JOIN hospital.medico m ON c.CRM = m.CRM
    JOIN hospital.especialidade e ON c.IdEsp = e.idEsp
    """

    cursor.execute(query)
    conn.commit()