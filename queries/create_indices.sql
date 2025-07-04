CREATE INDEX indice_nomepac ON hospital.paciente (NomePac);
CREATE INDEX indice_cpficol ON hospital.paciente (CPF);
CREATE INDEX indice_telefonepac ON hospital.paciente (TelefonePac);

CREATE INDEX indice_nomem ON hospital.medico (NomeM);
CREATE INDEX indice_telefonem ON hospital.medico (TelefoneM);

CREATE INDEX indice_nomee ON hospital.especialidade (NomeE);

CREATE INDEX indice_diasemana ON hospital.agenda (DiaSemana);
CREATE INDEX indice_crm_agenda ON hospital.agenda (CRM);

CREATE INDEX indice_idesp_exerce ON hospital.exerce_esp (idEsp);
CREATE INDEX indice_crm_exerce ON hospital.exerce_esp (CRM);

CREATE INDEX indice_dataconsulta ON hospital.consulta (Data);
CREATE INDEX indice_crm_consulta ON hospital.consulta (CRM);
CREATE INDEX indice_idpac_consulta ON hospital.consulta (IdPac);
CREATE INDEX indice_idesp_consulta ON hospital.consulta (IdEsp);

CREATE INDEX indice_idcon_diag ON hospital.diagnostico (IdCon);