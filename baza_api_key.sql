DROP TABLE IF EXISTS api_keys;
CREATE TABLE api_keys (
    id INT AUTO_INCREMENT PRIMARY KEY,
    api_key VARCHAR(255) NOT NULL UNIQUE,
    firma VARCHAR(100), 
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO api_keys (api_key, owner) VALUES 
('abc123xyz', 'Firma A'),
('key456def', 'Firma B'),
('789ghiJKL', 'Logistika C'),
('token321MNO', 'Speditor D'),
('safeKey999', 'Test Korisnik');


SELECT * FROM api_keys;
