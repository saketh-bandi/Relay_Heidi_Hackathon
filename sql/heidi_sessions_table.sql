-- Heidi Health Scribe Sessions Table
-- Stores AI-generated medical transcripts and clinical notes from Heidi Health API
-- Links to OpenEMR patient records via pid

CREATE TABLE IF NOT EXISTS heidi_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pid BIGINT NOT NULL,
    heidi_session_id VARCHAR(255) NOT NULL,
    session_name VARCHAR(255),
    session_gist VARCHAR(500),
    transcript TEXT,
    consult_note TEXT,
    consult_note_heading VARCHAR(255),
    duration INT COMMENT 'Session duration in seconds',
    session_date DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_heidi_session (heidi_session_id),
    KEY idx_patient (pid),
    KEY idx_session_date (session_date),
    CONSTRAINT fk_heidi_sessions_patient FOREIGN KEY (pid) 
        REFERENCES patient_data(pid) 
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
