-- MySQL Workbench Database Schema for Blood Donation System

CREATE DATABASE IF NOT EXISTS blood_donation_system;
USE blood_donation_system;

-- User Table
CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    blood_type VARCHAR(5),
    date_of_birth DATE,
    gender VARCHAR(10),
    address VARCHAR(200),
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code VARCHAR(20),
    country VARCHAR(100) DEFAULT 'United States',
    profile_image VARCHAR(200),
    is_donor BOOLEAN DEFAULT FALSE,
    is_admin BOOLEAN DEFAULT FALSE,
    is_verified BOOLEAN DEFAULT FALSE,
    last_donation DATETIME,
    donation_count INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Donations Table
CREATE TABLE IF NOT EXISTS donations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    donor_id INT NOT NULL,
    blood_type VARCHAR(5) NOT NULL,
    units FLOAT NOT NULL,
    donation_date DATETIME NOT NULL,
    next_eligible_date DATETIME,
    location VARCHAR(200),
    status VARCHAR(20) DEFAULT 'scheduled',
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (donor_id) REFERENCES user(id) ON DELETE CASCADE
);

-- Blood Requests Table
CREATE TABLE IF NOT EXISTS blood_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    requester_id INT NOT NULL,
    patient_name VARCHAR(100) NOT NULL,
    patient_age INT,
    patient_gender VARCHAR(20),
    blood_type VARCHAR(5) NOT NULL,
    units_required FLOAT NOT NULL,
    required_by DATETIME NOT NULL,
    hospital_name VARCHAR(200) NOT NULL,
    hospital_address TEXT,
    city VARCHAR(50) NOT NULL,
    contact_name VARCHAR(100) NOT NULL,
    contact_phone VARCHAR(15) NOT NULL,
    additional_notes TEXT,
    status VARCHAR(20) DEFAULT 'Pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (requester_id) REFERENCES user(id) ON DELETE CASCADE
);

-- Blood Inventory Table
CREATE TABLE IF NOT EXISTS blood_inventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    blood_type VARCHAR(5) NOT NULL UNIQUE,
    units_available INT DEFAULT 0,
    units_reserved INT DEFAULT 0,
    target_level FLOAT DEFAULT 100.0,
    critical_level FLOAT DEFAULT 10.0,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Initial Data for Blood Inventory
INSERT INTO blood_inventory (blood_type, units_available, units_reserved, target_level, critical_level) VALUES
('A+', 0, 0, 100.0, 10.0),
('A-', 0, 0, 100.0, 10.0),
('B+', 0, 0, 100.0, 10.0),
('B-', 0, 0, 100.0, 10.0),
('AB+', 0, 0, 100.0, 10.0),
('AB-', 0, 0, 100.0, 10.0),
('O+', 0, 0, 100.0, 10.0),
('O-', 0, 0, 100.0, 10.0)
ON DUPLICATE KEY UPDATE blood_type=blood_type;
