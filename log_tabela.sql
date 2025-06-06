CREATE TABLE IF NOT EXISTS api_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    api_key VARCHAR(255),
    firma VARCHAR(255),
    vreme DATETIME DEFAULT CURRENT_TIMESTAMP,
    ulaz_json TEXT,
    rezultat_json TEXT,
    ip_adresa VARCHAR(45)
);

SELECT *FROM api_logs;