SELECT medico.NomeM AS NomeMedico, COUNT(consulta.idconsulta) AS TotalConsultas
FROM hospital.medico
LEFT JOIN hospital.consulta ON medico.CRM = consulta.CRM
GROUP BY medico.NomeM
ORDER BY TotalConsultas;
