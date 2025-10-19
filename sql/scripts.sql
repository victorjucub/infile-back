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

-- World Nes API 1 57141da14ce84a72afcb1e64b6d3f588
-- World Nes API umg 0ae5dd5463864bb48015d971e9a37651
-- World Nes API sb 

-- NewsAPI.org 57141da14ce84a72afcb1e64b6d3f588

-- GNews API ec6e8ead31f8851aabc4b81344903019

-- id
-- title
-- text
-- summary
-- url
-- image
-- publish_date
-- author
-- category


DROP TABLE IF EXISTS noticias;
CREATE TABLE noticias (
    idnoticia SERIAL NOT NULL,
    idnoticiaref INT NOT NULL,
    titulo TEXT NULL DEFAULT NULL,
    texto TEXT NULL DEFAULT NULL,
    resumen TEXT NULL DEFAULT NULL,
    urlNoticia TEXT NULL DEFAULT NULL,
    imagen TEXT DEFAULT NULL,
    fecha_publicacion DATE DEFAULT NULL,
    autor TEXT DEFAULT NULL,
    categoria TEXT DEFAULT NULL,
    estado SMALLINT NULL DEFAULT 1,
    usuario_creo VARCHAR(200),
    fecha_creo TIMESTAMP DEFAULT NULL,
    usuario_modifico VARCHAR(200),
    fecha_modifico TIMESTAMP DEFAULT NULL,
    CONSTRAINT pk_noticia PRIMARY KEY (idnoticia)
);


DROP TABLE IF EXISTS refresh_tokens;
CREATE TABLE refresh_tokens (
    idtoken SERIAL PRIMARY KEY,
    idusuario INTEGER NOT NULL,
    token TEXT NOT NULL,
    estado BOOLEAN DEFAULT TRUE,
    fecha_creo TIMESTAMP DEFAULT NOW()
);