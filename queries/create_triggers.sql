CREATE TRIGGER after_paciente_update
AFTER UPDATE ON paciente
FOR EACH ROW
BEGIN
    UPDATE consulta
    SET NomePaciente = NEW.NomePac,
        IdadePaciente = NEW.Idade
    WHERE IdPac = NEW.idpaciente;
END;

CREATE TRIGGER after_medico_update
AFTER UPDATE ON medico
FOR EACH ROW
BEGIN
    UPDATE consulta
    SET NomeM = NEW.NomeM
    WHERE CRM = NEW.CRM;
END;

CREATE TRIGGER after_especialidade_update
AFTER UPDATE ON especialidade
FOR EACH ROW
BEGIN
    UPDATE consulta
    SET NomeE = NEW.NomeE
    WHERE IdEsp = NEW.idEsp;
END;