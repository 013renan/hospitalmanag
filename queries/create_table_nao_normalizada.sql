CREATE TABLE hospital.consulta_detalhada (
    idconsulta int NOT NULL,
    NomePac varchar(45) NOT NULL,
    CPF varchar(14) NOT NULL,
    NomeM varchar(45) NOT NULL,
    Data date NOT NULL,
    CRM int NOT NULL,
    NomeE varchar(45) NOT NULL,
    PRIMARY KEY (idconsulta)
);