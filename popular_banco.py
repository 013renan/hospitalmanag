import mysql.connector
from faker import Faker
import random
from datetime import datetime, timedelta
import traceback

fake = Faker('pt_BR')

def connect():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="bd123!",
        database="hospital"
    )

def insert_random_pacientes(conn, n):
    cursor = conn.cursor()
    for _ in range(n):
        nome = fake.name()
        cpf = fake.unique.cpf()
        idade = random.randint(1, 99)
        sexo = random.choice(['M', 'F'])
        telefone = fake.msisdn()[:11]
        endereco = fake.street_address()
        try:
            #print(f"Inserindo: {nome}, {cpf}, {idade}, {sexo}, {telefone}, {endereco}")
            cursor.execute(
                "INSERT INTO paciente (NomePac, CPF, Idade, Sexo, TelefonePac, Endereco) VALUES (%s, %s, %s, %s, %s, %s)",
                (nome, cpf, idade, sexo, telefone, endereco)
            )
            #print("Paciente inserido com sucesso")
        except Exception as e:
            print("Erro ao inserir paciente:")
            traceback.print_exc()
    conn.commit()


def generate_random_consultas(conn, consultas_por_paciente=10):
    cursor = conn.cursor()
    # Buscar todos os pares válidos de médico e especialidade
    cursor.execute("""
        SELECT ee.CRM, m.NomeM, ee.idEsp, e.NomeE
        FROM exerce_esp ee
        JOIN medico m ON ee.CRM = m.CRM
        JOIN especialidade e ON ee.idEsp = e.idEsp
    """)
    medico_especialidade = cursor.fetchall()  # Lista de tuplas (CRM, NomeM, idEsp, NomeE)

    cursor.execute("SELECT idpaciente, NomePac, Idade FROM paciente")
    pacientes = cursor.fetchall()
    formas_pgto = ['Dinheiro', 'Cartão', 'Boleto', '-']

    for paciente in pacientes:
        idpac, nomepac, idadepac = paciente
        for _ in range(consultas_por_paciente):
            crm, nomem, idesp, nomee = random.choice(medico_especialidade)
            data = fake.date_between(start_date='-2y', end_date='today')
            hora_inicio = fake.time(pattern="%H:%M:%S")
            hora_fim = (datetime.strptime(hora_inicio, "%H:%M:%S") + timedelta(minutes=30)).time().strftime("%H:%M:%S")
            formapgto = random.choice(formas_pgto)
            try:
                print(f"Inserindo consulta: Paciente {idpac}, Médico {crm}, Especialidade {idesp}")
                cursor.execute(
                    "INSERT INTO consulta (CRM, IdPac, IdEsp, Data, HoraInCon, HoraFimCon, FormaPgto, NomeM, NomeE, NomePaciente, IdadePaciente) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (crm, idpac, idesp, data, hora_inicio, hora_fim, formapgto, nomem, nomee, nomepac, idadepac)
                )
            except Exception as e:
                print(f"Erro ao inserir consulta: {e}")
    conn.commit()

