import streamlit as st
import pandas as pd
from datetime import datetime
from queriesMenu import (
    search_patient_by_cpf,
    insert_patient,
    search_consulta,
    insert_consulta,
    delete_consulta,
    update_consulta_field,
    search_all_consults_by_cpf_normalizada,
    search_all_consults_by_cpf,
    get_medicos,
    get_especialidades
)

def formatar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) == 11:
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    return cpf

def formatar_telefone(telefone):
    telefone = ''.join(filter(str.isdigit, telefone))
    if len(telefone) == 11:
        return f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"
    elif len(telefone) == 10:
        return f"({telefone[:2]}) {telefone[2:6]}-{telefone[6:]}"
    return telefone

def make_patient_df(raw_result):
    if not raw_result:
        return pd.DataFrame()
    df = pd.DataFrame(raw_result, columns=[
        "ID", "Nome", "CPF", "Idade", "Sexo", "Telefone", "Endereço"
    ])
    return df

def make_consultas_df(raw_result):
    if not raw_result:
        return pd.DataFrame()
    df = pd.DataFrame(raw_result, columns=[
        "ID Consulta", "Nome Médico", "Especialidade", "CRM", "ID Paciente", "ID Especialidade", "Data",
        "Nome Paciente", "Idade Paciente", "Hora Início", "Hora Fim", "PAU", "Valor PA", "Forma de Pagamento"
    ])
    return df

def make_relatorio_df(raw_result):
    if not raw_result:
        return pd.DataFrame()
    colunas = ["ID Consulta", "Nome Paciente", "Nome Médico", "Data", "CRM", "Especialidade"]
    df = pd.DataFrame(raw_result, columns=colunas)
    return df

