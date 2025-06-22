
INSERT INTO medico (CRM, NomeM, TelefoneM, Percentual)
VALUES
    (123456, 'Dr. House', '1112341841', 25),
    (789012, 'Dr. Kildare', '111849101', 15),
    (345678, 'Dr. João Silva', '1128593561', 15);



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

