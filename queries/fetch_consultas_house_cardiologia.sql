SELECT paciente.CPF, paciente.NomePac
FROM hospital.paciente paciente
JOIN hospital.consulta consulta ON paciente.idpaciente = consulta.IdPac
JOIN hospital.medico medico ON consulta.CRM = medico.CRM
JOIN hospital.exerce_esp exerce_esp ON medico.CRM = exerce_esp.CRM
JOIN hospital.especialidade especialidade ON exerce_esp.idEsp = especialidade.idEsp
WHERE medico.NomeM = 'Dr. House'
AND especialidade.NomeE = 'Cardiologia';
