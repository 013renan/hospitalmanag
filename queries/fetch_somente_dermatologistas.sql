SELECT medico.CRM, medico.NomeM
FROM hospital.medico AS medico
WHERE medico.CRM IN (
    SELECT exerce_esp.CRM
    FROM hospital.exerce_esp AS exerce_esp
    JOIN hospital.especialidade AS especialidade ON exerce_esp.idEsp = especialidade.idEsp
    WHERE especialidade.NomeE = 'Dermatologia'
)
AND medico.CRM NOT IN (
    SELECT exerce_esp.CRM
    FROM hospital.exerce_esp AS exerce_esp
    JOIN hospital.especialidade AS especialidade ON exerce_esp.idEsp = especialidade.idEsp
    WHERE especialidade.id <> 'Dermatologia'
);
