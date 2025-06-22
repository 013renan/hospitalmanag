SELECT consulta.CRM AS IdMedico, consulta.IdPac AS IdPaciente, consulta.IdEsp AS IdEspecial, consulta.Data, consulta.HoraInCon AS HoraInicCon
FROM hospital.consulta
WHERE MONTH(consulta.Data) = 1 AND YEAR(consulta.Data) = 2024;
