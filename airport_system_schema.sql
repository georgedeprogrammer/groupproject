-- WARNING: This script DROPS and recreates the tables below.
-- Running it again permanently deletes records currently stored in those tables.
-- Select the airport_system database in phpMyAdmin before running this script.

CREATE DATABASE IF NOT EXISTS airport_system;
USE airport_system;

DROP TABLE IF EXISTS Contact_Messages;
DROP TABLE IF EXISTS Newsletter_Subscribers;
DROP TABLE IF EXISTS Online_CheckIn;
DROP TABLE IF EXISTS Reports;
DROP TABLE IF EXISTS Tickets;
DROP TABLE IF EXISTS Parcel_Sending;
DROP TABLE IF EXISTS Flight_Booking;
DROP TABLE IF EXISTS user_logins;
DROP TABLE IF EXISTS customer_details;

CREATE TABLE customer_details (
    ID_Numbber INT PRIMARY KEY,
    Full_Name VARCHAR(100),
    Passport_Number VARCHAR(100),
    Email VARCHAR(100),
    Contact VARCHAR(20)
);

-- Kept separate from customer_details as requested.
CREATE TABLE user_logins (
    Login_ID INT AUTO_INCREMENT PRIMARY KEY,
    ID_Number INT NULL,
    Username VARCHAR(100) NOT NULL UNIQUE,
    Email VARCHAR(150) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    User_Role ENUM('admin', 'employee', 'customer')
        NOT NULL DEFAULT 'customer'
);

CREATE TABLE Flight_Booking (
    Passport_Number VARCHAR(13),
    Depature_Date DATE,
    Return_Date DATE,
    Passangers INT NULL,
    Destination VARCHAR(100),
    Class ENUM('economy', 'bussiness', 'first')
);

CREATE TABLE Parcel_Sending (
    ParcelID INT AUTO_INCREMENT PRIMARY KEY,
    Sender_Name VARCHAR(100),
    Recipient_Name VARCHAR(100),
    Parcel_Description VARCHAR(20),
    Weight DECIMAL(10,2),
    Destination VARCHAR(100)
);

CREATE TABLE Tickets (
    TicketID INT AUTO_INCREMENT PRIMARY KEY,
    Ticket_Number VARCHAR(30),
    Passport_Number VARCHAR(13),
    Flight_Date DATE,
    Amount INT
);

CREATE TABLE Reports (
    ReportID INT AUTO_INCREMENT PRIMARY KEY,
    Full_Name VARCHAR(100),
    ID_Numbber INT,
    Issue VARCHAR(250)
);

CREATE TABLE Online_CheckIn (
    CheckIn_ID INT AUTO_INCREMENT PRIMARY KEY,
    Passport_Number VARCHAR(13),
    Full_Name VARCHAR(100),
    Ticket_Number VARCHAR(30),
    Checked_As ENUM('canceled', 'reschedule', 'coming')
);

-- Extra tables for the Newsletter and Contact forms already present in the frontend.
CREATE TABLE Newsletter_Subscribers (
    Subscriber_ID INT AUTO_INCREMENT PRIMARY KEY,
    Email VARCHAR(150) NOT NULL UNIQUE,
    Subscribed_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Contact_Messages (
    Message_ID INT AUTO_INCREMENT PRIMARY KEY,
    Full_Name VARCHAR(100) NOT NULL,
    Email VARCHAR(150) NOT NULL,
    Message TEXT NOT NULL,
    Submitted_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
