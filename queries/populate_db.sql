INSERT INTO paciente (NomePac, CPF, Idade, Sexo, TelefonePac, Endereco)
VALUES
    ('Diego Pituca', '236.789.123-10', 35, 'F', '1124552028', 'Rua dos Pinheiros, 282'),
    ('João Santos', '521.654.987-10', 42, 'M', '1155563214', 'Rua Rodrigues Alves, 645'),
    ('Ana Oliveira', '678.912.345-10', 28, 'F', '1126543215', 'Rua das Orquídeas, 369'),
    ('Maria da Silva', '012.456.789-10', 23, 'F', '1154321212', 'Rua da Catedral, 123'),
    ('Pedro Oliveira', '333.222.111-10', 31, 'M', '11987456123', 'Rua João Ramalho, 987'),
    ('Carla Martins', '444.555.333-10', 27, 'F', '1112345678', 'Rua da Liberdade, 234'),
    ('Rodrigo Sousa', '888.777.666-10', 38, 'M', '1165432154', 'Rua Engenheiro Carlos Alberto, 987'),
    ('Felipe Lima', '111.222.333-10', 20, 'M', '3155551111', 'Rua Padre Anchieta, 234'),
    ('Larissa Martins', '999.444.555-10', 25, 'F', '3211122222', 'Rua da República, 123'),
    ('Lucas Almeida', '345.678.999-10', 15, 'M', '3412354321', 'Rua dos Imigrantes, 567');

INSERT INTO medico (CRM, NomeM, TelefoneM, Percentual)
VALUES
    (123456, 'Dr. House', '1112341841', 25),
    (789012, 'Dr. Kildare', '111849101', 15),
    (345678, 'Dr. Jo�o Silva', '1128593561', 15);

INSERT INTO doenca (iddoenca, nome)
VALUES
    (1, 'Gripe'),
    (2, 'Diabetes'),
    (3, 'Hipertensão'),
    (4, 'Asma'),
    (5, 'Câncer'),
    (6, 'Artrite'),
    (7, 'Obesidade'),
    (8, 'Depressão'),
    (9, 'Anemia'),
    (10, 'Outros');


INSERT INTO especialidade (idEsp, NomeE, Indice)
VALUES
    (1, 'Cardiologia', 0.8),
    (2, 'Ortopedia', 0.7),
    (3, 'Pediatria', 0.9),
    (4, 'Dermatologia', 0.75),
    (5, 'Neurologia', 0.85),
    (6, 'Ginecologia', 0.82),
    (7, 'Oftalmologia', 0.78),
    (8, 'Oncologia', 0.88),
    (9, 'Urologia', 0.79),
    (10, 'Outros', 1);


INSERT INTO agenda (DiaSemana, HoraInicio, HoraFIm, CRM)
VALUES 
    ('SEG', '08:00:00', '12:00:00', 123456),
    ('TER', '08:00:00', '12:00:00', 123456),
    ('QUA', '08:00:00', '12:00:00', 123456),
    ('QUI', '08:00:00', '12:00:00', 123456),
    ('SEX', '08:00:00', '12:00:00', 123456),
    ('SAB', '08:00:00', '12:00:00', 123456),
    ('DOM', '08:00:00', '12:00:00', 123456);

INSERT INTO agenda (DiaSemana, HoraInicio, HoraFIm, CRM)
VALUES 
    ('SEG', '09:00:00', '13:00:00', 789012),
    ('TER', '09:00:00', '13:00:00', 789012),
    ('QUI', '09:00:00', '13:00:00', 789012),
    ('SEX', '09:00:00', '13:00:00', 789012),
    ('SAB', '09:00:00', '13:00:00', 789012);

INSERT INTO agenda (DiaSemana, HoraInicio, HoraFIm, CRM)
VALUES 
    ('TER', '10:00:00', '14:00:00', 345678),
    ('QUA', '10:00:00', '14:00:00', 345678),
    ('QUI', '10:00:00', '14:00:00', 345678),
    ('SEX', '10:00:00', '14:00:00', 345678),
    ('DOM', '10:00:00', '14:00:00', 345678);


INSERT INTO exerce_esp (idEsp, CRM)
VALUES
    (2, 789012),
    (3, 345678),
    (5, 789012), 
    (6, 345678);

INSERT INTO exerce_esp (idEsp, CRM)
VALUES
    (1, 123456),
    (2, 123456),
    (3, 123456),
    (4, 123456),
    (5, 123456),
    (6, 123456),
    (7, 123456),
    (8, 123456),
    (9, 123456),
    (10, 123456);

INSERT INTO consulta 
(CRM, IdPac, IdEsp, Data, HoraInCon, HoraFimCon, FormaPgto, NomeM, NomeE, NomePaciente, IdadePaciente)
VALUES
(123456, 1, 3, '2024-05-10', '10:00:00', '09:00:00', 'Dinheiro', 'Dr. House', 'Pediatria', 'Diego Pituca', 35),
(789012, 2, 2, '2024-01-02', '09:00:00', '10:00:00', 'Cartão', 'Dr. Kildare', 'Ortopedia', 'João Santos', 42),
(345678, 3, 3, '2024-01-03', '10:00:00', '11:00:00', 'Boleto', 'Dr. João Silva', 'Pediatria', 'Ana Oliveira', 28),
(123456, 4, 1, '2024-01-04', '08:30:00', '09:30:00', '-', 'Dr. House', 'Cardiologia', 'Maria da Silva', 23),
(789012, 5, 2, '2024-01-05', '09:30:00', '10:30:00', 'Cartão', 'Dr. Kildare', 'Ortopedia', 'Pedro Oliveira', 31),
(345678, 6, 3, '2024-02-06', '10:30:00', '11:30:00', 'Boleto', 'Dr. João Silva', 'Pediatria', 'Carla Martins', 27),
(123456, 7, 1, '2024-03-07', '08:45:00', '09:45:00', 'Dinheiro', 'Dr. House', 'Cardiologia', 'Rodrigo Sousa', 38),
(789012, 8, 2, '2024-03-08', '09:45:00', '10:45:00', 'Cartão', 'Dr. Kildare', 'Ortopedia', 'Felipe Lima', 20),
(345678, 9, 3, '2024-04-09', '10:45:00', '11:45:00', '-', 'Dr. João Silva', 'Pediatria', 'Larissa Martins', 25),
(123456, 10, 1, '2024-05-10', '08:15:00', '09:15:00', 'Dinheiro', 'Dr. House', 'Cardiologia', 'Lucas Almeida', 15);



