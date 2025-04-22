CREATE DATABASE redcomer;

USE redcomer;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(100) NOT NULL UNIQUE,
    correo VARCHAR(150) NOT NULL,
    password VARCHAR(255) NOT NULL
);
