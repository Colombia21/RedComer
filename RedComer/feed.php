<?php
ini_set('display_errors', 1);
error_reporting(E_ALL);

header("Content-Type: application/json; charset=UTF-8");

$conexion = new mysqli("localhost", "root", "", "redcomer");

if ($conexion->connect_error) {
    http_response_code(500);
    echo json_encode(["error" => "Conexión fallida: " . $conexion->connect_error]);
    exit;
}

$sql = "
    SELECT p.id, u.usuario, p.descripcion, p.fecha,
           COUNT(l.id) AS total_likes
    FROM publicaciones p
    JOIN usuarios u ON p.usuario_id = u.id
    LEFT JOIN likes l ON p.id = l.publicacion_id
    GROUP BY p.id, u.usuario, p.descripcion, p.fecha
    ORDER BY p.fecha DESC
";

$resultado = $conexion->query($sql);
$datos = [];

if ($resultado) {
    while ($fila = $resultado->fetch_assoc()) {
        $datos[] = $fila;
    }
    echo json_encode($datos, JSON_UNESCAPED_UNICODE);
} else {
    http_response_code(500);
    echo json_encode(["error" => "Error en la consulta: " . $conexion->error]);
}

$conexion->close();
