# 🏥 Hospital Database Populator

Este projeto automatiza a criação e o preenchimento de um banco de dados MySQL com dados fictícios de pacientes e consultas médicas, utilizando Python e a biblioteca Faker.

## 📦 Tecnologias Utilizadas

- Python 3.8+
- MySQL Server
- Faker (geração de dados)
- mysql-connector-python

## ⚙️ Pré-requisitos

Antes de começar, você precisará ter instalado:

- Python (versão 3.8 ou superior)
- MySQL Server rodando localmente
- Git (para clonar o repositório)

## 🚀 Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. (Opcional) Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate     # Linux/macOS
   venv\Scripts\activate        # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## 🛠️ Configuração do Banco de Dados

1. Verifique se o MySQL Server está rodando.
2. Atualize os dados de conexão (usuário, senha, host) nos scripts `.py` conforme necessário.
3. Ao executar o script principal, o banco `hospital` será criado automaticamente com suas tabelas.

## ▶️ Como Usar

Execute o script principal para criar e popular o banco de dados:
```bash
python main.py
```

O script realiza as seguintes tarefas:
- Criação do banco de dados e tabelas
- Inserção de médicos e especialidades
- Geração de pacientes e consultas com dados fictícios

Você pode personalizar a quantidade de dados alterando os valores no início do `main.py`:
```python
n_pacientes = 50000
consultas_por_paciente = 10
```

## 🧱 Estrutura do Banco

A estrutura das tabelas está definida no arquivo `create_tables.sql`. Isso inclui:

- Médicos
- Especialidades
- Pacientes
- Consultas

## 📚 Créditos

- [Faker](https://faker.readthedocs.io/) — Geração de dados falsos
- [mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/) — Conector MySQL para Python

## 📝 Licença

Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE` para mais informações.


## 💻 Interface Web (Streamlit)

Este projeto também inclui uma interface web feita com [Streamlit](https://streamlit.io/), permitindo visualizar ou interagir com os dados do banco de forma amigável.

Para rodar a interface, use o seguinte comando:
```bash
python -m streamlit run interface.py
```

Certifique-se de que o ambiente virtual está ativado (se estiver usando um), e que todas as dependências estão instaladas.
