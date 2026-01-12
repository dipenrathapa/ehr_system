-- EHR System Database Schema
-- Run these commands in MySQL Workbench

-- Create the database
CREATE DATABASE IF NOT EXISTS ehr_system;
USE ehr_system;

-- Table: doctors
-- Stores doctor registration and login information
CREATE TABLE IF NOT EXISTS doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,  -- Stores bcrypt hashed password
    specialty VARCHAR(100),
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE doctors
ADD COLUMN reset_token VARCHAR(255) NULL;

-- Table: patients
-- Stores patient EHR data linked to a specific doctor
CREATE TABLE IF NOT EXISTS patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    doctor_id INT NOT NULL,                      -- Foreign key to doctors table
    
    -- Text fields
    full_name VARCHAR(100) NOT NULL,
    age INT,
    weight DECIMAL(5,2),                         -- Weight in kg
    height DECIMAL(5,2),                         -- Height in cm
    blood_type VARCHAR(5),
    phone VARCHAR(20),
    email VARCHAR(100),
    address TEXT,
    
    -- Radio field (Gender)
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    
    -- Checkbox fields (stored as boolean/tinyint)
    has_allergies TINYINT(1) DEFAULT 0,
    has_diabetes TINYINT(1) DEFAULT 0,
    has_hypertension TINYINT(1) DEFAULT 0,
    has_heart_disease TINYINT(1) DEFAULT 0,
    is_smoker TINYINT(1) DEFAULT 0,
    
    -- Date fields
    date_of_birth DATE,
    admission_date DATE,
    last_visit_date DATE,
    
    -- Textarea field
    medical_history TEXT,
    current_medications TEXT,
    diagnosis TEXT,
    treatment_notes TEXT,
    
    -- Image upload (stores file path)
    report_image VARCHAR(255),
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Foreign key constraint
    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE


);

-- Create indexes for better query performance
CREATE INDEX idx_patients_doctor ON patients(doctor_id);
CREATE INDEX idx_doctors_email ON doctors(email);



CREATE TABLE contact_inquiries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    message TEXT NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



CREATE TABLE sus_responses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    doctor_id INT NULL,  -- optional if you want to track which doctor took it
    q1 INT NOT NULL,
    q2 INT NOT NULL,
    q3 INT NOT NULL,
    q4 INT NOT NULL,
    q5 INT NOT NULL,
    q6 INT NOT NULL,
    q7 INT NOT NULL,
    q8 INT NOT NULL,
    q9 INT NOT NULL,
    q10 INT NOT NULL,
    sus_score FLOAT NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);