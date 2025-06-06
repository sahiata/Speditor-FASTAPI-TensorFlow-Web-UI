CREATE DATABASE IF NOT EXISTS spedicija;
USE spedicija;

CREATE TABLE IF NOT EXISTS log_predikcija (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vreme TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ulaz JSON,
    rezultat JSON,
    ip_adresa VARCHAR(45)
);

SELECT * FROM log_predikcija;