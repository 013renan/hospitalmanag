SELECT medico.CRM, medico.NomeM
FROM hospital.medico
JOIN hospital.exerce_esp ON medico.CRM = exerce_esp.CRM
JOIN hospital.especialidade e ON exerce_esp.idEsp = e.idEsp
GROUP BY medico.CRM, medico.NomeM
HAVING COUNT(DISTINCT e.idEsp) = (SELECT COUNT(*) FROM hospital.especialidade);
