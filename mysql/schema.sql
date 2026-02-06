-- =====================
-- 1. TABLA USUARIOS
-- =====================
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    email VARCHAR(180) NOT NULL UNIQUE,
    password VARCHAR(120) NOT NULL,
    rol ENUM('admin', 'cliente') NOT NULL DEFAULT 'cliente',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================
-- 2. TABLA MESAS
-- =====================
CREATE TABLE mesas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero_mesa INT NOT NULL UNIQUE,
    capacidad INT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

-- =====================
-- 3. TABLA MENÚS (UNO POR FECHA)
-- =====================
CREATE TABLE menus (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL UNIQUE,
    nombre VARCHAR(160) NOT NULL,
    descripcion TEXT,
    foto_url VARCHAR(500),
    precio DECIMAL(10, 2) NOT NULL
);

-- =====================
-- 4. TABLA RESERVAS
-- =====================
CREATE TABLE reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    mesa_id INT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    party_size INT NOT NULL,
    estado ENUM(
        'confirmada',
        'cancelada',
        'completada'
    ) NOT NULL DEFAULT 'confirmada',
    resena TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
    FOREIGN KEY (mesa_id) REFERENCES mesas (id)
);

-- ADMIN
INSERT INTO
    usuarios (nombre, email, password, rol)
VALUES (
        'Admin Principal',
        'admin@restaurante.com',
        'admin123',
        'admin'
    );

-- CLIENTES
INSERT INTO
    usuarios (nombre, email, password, rol)
VALUES (
        'Juan Perez',
        'juan@email.com',
        'cliente123',
        'cliente'
    ),
    (
        'Maria Lopez',
        'maria@email.com',
        'cliente123',
        'cliente'
    );

-- MESAS
INSERT INTO
    mesas (numero_mesa, capacidad)
VALUES (1, 2),
    (2, 2),
    (3, 4),
    (4, 4),
    (5, 6);

-- MENÚS
INSERT INTO
    menus (
        fecha,
        nombre,
        descripcion,
        foto_url,
        precio
    )
VALUES (
        '2024-05-22',
        'Menú del Día: Pasta',
        'Espaguetis al pesto, ensalada caprese y bebida.',
        'https://images.unsplash.com/photo-1473093226795-af9932fe5856?auto=format&fit=crop&w=600',
        12.50
    ),
    (
        '2024-05-23',
        'Menú Especial: Hamburguesa',
        'Hamburguesa de buey, patatas rústicas y postre.',
        'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=600',
        14.00
    ),
    (
        '2024-05-24',
        'Menú Saludable: Bowl',
        'Bowl de quinoa con salmón, aguacate y zumo natural.',
        'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=600',
        13.50
    );