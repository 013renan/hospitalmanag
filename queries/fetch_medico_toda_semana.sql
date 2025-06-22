SELECT medico.NomeM
FROM hospital.medico medico
JOIN hospital.agenda agenda ON medico.CRM = agenda.CRM
GROUP BY medico.CRM, medico.NomeM
HAVING COUNT(DISTINCT DiaSemana) = 7;