def main():
    st.set_page_config(
        page_title="Sistema Hospitalar",
        page_icon="🏥",
        layout="wide"
    )

    if "menu" not in st.session_state:
        st.session_state.menu = "Home"

    st.sidebar.title("Sistema Hospitalar")
    menu = st.sidebar.radio(
        "Navegação",
        ["Home", "Gestão de Pacientes", "Gestão de Consultas", "Relatórios"],
        index=["Home", "Gestão de Pacientes", "Gestão de Consultas", "Relatórios"].index(st.session_state.menu)
    )
    st.session_state.menu = menu

    if menu == "Home":
        st.title("🏥 Sistema Hospitalar")
        st.subheader("Bem-vindo ao Sistema de Gestão Hospitalar")
        st.write("Utilize o menu lateral para navegar entre as funcionalidades.")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("### Pacientes")
            st.write("Cadastre e busque informações de pacientes")
            if st.button("Ir para Pacientes"):
                st.session_state.menu = "Gestão de Pacientes"
                st.rerun()
        with col2:
            st.info("### Consultas")
            st.write("Gerencie consultas médicas")
            if st.button("Ir para Consultas"):
                st.session_state.menu = "Gestão de Consultas"
                st.rerun()
        with col3:
            st.info("### Relatórios")
            st.write("Visualize relatórios e históricos")
            if st.button("Ir para Relatórios"):
                st.session_state.menu = "Relatórios"
                st.rerun()

    elif menu == "Gestão de Pacientes":
        st.title("👤 Gestão de Pacientes")
        aba = st.tabs(["Buscar Paciente", "Cadastrar Paciente"])

        # Buscar paciente por CPF
        with aba[0]:
            st.subheader("Buscar Paciente por CPF")
            cpf = st.text_input("Digite o CPF do paciente:", max_chars=14, help="Digite o CPF completo, com ou sem pontos/traço.")
            if st.button("Buscar Paciente"):
                if cpf:
                    # Permite buscar com ou sem máscara
                    cpf_busca = formatar_cpf(cpf)
                    with st.spinner("Buscando paciente..."):
                        raw_result = search_patient_by_cpf(cpf_busca)
                        if not raw_result:
                            # Tenta buscar sem máscara se não encontrou
                            raw_result = search_patient_by_cpf(''.join(filter(str.isdigit, cpf)))
                    df = make_patient_df(raw_result)
                    if not df.empty:
                        st.success("Paciente encontrado!")
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.error("Paciente não encontrado.")
                else:
                    st.warning("Digite o CPF para buscar.")

        # Cadastrar paciente
        with aba[1]:
            st.subheader("Cadastrar Novo Paciente")
            with st.form("form_cadastro_paciente"):
                col1, col2 = st.columns(2)
                with col1:
                    nomepac = st.text_input("Nome")
                    cpf_cad = st.text_input("CPF (apenas números)", max_chars=11, help="Digite apenas os 11 números do CPF.")
                    idade_str = st.text_input("Idade (em anos)", max_chars=3)
                with col2:
                    sexo = st.selectbox("Sexo", options=["M", "F"])
                    telefonepac = st.text_input("Telefone (apenas números)", max_chars=11, help="DDD + número, só números.")
                    endereco = st.text_area("Endereço", height=100)
                submitted = st.form_submit_button("Cadastrar Paciente")
                if submitted:
                    # Validações
                    if not nomepac or not cpf_cad or not telefonepac or not endereco or not idade_str:
                        st.error("Preencha todos os campos obrigatórios.")
                    elif not (cpf_cad.isdigit() and len(cpf_cad) == 11):
                        st.error("CPF deve ter 11 números.")
                    elif not (telefonepac.isdigit() and len(telefonepac) in [10, 11]):
                        st.error("Telefone deve ter 10 ou 11 números (incluindo DDD).")
                    elif not (idade_str.isdigit() and 0 < int(idade_str) <= 120):
                        st.error("Idade deve ser um número entre 1 e 120.")
                    else:
                        cpf_mask = formatar_cpf(cpf_cad)
                        tel_mask = formatar_telefone(telefonepac)
                        idade = int(idade_str)
                        try:
                            #st.write("DEBUG: Vai cadastrar paciente com:", nomepac, cpf_mask, idade, sexo, telefonepac, endereco)

                            # Remova o campo idpaciente do insert_patient!
                            insert_patient(nomepac, cpf_mask, idade, sexo, telefonepac, endereco)
                            st.success(f"Paciente {nomepac} cadastrado!")
                        except Exception as e:
                            st.error(f"Erro ao cadastrar paciente: {str(e)}")

    elif menu == "Gestão de Consultas":
        st.title("📋 Gestão de Consultas")
        tabs = st.tabs(["Buscar Consulta", "Agendar Consulta", "Atualizar Consulta", "Deletar Consulta"])

        with tabs[0]:
            st.subheader("Buscar Consulta")
            col1, col2, col3 = st.columns(3)
            with col1:
                patient_id = st.number_input("ID do Paciente (opcional):", min_value=0)
                patient_id = None if patient_id == 0 else patient_id
            with col2:
                date = st.date_input("Data (opcional):", value=None)
                date_str = date.strftime("%Y-%m-%d") if date else None
            with col3:
                crm = st.number_input("CRM do Médico (opcional):", min_value=0)
                crm = None if crm == 0 else crm
            if st.button("Buscar Consultas"):
                with st.spinner("Buscando consultas..."):
                    raw_result = search_consulta(patient_id, date_str, crm)
                df = make_consultas_df(raw_result)
                if not df.empty:
                    st.success("Consultas encontradas!")
                    st.dataframe(df, use_container_width=True)
                else:
                    st.error("Nenhuma consulta encontrada com os critérios informados.")

        with tabs[1]:
            st.subheader("Agendar Nova Consulta")
            with st.form("form_agendar_consulta"):
                col1, col2 = st.columns(2)
                with col1:
                    # Busca médicos e especialidades do banco
                    medicos = get_medicos()
                    opcoes_medicos = [f"{nome} (CRM: {crm})" for crm, nome in medicos]
                    medico_selecionado = st.selectbox("Selecione o Médico:", opcoes_medicos)
                    crm = int(medico_selecionado.split("CRM: ")[1].replace(")", ""))

                    #pacientes = ... # Faça o mesmo para pacientes se quiser, ou mantenha o number_input
                    idpac = st.number_input("ID do Paciente:", min_value=1, step=1)

                    especialidades = get_especialidades()
                    opcoes_especialidades = [f"{nome} (ID: {id_esp})" for id_esp, nome in especialidades]
                    especialidade_selecionada = st.selectbox("Selecione a Especialidade:", opcoes_especialidades)
                    idesp = int(especialidade_selecionada.split("ID: ")[1].replace(")", ""))

                with col2:
                    data = st.date_input("Data da Consulta:", min_value=datetime.today())
                    horaincon = st.time_input("Hora de Início:")
                    horafimcon = st.time_input("Hora de Fim:", value=datetime.strptime("00:30:00", "%H:%M:%S").time())
                    formapgto = st.selectbox("Forma de Pagamento:", ["Dinheiro", "Cartão", "Boleto", "-"])
                submitted = st.form_submit_button("Agendar Consulta")
                if submitted:
                    try:
                        insert_consulta(
                            crm, idpac, idesp,
                            data.strftime("%Y-%m-%d"),
                            horaincon.strftime("%H:%M:%S"),
                            horafimcon.strftime("%H:%M:%S"),
                            formapgto
                        )
                        st.success("Consulta agendada com sucesso!")
                        st.balloons()
                    except Exception as e:
                        st.error(f"Erro ao agendar consulta: {str(e)}")

        with tabs[2]:
            st.subheader("Atualizar Consulta")
            idconsulta = st.number_input("ID da Consulta", min_value=1, key="idconsulta_update")
            field = st.selectbox("Campo a atualizar", [
                "Data", "HoraInCon", "HoraFimCon", "FormaPgto"
            ])
            if field == "Data":
                value = st.date_input("Nova Data:", min_value=datetime.today()).strftime("%Y-%m-%d")
            elif field in ["HoraInCon", "HoraFimCon"]:
                value = st.time_input(f"Nova {field}:").strftime("%H:%M:%S")
            else:
                value = st.selectbox("Novo Valor para Forma de Pagamento", ["Dinheiro", "Cartão", "Boleto", "-"])
            if st.button("Atualizar Consulta"):
                try:
                    update_consulta_field(idconsulta, field, value)
                    st.success("Consulta atualizada com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao atualizar consulta: {str(e)}")

        with tabs[3]:
            st.subheader("Deletar Consulta")
            idconsulta_del = st.number_input("ID da Consulta a ser deletada:", min_value=1)
            confirm = st.checkbox("Confirmar deleção? Esta ação não pode ser desfeita.")
            if st.button("Deletar Consulta"):
                if confirm:
                    try:
                        delete_consulta(idconsulta_del)
                        st.success("Consulta deletada com sucesso!")
                    except Exception as e:
                        st.error(f"Erro ao deletar consulta: {str(e)}")
                else:
                    st.warning("Por favor, confirme a deleção antes de continuar.")

    elif menu == "Relatórios":
        st.title("📊 Relatórios")
        st.subheader("Histórico de Consultas por Paciente")
        cpf = st.text_input("Digite o CPF do paciente:", max_chars=14, help="Digite o CPF completo, incluindo pontos e traço.")
        if st.button("Buscar Histórico"):
            if cpf:
                cpf_busca = formatar_cpf(cpf)
                with st.spinner("Buscando histórico..."):
                    raw_result = search_all_consults_by_cpf_normalizada(cpf_busca)
                    if not raw_result:
                        raw_result = search_all_consults_by_cpf_normalizada(''.join(filter(str.isdigit, cpf)))
                df = make_relatorio_df(raw_result)
                if not df.empty:
                    st.success(f"Histórico encontrado para CPF {cpf}")
                    st.dataframe(df, use_container_width=True)
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        "Exportar para CSV",
                        csv,
                        f"historico_consultas_{cpf}.csv",
                        "text/csv"
                    )
                else:
                    st.error("Nenhuma consulta encontrada para este CPF.")
            else:
                st.warning("Digite um CPF para buscar.")

if __name__ == "__main__":
    main()
