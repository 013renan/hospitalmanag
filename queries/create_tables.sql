
CREATE TABLE  paciente (
  idpaciente int NOT NULL AUTO_INCREMENT,
  NomePac varchar(45) NOT NULL,
  CPF varchar(14) NOT NULL,
  Idade int NOT NULL,
  Sexo char(1) NOT NULL,
  TelefonePac varchar(12) NOT NULL,
  Endereco varchar(45) NOT NULL,
  PRIMARY KEY (idpaciente),
  UNIQUE KEY idpaciente_UNIQUE (idpaciente),
  UNIQUE KEY pacientecol_UNIQUE (CPF)
);

CREATE TABLE  medico (
  CRM int NOT NULL,
  NomeM varchar(45) NOT NULL,
  TelefoneM varchar(12) NOT NULL,
  Percentual float NOT NULL,
  PRIMARY KEY (CRM),
  UNIQUE KEY CRM_UNIQUE (CRM)
);

CREATE TABLE  doenca (
  iddoenca int NOT NULL,
  nome varchar(45) NOT NULL,
  PRIMARY KEY (iddoenca),
  UNIQUE KEY iddoenca_UNIQUE (iddoenca)
);

CREATE TABLE  especialidade (
  idEsp int NOT NULL,
  NomeE varchar(45) NOT NULL,
  Indice float NOT NULL,
  PRIMARY KEY (idEsp),
  UNIQUE KEY idEsp_UNIQUE (idEsp),
  UNIQUE KEY NomeEl_UNIQUE (NomeE)
);

CREATE TABLE  agenda (
  idAgenda int NOT NULL AUTO_INCREMENT,
  DiaSemana varchar(3) DEFAULT 'SEG',
  HoraInicio time DEFAULT NULL,
  HoraFIm time DEFAULT NULL,
  CRM int NOT NULL,
  PRIMARY KEY (idAgenda),
  KEY CRM_idx (CRM),
  CONSTRAINT CRM FOREIGN KEY (CRM) REFERENCES medico (CRM) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE  exerce_esp (
  idEsp int NOT NULL,
  CRM int NOT NULL,
  PRIMARY KEY (idEsp,CRM),
  KEY CRM_idx (CRM),
  CONSTRAINT crmEsp FOREIGN KEY (CRM) REFERENCES medico (CRM) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT exEsp FOREIGN KEY (idEsp) REFERENCES especialidade (idEsp) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE  consulta (
  idconsulta int NOT NULL AUTO_INCREMENT,
  NomeM varchar(45) NOT NULL,
  NomeE varchar(45) NOT NULL,
  CRM int NOT NULL,
  IdPac int NOT NULL,
  IdEsp int NOT NULL,
  Data date NOT NULL,
  NomePaciente varchar(45), 
  IdadePaciente int,
  HoraInCon time NOT NULL,
  HoraFimCon time NOT NULL,
  Pau varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  ValorPa float DEFAULT NULL,
  FormaPgto varchar(45) NOT NULL,
  PRIMARY KEY (idconsulta),
  UNIQUE KEY idconsulta_UNIQUE (idconsulta),
  KEY MedCon_idx (CRM),
  KEY EspCon_idx (IdEsp),
  KEY PacCon_idx (IdPac),
  CONSTRAINT EspCon FOREIGN KEY (IdEsp) REFERENCES especialidade (idEsp),
  CONSTRAINT MedCon FOREIGN KEY (CRM) REFERENCES medico (CRM),
  CONSTRAINT PacCon FOREIGN KEY (IdPac) REFERENCES paciente (idpaciente) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE consulta_detalhada (
    idconsulta int NOT NULL,
    NomePac varchar(45) NOT NULL,
    CPF varchar(14) NOT NULL,
    NomeM varchar(45) NOT NULL,
    CRM int NOT NULL,
    Data date NOT NULL,
    HoraInCon time NOT NULL,
    HoraFimCon time NOT NULL,
    IdEsp int NOT NULL,
    NomeE varchar(45) NOT NULL,
    FormaPgto varchar(45) NOT NULL,
    PRIMARY KEY (idconsulta)
);



