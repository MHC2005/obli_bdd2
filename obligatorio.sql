CREATE TABLE Persona (
    CI INT PRIMARY KEY,
    Nombre_Completo VARCHAR(100),
    Numero VARCHAR(20),
    Serie VARCHAR(20)
);

CREATE TABLE Establecimiento (
    ID_Establecimiento INT PRIMARY KEY,
    Tipo VARCHAR(50),
    Zona VARCHAR(50),
    Departamento VARCHAR(50),
    Nombre VARCHAR(100),
    Direccion VARCHAR(100)
);

CREATE TABLE Circuito (
    ID_Circuito INT PRIMARY KEY,
    Barrio VARCHAR(50),
    Accesible BOOLEAN,
    Localidad VARCHAR(50),
    Departamento VARCHAR(50),
    ID_Establecimiento INT,
    FOREIGN KEY (ID_Establecimiento) REFERENCES Establecimiento(ID_Establecimiento)
);

CREATE TABLE Ciudadano (
    CI INT PRIMARY KEY,
    Fecha_Nacimiento DATE,
    ID_Circuito INT,
    FOREIGN KEY (CI) REFERENCES Persona(CI),
    FOREIGN KEY (ID_Circuito) REFERENCES Circuito(ID_Circuito)
);

CREATE TABLE Miembro_Mesa (
    CI INT PRIMARY KEY,
    Organismo_Estado VARCHAR(100),
    FOREIGN KEY (CI) REFERENCES Persona(CI)
);

CREATE TABLE Agente_Policial (
    CI INT PRIMARY KEY,
    Comisaria VARCHAR(50),
    ID_Establecimiento INT,
    FOREIGN KEY (CI) REFERENCES Persona(CI),
    FOREIGN KEY (ID_Establecimiento) REFERENCES Establecimiento(ID_Establecimiento)
);

CREATE TABLE Eleccion (
    ID_Eleccion INT PRIMARY KEY,
    Fecha DATE,
    Tipo VARCHAR(50)
);

CREATE TABLE Candidato (
    CI INT PRIMARY KEY,
    Cargo_Postulado VARCHAR(50),
    FOREIGN KEY (CI) REFERENCES Persona(CI)
);

CREATE TABLE Partido_Politico (
    ID_Partido_Politico INT PRIMARY KEY,
    Nombre VARCHAR(100),
    Direccion_Sede VARCHAR(100),
    CI_Presidente INT,
    CI_Vicepresidente INT,
    FOREIGN KEY (CI_Presidente) REFERENCES Persona(CI),
    FOREIGN KEY (CI_Vicepresidente) REFERENCES Persona(CI)
);

CREATE TABLE Lista (
    Numero_Lista INT PRIMARY KEY,
    Organ VARCHAR(50),
    Departamento VARCHAR(50),
    ID_Partido_Politico INT,
    CI INT,
    FOREIGN KEY (ID_Partido_Politico) REFERENCES Partido_Politico(ID_Partido_Politico),
    FOREIGN KEY (CI) REFERENCES Candidato(CI)
);

CREATE TABLE Voto (
    ID_Voto INT PRIMARY KEY,
    Fecha_Hora_Emision TIMESTAMP,
    Observado BOOLEAN,
    Estado VARCHAR(50),
    ID_Eleccion INT,
    ID_Circuito INT,
    Numero_Lista INT,
    FOREIGN KEY (ID_Eleccion) REFERENCES Eleccion(ID_Eleccion),
    FOREIGN KEY (ID_Circuito) REFERENCES Circuito(ID_Circuito),
    FOREIGN KEY (Numero_Lista) REFERENCES Lista(Numero_Lista)
);

CREATE TABLE Voto_Papeleta (
    ID_Papeleta INT,
    ID_Voto INT,
    PRIMARY KEY (ID_Papeleta, ID_Voto),
    FOREIGN KEY (ID_Papeleta) REFERENCES Papeleta(ID_Papeleta),
    FOREIGN KEY (ID_Voto) REFERENCES Voto(ID_Voto)
);

