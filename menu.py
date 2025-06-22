from queriesMenu import *

def main():
    while True:
        print("\nSistema Hospitalar")
        print("1. Buscar Paciente por CPF")
        print("2. Buscar Consulta")
        print("3. Inserir Consulta")
        print("4. Inserir Paciente")
        print("5. Deletar Consulta")
        print("6. Atualizar Campo de Consulta")
        print("7. Buscar todas as Consultas por CPF")
        print("8. Sair")
        choice = input("Digite sua escolha: ")

        if choice == '1':
            cpf = input("Digite o CPF: ")
            result = search_patient_by_cpf(cpf)
            print(result)

        elif choice == '2':
            patient_id = input("Digite o ID do Paciente (ou pressione Enter para pular): ")
            date = input("Digite a Data (AAAA-MM-DD) (ou pressione Enter para pular): ")
            crm = input("Digite o CRM (ou pressione Enter para pular): ")

            patient_id = int(patient_id) if patient_id else None
            crm = int(crm) if crm else None

            result = search_consulta(patient_id=patient_id, date=date, crm=crm)
            print(result)

        elif choice == '3':
            crm = int(input("Digite o CRM: "))
            idpac = int(input("Digite o ID do Paciente: "))
            idesp = int(input("Digite o ID da Especialidade: "))
            data = input("Digite a Data (AAAA-MM-DD): ")
            horaincon = input("Digite a Hora de Início (HH:MM:SS): ")
            horafimcon = input("Digite a Hora de Fim (HH:MM:SS): ")
            formapgto = input("Digite a Forma de Pagamento: ")
            insert_consulta(crm, idpac, idesp, data, horaincon, horafimcon, formapgto)
            print("Consulta inserida com sucesso.")

        elif choice == '4':
            idpaciente = int(input("Digite o ID do Paciente: "))
            nomepac = input("Digite o Nome do Paciente: ")
            cpf = input("Digite o CPF: ")
            idade = int(input("Digite a Idade: "))
            sexo = input("Digite o Sexo (M/F): ")
            telefonepac = input("Digite o Telefone: ")
            endereco = input("Digite o Endereço: ")
            insert_patient(idpaciente, nomepac, cpf, idade, sexo, telefonepac, endereco)
            print("Paciente inserido com sucesso.")

        elif choice == '5':
            idconsulta = int(input("Digite o ID da Consulta: "))
            delete_consulta(idconsulta)
            print("Consulta deletada com sucesso.")

        elif choice == '6':
            idconsulta = int(input("Digite o ID da Consulta: "))
            field = input("Digite o campo a ser atualizado: ")
            value = input(f"Digite o novo valor para {field}: ")
            update_consulta_field(idconsulta, field, value)
            print("Consulta atualizada com sucesso.")

        elif choice == '7':
            cpf = input("Digite o CPF: ")
            print("Tabela Normalizada:")
            result = search_all_consults_by_cpf_normalizada(cpf)
            result = search_all_consults_by_cpf(cpf)
            print(result)

        elif choice == '8':
            break

        else:
            print("Escolha inválida. Por favor, tente novamente.")

if __name__ == "__main__":
    main()