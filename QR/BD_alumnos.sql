
CREATE TABLE BD_alumnos (
    id INT PRIMARY KEY IDENTITY(1,1),
    nombre NVARCHAR(255) NOT NULL,
    edad INT,
    carrera NVARCHAR(255),
    codigo_qr NVARCHAR(255)
);
