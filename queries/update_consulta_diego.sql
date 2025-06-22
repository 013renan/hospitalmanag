CREATE TEMPORARY TABLE id_da_consulta AS (
    SELECT consulta.idconsulta
    FROM hospital.consulta
    JOIN hospital.paciente ON consulta.IdPac = paciente.idpaciente
    JOIN hospital.medico ON consulta.CRM = medico.CRM
    JOIN hospital.especialidade ON consulta.IdEsp = especialidade.idEsp
    WHERE paciente.NomePac = 'Diego Pituca'
      AND consulta.Data = '2024-05-10'
      AND consulta.HoraInCon = '10:00:00'
      AND especialidade.NomeE = 'Dermatologia'
      AND medico.NomeM = 'Dr. House'
);

UPDATE hospital.consulta
SET CRM = (SELECT CRM FROM hospital.medico WHERE NomeM = 'Dr. Kildare'),
    Data = '2024-05-24',
    HoraInCon = '10:00:00'
WHERE idconsulta IN (SELECT idconsulta FROM id_da_consulta);

