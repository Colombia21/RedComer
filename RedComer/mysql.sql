CREATE DATABASE IF NOT EXISTS redcomer;

USE redcomer;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(100) NOT NULL UNIQUE,
    correo VARCHAR(150) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS publicaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    contenido TEXT, 
    imagen VARCHAR(255),
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS carrito (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    publicacion_id INT NOT NULL,
    fecha_agregado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (publicacion_id) REFERENCES publicaciones(id),
    UNIQUE (usuario_id, publicacion_id)
);

ALTER TABLE publicaciones CHANGE contenido descripcion TEXT;

CREATE TABLE IF NOT EXISTS likes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    publicacion_id INT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (publicacion_id) REFERENCES publicaciones(id),
    UNIQUE (usuario_id, publicacion_id)
);


SELECT p.id, u.usuario, p.descripcion, p.imagen, p.fecha, 
       COUNT(l.id) AS total_likes
FROM publicaciones p
JOIN usuarios u ON p.usuario_id = u.id
LEFT JOIN likes l ON p.id = l.publicacion_id
GROUP BY p.id
ORDER BY p.fecha DESC;
