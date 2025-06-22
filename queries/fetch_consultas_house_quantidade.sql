SELECT especialidade.NomeE AS Especialidade, COUNT(*) AS Quantidade
FROM hospital.consulta
JOIN hospital.medico ON consulta.CRM = medico.CRM
JOIN hospital.especialidade ON consulta.IdEsp = especialidade.idEsp
WHERE medico.NomeM = 'Dr. House'
GROUP BY especialidade.NomeE;