CREATE TABLE Papeleta (
    ID_Papeleta INT PRIMARY KEY,
    Tipo VARCHAR(50),
    Color VARCHAR(50),
    ID_Eleccion INT,
    FOREIGN KEY (ID_Eleccion) REFERENCES Eleccion(ID_Eleccion)
);

CREATE TABLE Presentan (
    CI INT,
    ID_Eleccion INT,
    PRIMARY KEY (CI, ID_Eleccion),
    FOREIGN KEY (CI) REFERENCES Candidato(CI),
    FOREIGN KEY (ID_Eleccion) REFERENCES Eleccion(ID_Eleccion)
);

CREATE TABLE Integra (
    CI INT,
    ID_Circuito INT,
    Cargo VARCHAR(50),
    PRIMARY KEY (CI, ID_Circuito),
    FOREIGN KEY (CI) REFERENCES Miembro_Mesa(CI),
    FOREIGN KEY (ID_Circuito) REFERENCES Circuito(ID_Circuito)
);

CREATE TABLE Contiene (
    CI INT,
    Numero_Lista INT,
    PRIMARY KEY (CI, Numero_Lista),
    FOREIGN KEY (CI) REFERENCES Candidato(CI),
    FOREIGN KEY (Numero_Lista) REFERENCES Lista(Numero_Lista)
);


INSERT INTO persona (ci, nombre_completo, numero, serie) VALUES
(12345678, 'Ana López', 1234, 5678),
(23456789, 'Carlos Méndez', 2345, 6789),
(34567890, 'María Pérez', 3456, 7890),
(45678901, 'Luis Fernández', 4567, 8901);

UPDATE persona SET numero = '099123456' WHERE ci = 12345678;
UPDATE persona SET numero = '098765432' WHERE ci = 23456789;
UPDATE persona SET numero = '091112233' WHERE ci = 34567890;
UPDATE persona SET numero = '094998877' WHERE ci = 45678901;

-- Script completo de INSERT para sistema electoral
-- Ejecutar en orden para respetar foreign keys

-- Limpiar datos existentes en orden de dependencias
DELETE FROM Voto_Papeleta;
DELETE FROM Voto;
DELETE FROM Contiene;
DELETE FROM Integra;
DELETE FROM Presentan;
DELETE FROM Papeleta;
DELETE FROM Agente_Policial;
DELETE FROM Miembro_Mesa;
DELETE FROM Ciudadano;
DELETE FROM Lista;
DELETE FROM Candidato;
DELETE FROM Partido_Politico;
DELETE FROM Persona;
DELETE FROM Circuito;
DELETE FROM Establecimiento;
DELETE FROM Eleccion;

-- 1. Establecimiento
INSERT INTO Establecimiento (ID_Establecimiento, Tipo, Zona, Departamento, Nombre, Direccion)
VALUES
(1, 'Escuela', 'Centro', 'Montevideo', 'Escuela José Pedro Varela', 'Mercedes 1234'),
(2, 'Liceo', 'Este', 'Canelones', 'Liceo Departamental', 'Artigas 567'),
(3, 'Centro Comunal', 'Norte', 'Maldonado', 'Centro Comunal Zonal', 'Sarandi 890'),
(4, 'Policlínica', 'Sur', 'Colonia', 'Policlínica del Barrio', 'Treinta y Tres 345'),
(5, 'Club', 'Oeste', 'Montevideo', 'Club Social y Deportivo', 'Bulevar Batlle 678');

-- 2. Circuito
INSERT INTO Circuito (ID_Circuito, Barrio, Accesible, Localidad, Departamento, ID_Establecimiento)
VALUES
(1, 'Centro', TRUE, 'Montevideo', 'Montevideo', 1),
(2, 'Pocitos', TRUE, 'Montevideo', 'Montevideo', 5),
(3, 'Canelones', FALSE, 'Canelones', 'Canelones', 2),
(4, 'Punta del Este', TRUE, 'Maldonado', 'Maldonado', 3),
(5, 'Colonia del Sacramento', FALSE, 'Colonia', 'Colonia', 4);

