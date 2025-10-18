DROP TABLE IF EXISTS usuario;
CREATE TABLE usuario (
    idusuario SERIAL NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL,
    usuario VARCHAR(100) NOT NULL,
    clave VARCHAR(100) NOT NULL,
    clave_vence DATE DEFAULT NULL,
    clave_ultima VARCHAR(100) DEFAULT NULL,
    estado SMALLINT NULL DEFAULT 1,
    usuario_creo VARCHAR(200),
    fecha_creo TIMESTAMP DEFAULT NULL,
    usuario_modifico VARCHAR(200),
    fecha_modifico TIMESTAMP DEFAULT NULL,
    CONSTRAINT pk_usuario PRIMARY KEY (idusuario)
);