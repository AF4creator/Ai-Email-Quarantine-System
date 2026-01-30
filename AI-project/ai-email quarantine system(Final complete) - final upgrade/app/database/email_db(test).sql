CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    imap_server VARCHAR(255) NOT NULL,
    imap_port INT DEFAULT 993,
    imap_email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    imap_password_enc VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE quarantined_emails (
    email_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    message_uid VARCHAR(100) NOT NULL,
    sender VARCHAR(255),
    subject VARCHAR(255),
    body LONGTEXT,
    received_at VARCHAR(100),
    quarantined_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    classification VARCHAR(50),
    spam_score FLOAT,
    url_status VARCHAR(50),
    status VARCHAR(20) DEFAULT 'active',
    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);

CREATE TABLE scan_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    total_scanned INT NOT NULL,
    total_quarantined INT NOT NULL,
    total_suspicious INT NOT NULL,
    total_safe INT NOT NULL,
    scan_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);

CREATE TABLE whitelist (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    sender_email VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);
