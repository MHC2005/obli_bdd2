CREATE TABLE Persona (
    CI VARCHAR(20) PRIMARY KEY,
    NombreCompleto VARCHAR(100),
    Numero VARCHAR(20),
    Serie VARCHAR(20)
);
-- Tabla Elección
CREATE TABLE Eleccion (
    IDEleccion SERIAL PRIMARY KEY,
    Fecha DATE,
    Tipo VARCHAR(50)
);

-- Tabla Establecimiento
CREATE TABLE Establecimiento (
    IDEstablecimiento SERIAL PRIMARY KEY,
    Tipo VARCHAR(50),
    Zona VARCHAR(50),
    Departamento VARCHAR(50),
    Nombre VARCHAR(100),
    Direccion VARCHAR(150)
);

-- Tabla Circuito
CREATE TABLE Circuito (
    IDCircuito SERIAL PRIMARY KEY,
    Barrio VARCHAR(100),
    Accesible BOOLEAN,
    Localidad VARCHAR(100),
    Departamento VARCHAR(100),
    IDEstablecimiento INT,
    FOREIGN KEY (IDEstablecimiento) REFERENCES Establecimiento(IDEstablecimiento)
);

-- Tabla Ciudadano
CREATE TABLE Ciudadano (
    CI VARCHAR(20) PRIMARY KEY,
    FechaNacimiento DATE,
    IDCircuito INT,
    FOREIGN KEY (CI) REFERENCES Persona(CI),
    FOREIGN KEY (IDCircuito) REFERENCES Circuito(IDCircuito)
);

-- Tabla MiembroMesa
CREATE TABLE MiembroMesa (
    CI VARCHAR(20) PRIMARY KEY,
    OrganismoEstado VARCHAR(100),
    FOREIGN KEY (CI) REFERENCES Persona(CI)
);

-- Tabla AgentePolicial
CREATE TABLE AgentePolicial (
    CI VARCHAR(20) PRIMARY KEY,
    Comisaria VARCHAR(100),
    IDEstablecimiento INT,
    FOREIGN KEY (CI) REFERENCES Persona(CI),
    FOREIGN KEY (IDEstablecimiento) REFERENCES Establecimiento(IDEstablecimiento)
);

-- Tabla PartidoPolitico
CREATE TABLE PartidoPolitico (
    IDPartidoPolitico SERIAL PRIMARY KEY,
    Nombre VARCHAR(100),
    DireccionSede VARCHAR(150),
    Presidente VARCHAR(100),
    Vicepresidente VARCHAR(100)
);

-- Tabla Candidato
CREATE TABLE Candidato (
    CI VARCHAR(20),
    IDEleccion INT,
    Lista VARCHAR(50),
    IDPartidoPolitico INT,
    CargoPostulado VARCHAR(100),
    PRIMARY KEY (CI, IDEleccion),
    FOREIGN KEY (CI) REFERENCES Persona(CI),
    FOREIGN KEY (IDEleccion) REFERENCES Eleccion(IDEleccion),
    FOREIGN KEY (IDPartidoPolitico) REFERENCES PartidoPolitico(IDPartidoPolitico)
);

-- Tabla Presentan
CREATE TABLE Presentan (
    CI VARCHAR(20),
    IDEleccion INT,
    PRIMARY KEY (CI, IDEleccion),
    FOREIGN KEY (CI) REFERENCES Persona(CI),
    FOREIGN KEY (IDEleccion) REFERENCES Eleccion(IDEleccion)
);

-- Tabla Papeleta
CREATE TABLE Papeleta (
    IDPapeleta SERIAL PRIMARY KEY,
    Tipo VARCHAR(50),
    ListaAsociada VARCHAR(50),
    Color VARCHAR(50)
);

-- Tabla Voto
CREATE TABLE Voto (
    IDVoto SERIAL PRIMARY KEY,
    FechaHoraEmision TIMESTAMP,
    Observado BOOLEAN,
    Estado VARCHAR(50),
    IDEleccion INT,
    IDCircuito INT,
    FOREIGN KEY (IDEleccion) REFERENCES Eleccion(IDEleccion),
    FOREIGN KEY (IDCircuito) REFERENCES Circuito(IDCircuito)
);

-- Tabla VotoPapeleta
CREATE TABLE VotoPapeleta (
    IDPapeleta INT,
    IDVoto INT,
    PRIMARY KEY (IDPapeleta, IDVoto),
    FOREIGN KEY (IDPapeleta) REFERENCES Papeleta(IDPapeleta),
    FOREIGN KEY (IDVoto) REFERENCES Voto(IDVoto)
);

-- Tabla Integra
CREATE TABLE Integra (
    CI VARCHAR(20),
    IDCircuito INT,
    Cargo VARCHAR(50),
    PRIMARY KEY (CI, IDCircuito),
    FOREIGN KEY (CI) REFERENCES Persona(CI),
    FOREIGN KEY (IDCircuito) REFERENCES Circuito(IDCircuito)
);

-- Tabla Lista
CREATE TABLE Lista (
    NumeroLista VARCHAR(50) PRIMARY KEY,
    Organo VARCHAR(50),
    CandidatoApoyado VARCHAR(100),
    Departamento VARCHAR(100),
    IDPartidoPolitico INT,
    CI VARCHAR(20),
    FOREIGN KEY (IDPartidoPolitico) REFERENCES PartidoPolitico(IDPartidoPolitico),
    FOREIGN KEY (CI) REFERENCES Persona(CI)
);

-- Tabla Contiene
CREATE TABLE Contiene (
    CI VARCHAR(20),
    NumeroLista VARCHAR(50),
    PRIMARY KEY (CI, NumeroLista),
    FOREIGN KEY (CI) REFERENCES Persona(CI),
    FOREIGN KEY (NumeroLista) REFERENCES Lista(NumeroLista)
);