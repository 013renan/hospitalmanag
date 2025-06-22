SELECT medico.CRM AS IdMedico,
       paciente.idpaciente AS IdPaciente,
       consultas.IdEsp AS IdEspecial,
       consultas.Data AS Data,
       consultas.HoraInCon AS HoraInicCon
FROM hospital.consulta AS consultas
JOIN hospital.paciente AS paciente ON consultas.IdPac = paciente.idpaciente
JOIN hospital.medico AS medico ON consultas.CRM = medico.CRM
WHERE paciente.NomePac = 'Diego Pituca' AND medico.NomeM = 'Dr. House';
