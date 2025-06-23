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