-- 3. Eleccion
INSERT INTO Eleccion (ID_Eleccion, Fecha, Tipo)
VALUES
(1, '2024-10-27', 'Elecciones Nacionales'),
(2, '2024-11-24', 'Balotaje Presidencial'),
(3, '2025-05-10', 'Elecciones Departamentales'),
(4, '2025-10-26', 'Elecciones Generales'),
(5, '2025-11-30', 'Referéndum Nacional');

-- 4. Persona
INSERT INTO Persona (CI, Nombre_Completo, Numero, Serie)
VALUES
(12345678, 'Juan Pérez García', '1234567', 'A'),
(87654321, 'María González López', '7654321', 'B'),
(11111111, 'Carlos Rodríguez Silva', '1111111', 'A'),
(22222222, 'Ana Martínez Fernández', '2222222', 'C'),
(33333333, 'Luis Sánchez Torres', '3333333', 'B'),
(44444444, 'Patricia Álvarez Castro', '4444444', 'A'),
(55555555, 'Roberto Díaz Mendoza', '5555555', 'C'),
(66666666, 'Carmen Vega Morales', '6666666', 'B'),
(77777777, 'Diego Herrera Ramos', '7777777', 'A'),
(88888888, 'Lucía Torres Jiménez', '8888888', 'B');


-- 5. Partido_Politico
INSERT INTO Partido_Politico (ID_Partido_Politico, Nombre, Direccion_Sede, CI_Presidente, CI_Vicepresidente)
VALUES
(1, 'Partido Colorado', 'Av. Libertador 1234', 12345678, 87654321),
(2, 'Partido Nacional', 'Calle Uruguay 567', 11111111, 22222222),
(3, 'Frente Amplio', 'Mercedes 1234', 33333333, 44444444),
(4, 'Cabildo Abierto', 'Av. Brasil 890', 55555555, 66666666),
(5, 'Partido Independiente', 'Rincón 345', 77777777, 88888888);

-- 6. Candidato
INSERT INTO Candidato (CI, Cargo_Postulado)
VALUES
(12345678, 'Presidente'),
(87654321, 'Vicepresidente'),
(11111111, 'Presidente'),
(22222222, 'Vicepresidente'),
(33333333, 'Presidente'),
(44444444, 'Vicepresidente'),
(55555555, 'Senador'),
(66666666, 'Diputado'),
(77777777, 'Intendente'),
(88888888, 'Alcalde');

-- 7. Lista
INSERT INTO Lista (Numero_Lista, Organ, Departamento, ID_Partido_Politico, CI)
VALUES
(101, 'Senado', 'Montevideo', 1, 12345678),
(201, 'Senado', 'Montevideo', 2, 11111111),
(301, 'Senado', 'Montevideo', 3, 33333333),
(102, 'Diputados', 'Montevideo', 1, 87654321),
(202, 'Diputados', 'Canelones', 2, 22222222),
(401, 'Senado', 'Maldonado', 4, 55555555),
(402, 'Diputados', 'Maldonado', 4, 66666666),
(501, 'Intendencia', 'Colonia', 5, 77777777),
(302, 'Intendencia', 'Montevideo', 3, 88888888);

-- 8. Ciudadano
INSERT INTO Ciudadano (CI, Fecha_Nacimiento, ID_Circuito)
VALUES
(12345678, '1980-05-15', 1),
(87654321, '1975-12-20', 2),
(11111111, '1985-03-10', 3),
(22222222, '1990-08-25', 4),
(44444444, '1982-11-30', 5),
(77777777, '1978-07-18', 1),
(88888888, '1987-04-22', 2);

