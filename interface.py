import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import mysql.connector
from config import DB_CONFIG
import queriesMenu as qm

# --- GESTÃO DA LIGAÇÃO À BASE DE DADOS ---
@st.cache_resource
def get_db_connection():
    """
    Estabelece e retorna uma ligação à base de dados.
    O decorador @st.cache_resource garante que a ligação é criada
    apenas uma vez e reutilizada nas interações do utilizador.
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print("Ligação à base de dados estabelecida pela interface.")
        return conn
    except mysql.connector.Error as e:
        st.error(f"Erro de ligação à base de dados: {e}")
        return None

# --- FUNÇÕES AUXILIARES DE FORMATAÇÃO E DATAFRAME ---

def formatar_cpf(cpf):
    """Formata uma string de CPF para o padrão XXX.XXX.XXX-XX."""
    cpf_limpo = ''.join(filter(str.isdigit, str(cpf)))
    if len(cpf_limpo) == 11:
        return f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"
    return cpf

def formatar_telefone(telefone):
    """Formata uma string de telefone para (XX) XXXXX-XXXX ou (XX) XXXX-XXXX."""
    tel_limpo = ''.join(filter(str.isdigit, str(telefone)))
    if len(tel_limpo) == 11:
        return f"({tel_limpo[:2]}) {tel_limpo[2:7]}-{tel_limpo[7:]}"
    elif len(tel_limpo) == 10:
        return f"({tel_limpo[:2]}) {tel_limpo[2:6]}-{tel_limpo[6:]}"
    return telefone

def make_patient_df(raw_result):
    """Cria um DataFrame de pacientes a partir do resultado bruto da query."""
    if not raw_result:
        return pd.DataFrame()
    df = pd.DataFrame(raw_result, columns=[
        "ID", "Nome", "CPF", "Idade", "Sexo", "Telefone", "Endereço"
    ])
    return df

def make_consultas_df(raw_result):
    """Cria um DataFrame de consultas a partir do resultado bruto da query."""
    if not raw_result:
        return pd.DataFrame()
    df_temp = pd.DataFrame(raw_result)
    df_temp.columns = [
        "ID Consulta", "CRM", "ID Especialidade", "ID Paciente", "Data", "Hora Início", "Hora Fim", "Forma de Pagamento", "Nome Médico", "Especialidade", "Nome Paciente", "Idade Paciente"
    ]
    colunas_exibicao = [
        "ID Consulta", "Nome Médico", "Especialidade", "CRM", "ID Paciente", "ID Especialidade", "Data",
        "Nome Paciente", "Idade Paciente", "Hora Início", "Hora Fim", "Forma de Pagamento"
    ]
    df = df_temp[colunas_exibicao]
    if "Data" in df.columns:
        if df["Data"].dtype == object:
            df["Data"] = pd.to_datetime(df["Data"], errors='coerce').dt.strftime('%d/%m/%Y')
        else:
            df["Data"] = df["Data"].astype(str)
    return df

def make_relatorio_df(raw_result):
    """Cria um DataFrame para o relatório de histórico de consultas."""
    if not raw_result:
        return pd.DataFrame()
    colunas = ["ID Consulta", "Nome Paciente", "Nome Médico", "Data", "CRM", "Especialidade"]
    df = pd.DataFrame(raw_result, columns=colunas)
    if "Data" in df.columns:
        df["Data"] = pd.to_datetime(df["Data"]).dt.strftime('%d/%m/%Y')
    return df

# --- INTERFACE PRINCIPAL ---

def main():
    st.set_page_config(
        page_title="Sistema Hospitalar",
        page_icon="🏥",
        layout="wide"
    )

    conn = get_db_connection()
    if not conn:
        st.error("Não foi possível ligar à base de dados. Verifique as configurações e o estado do servidor.")
        st.stop()

    if "menu" not in st.session_state:
        st.session_state.menu = "Home"

    st.sidebar.title("Sistema Hospitalar")
    menu_options = ["Home", "Gestão de Pacientes", "Gestão de Consultas", "Relatórios"]
    
    try:
        current_index = menu_options.index(st.session_state.menu)
    except ValueError:
        current_index = 0
        st.session_state.menu = "Home"

    st.session_state.menu = st.sidebar.radio(
        "Navegação",
        menu_options,
        index=current_index
    )

    if st.session_state.menu == "Home":
        st.title("🏥 Sistema Hospitalar")
        st.subheader("Bem-vindo ao Sistema de Gestão Hospitalar")
        st.write("Utilize o menu lateral para navegar entre as funcionalidades.")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Ir para Pacientes", use_container_width=True):
                st.session_state.menu = "Gestão de Pacientes"
                st.rerun()
        with col2:
            if st.button("Ir para Consultas", use_container_width=True):
                st.session_state.menu = "Gestão de Consultas"
                st.rerun()
        with col3:
            if st.button("Ir para Relatórios", use_container_width=True):
                st.session_state.menu = "Relatórios"
                st.rerun()

    elif st.session_state.menu == "Gestão de Pacientes":
        st.title("👤 Gestão de Pacientes")
        tabs = st.tabs(["Buscar Paciente", "Cadastrar Paciente"])

        with tabs[0]:
            st.subheader("Buscar Paciente por CPF")
            cpf_busca = st.text_input("Digite o CPF do paciente:", max_chars=14, help="Digite o CPF completo, com ou sem pontos/traço.")
            if st.button("Buscar Paciente"):
                if cpf_busca:
                    cpf_formatado = formatar_cpf(cpf_busca)
                    with st.spinner("A buscar paciente..."):
                        raw_result = qm.search_patient_by_cpf(conn, cpf_formatado)
                    df = make_patient_df(raw_result)
                    if not df.empty:
                        st.success("Paciente encontrado!")
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.error("Paciente não encontrado.")
                else:
                    st.warning("Digite o CPF para buscar.")

        with tabs[1]:
            st.subheader("Cadastrar Novo Paciente")
            with st.form("form_cadastro_paciente", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    nomepac = st.text_input("Nome Completo")
                    cpf_cad = st.text_input("CPF (apenas números)", max_chars=11)
                    idade_str = st.text_input("Idade", max_chars=3)
                with col2:
                    sexo = st.selectbox("Sexo", options=["M", "F"], index=None, placeholder="Selecione...")
                    telefonepac = st.text_input("Telefone (com DDD)", max_chars=11)
                    endereco = st.text_area("Endereço Completo")

                submitted = st.form_submit_button("Cadastrar Paciente")
                if submitted:
                    if not all([nomepac, cpf_cad, idade_str, sexo, telefonepac, endereco]):
                        st.error("Preencha todos os campos obrigatórios.")
                    elif not (cpf_cad.isdigit() and len(cpf_cad) == 11):
                        st.error("CPF deve conter exatamente 11 números.")
                    elif not (telefonepac.isdigit() and len(telefonepac) in [10, 11]):
                        st.error("Telefone deve conter 10 ou 11 números (incluindo DDD).")
                    elif not (idade_str.isdigit() and 0 < int(idade_str) <= 120):
                        st.error("Idade deve ser um número válido entre 1 e 120.")
                    else:
                        cpf_mask = formatar_cpf(cpf_cad)
                        tel_mask = formatar_telefone(telefonepac)
                        idade = int(idade_str)
                        
                        try:
                            qm.insert_patient(conn, nomepac, cpf_mask, idade, sexo, tel_mask, endereco)
                            st.success(f"Paciente {nomepac} cadastrado com sucesso!")
                        except Exception as e:
                            st.error(f"Erro ao cadastrar paciente: {str(e)}")

    elif st.session_state.menu == "Gestão de Consultas":
        st.title("📋 Gestão de Consultas")
        tabs = st.tabs(["Buscar Consulta", "Agendar Consulta", "Atualizar Consulta", "Deletar Consulta"])

        with tabs[0]:
            st.subheader("Buscar Consulta")
            col1, col2, col3 = st.columns(3)
            with col1:
                patient_id = st.number_input("ID do Paciente (opcional):", min_value=0, step=1)
                patient_id = None if patient_id == 0 else patient_id
            with col2:
                date_val = st.date_input("Data (opcional):", value=None)
                date_str = date_val.strftime("%Y-%m-%d") if date_val else None
            with col3:
                crm = st.number_input("CRM do Médico (opcional):", min_value=0, step=1)
                crm = None if crm == 0 else crm
            if st.button("Buscar Consultas"):
                with st.spinner("A buscar consultas..."):
                    raw_result = qm.search_consulta(conn, patient_id, date_str, crm)
                df = make_consultas_df(raw_result)
                if not df.empty:
                    st.success("Consultas encontradas!")
                    st.dataframe(df, use_container_width=True)
                else:
                    st.error("Nenhuma consulta encontrada com os critérios informados.")

        with tabs[1]:
            st.subheader("Agendar Nova Consulta")
            with st.form("form_agendar_consulta", clear_on_submit=True):
                medicos = qm.get_medicos(conn)
                opcoes_medicos = {f"{nome} (CRM: {crm})": crm for crm, nome in medicos}
                medico_selecionado = st.selectbox("Selecione o Médico:", options=opcoes_medicos.keys())
                crm_ag = opcoes_medicos[medico_selecionado]

                idpac = st.number_input("ID do Paciente:", min_value=1, step=1)

                especialidades = qm.get_especialidades(conn)
                opcoes_especialidades = {f"{nome} (ID: {id_esp})": id_esp for id_esp, nome in especialidades}
                especialidade_selecionada = st.selectbox("Selecione a Especialidade:", opcoes_especialidades.keys())
                idesp = opcoes_especialidades[especialidade_selecionada]

                data_ag = st.date_input("Data da Consulta:", min_value=datetime.today())
                horaincon = st.time_input("Hora de Início:")
                horafimcon = st.time_input("Hora de Fim:", value=(datetime.strptime("00:30", "%H:%M") + timedelta(hours=horaincon.hour, minutes=horaincon.minute)).time())
                formapgto = st.selectbox("Forma de Pagamento:", ["Dinheiro", "Cartão", "Boleto", "-"])
                
                submitted_ag = st.form_submit_button("Agendar Consulta")
                if submitted_ag:
                    try:
                        qm.insert_consulta(
                            conn, crm_ag, idpac, idesp,
                            data_ag.strftime("%Y-%m-%d"),
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
            idconsulta_upd = st.number_input("ID da Consulta", min_value=1, step=1, key="idconsulta_update")
            field = st.selectbox("Campo a atualizar", ["Data", "HoraInCon", "HoraFimCon", "FormaPgto"])
            
            value = None
            if field == "Data":
                value = st.date_input("Nova Data:", min_value=datetime.today()).strftime("%Y-%m-%d")
            elif field in ["HoraInCon", "HoraFimCon"]:
                value = st.time_input(f"Nova {field}:").strftime("%H:%M:%S")
            else:
                value = st.selectbox("Novo Valor para Forma de Pagamento", ["Dinheiro", "Cartão", "Boleto", "-"])

            if st.button("Atualizar Consulta"):
                try:
                    qm.update_consulta_field(conn, idconsulta_upd, field, value)
                    st.success("Consulta atualizada com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao atualizar consulta: {str(e)}")

        with tabs[3]:
            st.subheader("Deletar Consulta")
            idconsulta_del = st.number_input("ID da Consulta a ser deletada:", min_value=1, step=1)
            confirm = st.checkbox("Confirmar deleção? Esta ação não pode ser desfeita.")
            if st.button("Deletar Consulta"):
                if confirm:
                    try:
                        qm.delete_consulta(conn, idconsulta_del)
                        st.success("Consulta deletada com sucesso!")
                    except Exception as e:
                        st.error(f"Erro ao deletar consulta: {str(e)}")
                else:
                    st.warning("Por favor, confirme a deleção antes de continuar.")

    elif st.session_state.menu == "Relatórios":
        st.title("📊 Relatórios")
        st.subheader("Histórico de Consultas por Paciente")
        cpf_rel = st.text_input("Digite o CPF do paciente para o relatório:", max_chars=14, help="Digite o CPF completo.")
        if st.button("Buscar Histórico"):
            if cpf_rel:
                cpf_formatado_rel = formatar_cpf(cpf_rel)
                with st.spinner("A buscar histórico..."):
                    paciente_info = qm.search_patient_by_cpf(conn, cpf_formatado_rel)
                    if paciente_info:
                        df_paciente = make_patient_df(paciente_info)
                        st.markdown("#### Dados do Paciente")
                        st.dataframe(df_paciente, use_container_width=True)

                        raw_result_rel = qm.search_all_consults_by_cpf_normalizada(conn, cpf_formatado_rel)
                        df = make_relatorio_df(raw_result_rel)
                        if not df.empty:
                            st.success(f"Histórico encontrado para CPF {cpf_formatado_rel}")
                            st.markdown("#### Histórico de Consultas")
                            st.dataframe(df, use_container_width=True)

                            total_consultas = len(df)
                            st.metric("Total de consultas realizadas", total_consultas)

                            if "Especialidade" in df.columns and not df["Especialidade"].empty:
                                especialidade_frequente = df["Especialidade"].mode()[0]
                                st.metric("Especialidade mais frequente", especialidade_frequente)

                            csv = df.to_csv(index=False).encode('utf-8')
                            st.download_button(
                                "Exportar para CSV",
                                csv,
                                f"historico_consultas_{cpf_rel}.csv",
                                "text/csv"
                            )
                        else:
                            st.info("Paciente encontrado, mas não possui histórico de consultas.")
                    else:
                        st.error("Paciente não encontrado.")
            else:
                st.warning("Digite um CPF para buscar.")

if __name__ == "__main__":
    main()