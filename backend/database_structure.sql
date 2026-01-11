-- =====================================================
-- FLAT BOOKING SYSTEM - COMPLETE DATABASE STRUCTURE
-- =====================================================

-- Create Database
CREATE DATABASE IF NOT EXISTS rental_portal;
USE rental_portal;

-- =====================================================
-- 1. REGISTER TABLE
-- =====================================================
CREATE TABLE register (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('USER', 'ADMIN') NOT NULL DEFAULT 'USER',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_role (role)
);

-- =====================================================
-- 2. FLATS TABLE
-- =====================================================
CREATE TABLE flats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flat_no VARCHAR(50) UNIQUE NOT NULL,
    flat_type VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    status ENUM('Available', 'Booked') DEFAULT 'Available',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_flat_no (flat_no),
    INDEX idx_status (status)
);

-- =====================================================
-- 3. BOOKING TABLE
-- =====================================================
CREATE TABLE booking (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_email VARCHAR(255) NOT NULL,
    flat_no VARCHAR(50) NOT NULL,
    status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Foreign Key Constraints
    FOREIGN KEY (user_email) REFERENCES register(email) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (flat_no) REFERENCES flats(flat_no) ON DELETE CASCADE ON UPDATE CASCADE,
    
    -- Indexes
    INDEX idx_user_email (user_email),
    INDEX idx_flat_no (flat_no),
    INDEX idx_status (status)
);

-- =====================================================
-- 4. ADMIN TABLE
-- =====================================================
CREATE TABLE admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    admin_email VARCHAR(255) NOT NULL,
    admin_password VARCHAR(255) NOT NULL,
    approved_user_id INT,
    approval_status ENUM('Approved', 'Not Approved') DEFAULT 'Not Approved',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Foreign Key Constraints
    FOREIGN KEY (admin_email) REFERENCES register(email) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (approved_user_id) REFERENCES register(id) ON DELETE SET NULL ON UPDATE CASCADE,
    
    -- Indexes
    INDEX idx_admin_email (admin_email),
    INDEX idx_approved_user_id (approved_user_id),
    INDEX idx_approval_status (approval_status)
);

-- =====================================================
-- SAMPLE DATA INSERTION
-- =====================================================

-- Insert Sample Users
INSERT INTO register (email, password, role) VALUES
('admin@rental.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.PJ/..G', 'ADMIN'),
('user1@rental.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.PJ/..G', 'USER'),
('user2@rental.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.PJ/..G', 'USER');

-- Insert Sample Flats
INSERT INTO flats (flat_no, flat_type, price, status) VALUES
('A101', '1BHK', 15000.00, 'Available'),
('A102', '2BHK', 25000.00, 'Available'),
('A103', '3BHK', 35000.00, 'Available'),
('B201', '1BHK', 18000.00, 'Available'),
('B202', '2BHK', 28000.00, 'Booked');

-- Insert Sample Bookings
INSERT INTO booking (user_email, flat_no, status) VALUES
('user1@rental.com', 'A101', 'Pending'),
('user2@rental.com', 'B202', 'Approved');

-- Insert Sample Admin Records
INSERT INTO admin (admin_email, admin_password, approved_user_id, approval_status) VALUES
('admin@rental.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.PJ/..G', 2, 'Approved');

-- =====================================================
-- USEFUL QUERIES FOR APPLICATION
-- =====================================================

-- 1. Login Validation Query
-- SELECT * FROM register WHERE email = ? AND password = ?;

-- 2. Get All Available Flats
-- SELECT * FROM flats WHERE status = 'Available';

-- 3. Get User Bookings
-- SELECT b.*, f.flat_type, f.price FROM booking b 
-- JOIN flats f ON b.flat_no = f.flat_no 
-- WHERE b.user_email = ?;

-- 4. Admin - Get All Pending Bookings
-- SELECT b.*, r.email as user_email, f.flat_type, f.price 
-- FROM booking b 
-- JOIN register r ON b.user_email = r.email 
-- JOIN flats f ON b.flat_no = f.flat_no 
-- WHERE b.status = 'Pending';

-- 5. Update Booking Status
-- UPDATE booking SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?;

-- 6. Update Flat Status when Booked
-- UPDATE flats SET status = 'Booked', updated_at = CURRENT_TIMESTAMP WHERE flat_no = ?;

-- =====================================================
-- TRIGGERS FOR AUTOMATIC UPDATES
-- =====================================================

-- Trigger to update flat status when booking is approved
DELIMITER //
CREATE TRIGGER update_flat_status_on_booking_approval
AFTER UPDATE ON booking
FOR EACH ROW
BEGIN
    IF NEW.status = 'Approved' AND OLD.status != 'Approved' THEN
        UPDATE flats SET status = 'Booked' WHERE flat_no = NEW.flat_no;
    END IF;
    
    IF NEW.status = 'Rejected' AND OLD.status = 'Approved' THEN
        UPDATE flats SET status = 'Available' WHERE flat_no = NEW.flat_no;
    END IF;
END//
DELIMITER ;

-- =====================================================
-- VIEWS FOR EASY DATA ACCESS
-- =====================================================

-- View for User Dashboard
CREATE VIEW user_dashboard AS
SELECT 
    b.id as booking_id,
    b.user_email,
    b.flat_no,
    f.flat_type,
    f.price,
    b.status as booking_status,
    b.created_at as booking_date
FROM booking b
JOIN flats f ON b.flat_no = f.flat_no;

-- View for Admin Dashboard
CREATE VIEW admin_dashboard AS
SELECT 
    b.id as booking_id,
    r.email as user_email,
    r.role as user_role,
    b.flat_no,
    f.flat_type,
    f.price,
    b.status as booking_status,
    b.created_at as booking_date,
    b.updated_at as last_updated
FROM booking b
JOIN register r ON b.user_email = r.email
JOIN flats f ON b.flat_no = f.flat_no;

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================

-- Additional composite indexes for better performance
CREATE INDEX idx_booking_user_status ON booking(user_email, status);
CREATE INDEX idx_flats_type_status ON flats(flat_type, status);
CREATE INDEX idx_register_email_role ON register(email, role);

-- =====================================================
-- CONSTRAINTS AND VALIDATIONS
-- =====================================================

-- Add check constraints
ALTER TABLE flats ADD CONSTRAINT chk_price_positive CHECK (price > 0);
ALTER TABLE register ADD CONSTRAINT chk_email_format CHECK (email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');

-- =====================================================
-- END OF DATABASE STRUCTURE
-- =====================================================