-- 9. Miembro_Mesa
INSERT INTO Miembro_Mesa (CI, Organismo_Estado)
VALUES
(33333333, 'Corte Electoral'),
(55555555, 'Ministerio del Interior'),
(66666666, 'Corte Electoral');

-- 10. Agente_Policial
INSERT INTO Agente_Policial (CI, Comisaria, ID_Establecimiento)
VALUES
(77777777, '1ra Seccional', 1),
(88888888, '5ta Seccional', 2);

-- 11. Papeleta
INSERT INTO Papeleta (ID_Papeleta, Tipo, Color, ID_Eleccion)
VALUES
(1, 'Presidencial', 'Blanca', 1),
(2, 'Senatorial', 'Amarilla', 1),
(3, 'Diputados', 'Rosa', 1),
(4, 'Presidencial', 'Blanca', 2),
(5, 'Departamental', 'Verde', 3);

-- 12. Voto
INSERT INTO Voto (ID_Voto, Fecha_Hora_Emision, Observado, Estado, ID_Eleccion, ID_Circuito, Numero_Lista)
VALUES
(1, '2024-10-27 08:30:00', FALSE, 'Válido', 1, 1, 101),
(2, '2024-10-27 09:15:00', FALSE, 'Válido', 1, 1, 201),
(3, '2024-10-27 10:45:00', TRUE, 'Observado', 1, 2, 301),
(4, '2024-10-27 11:20:00', FALSE, 'Válido', 1, 3, 101),
(5, '2024-10-27 14:30:00', FALSE, 'Anulado', 1, 4, NULL),
(6, '2024-10-27 15:45:00', FALSE, 'Válido', 1, 5, 401),
(7, '2024-10-27 16:20:00', FALSE, 'Válido', 1, 2, 302),
(8, '2024-10-27 17:10:00', TRUE, 'Recurrido', 1, 1, 501);

-- 13. Relaciones - Presentan (Candidato presenta en Elección)
INSERT INTO Presentan (CI, ID_Eleccion)
VALUES
(12345678, 1),
(87654321, 1),
(11111111, 1),
(22222222, 1),
(33333333, 1),
(44444444, 1),
(55555555, 3),
(66666666, 3),
(77777777, 3),
(88888888, 5);

-- 14. Relaciones - Integra (Miembro Mesa integra Circuito)
INSERT INTO Integra (CI, ID_Circuito, Cargo)
VALUES
(33333333, 1, 'Presidente de Mesa'),
(55555555, 2, 'Secretario de Mesa'),
(66666666, 3, 'Presidente de Mesa'),
(33333333, 4, 'Vocal'),
(55555555, 5, 'Presidente de Mesa');

-- 15. Relaciones - Contiene (Lista contiene Candidatos)
INSERT INTO Contiene (CI, Numero_Lista)
VALUES
(12345678, 101),
(87654321, 102),
(11111111, 201),
(22222222, 202),
(33333333, 301),
(88888888, 302),
(55555555, 401),
(66666666, 402),
(77777777, 501);


-- Verificar datos insertados
SELECT 'Establecimiento' as tabla, COUNT(*) as registros FROM Establecimiento
UNION ALL
SELECT 'Circuito', COUNT(*) FROM Circuito
UNION ALL
SELECT 'Elección', COUNT(*) FROM Eleccion
UNION ALL
SELECT 'Persona', COUNT(*) FROM Persona
UNION ALL
SELECT 'Partido_Politico', COUNT(*) FROM Partido_Politico
UNION ALL
SELECT 'Candidato', COUNT(*) FROM Candidato
UNION ALL
SELECT 'Lista', COUNT(*) FROM Lista
UNION ALL
SELECT 'Ciudadano', COUNT(*) FROM Ciudadano
UNION ALL
SELECT 'Voto', COUNT(*) FROM Voto;

ALTER TABLE persona ADD COLUMN password VARCHAR(100);

-- Establecer contraseña por defecto para todos los usuarios
UPDATE Persona SET password = '123';

