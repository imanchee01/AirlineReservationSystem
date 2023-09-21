-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server Version:               11.1.2-MariaDB - mariadb.org binary distribution
-- Server Betriebssystem:        Win64
-- HeidiSQL Version:             12.3.0.6589
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Exportiere Datenbank Struktur für airline
CREATE DATABASE IF NOT EXISTS `airline` /*!40100 DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci */;
USE `airline`;

-- Exportiere Struktur von Tabelle airline.user
CREATE TABLE IF NOT EXISTS `user` (
  `userId` int(10) NOT NULL AUTO_INCREMENT,
  `user_password` varchar(50) NOT NULL,
  `user_type` enum('Employee','Client') DEFAULT 'Client',
  `user_email` varchar(50) NOT NULL,
  `user_name` varchar(100) NOT NULL,
  PRIMARY KEY (`userId`),
  UNIQUE KEY `user_email` (`user_email`),
  CONSTRAINT `CONSTRAINT_1` CHECK (`user_email` like '%@%.%')
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Exportiere Daten aus Tabelle airline.user: ~4 rows (ungefähr)
INSERT INTO `user` (`userId`, `user_password`, `user_type`, `user_email`, `user_name`) VALUES
	(27, 'password1', 'Employee', 'employee1@example.com', 'John Doe'),
	(28, 'password2', 'Client', 'client1@example.com', 'Jane Smith'),
	(29, 'password3', 'Client', 'client2@example.com', 'Bob Johnson'),
	(30, 'password4', 'Client', 'client3@example.com', 'Elena Evergreen');

-- Exportiere Struktur von Tabelle airline.client
CREATE TABLE IF NOT EXISTS `client` (
  `clientId` int(11) DEFAULT NULL,
  `miles` float DEFAULT 0,
  `tier` enum('bronze','silver','gold') DEFAULT 'bronze',
  KEY `clientId` (`clientId`),
  CONSTRAINT `client_ibfk_1` FOREIGN KEY (`clientId`) REFERENCES `user` (`userId`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Exportiere Daten aus Tabelle airline.client: ~3 rows (ungefähr)
INSERT INTO `client` (`clientId`, `miles`, `tier`) VALUES
	(28, 450, 'bronze'),
	(29, 1300, 'silver'),
	(30, 0, 'bronze');

-- Exportiere Struktur von Tabelle airline.employee
CREATE TABLE IF NOT EXISTS `employee` (
  `employeeId` int(11) DEFAULT NULL,
  KEY `employeeId` (`employeeId`),
  CONSTRAINT `employee_ibfk_1` FOREIGN KEY (`employeeId`) REFERENCES `user` (`userId`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Exportiere Daten aus Tabelle airline.employee: ~1 rows (ungefähr)
INSERT INTO `employee` (`employeeId`) VALUES
	(27);

-- Exportiere Struktur von Tabelle airline.aircraft
CREATE TABLE IF NOT EXISTS `aircraft` (
  `aircraftId` int(11) NOT NULL AUTO_INCREMENT,
  `aircraft_model` varchar(30) NOT NULL,
  `aircraft_capacity` int(11) NOT NULL,
  `aircraft_firstclass` enum('n','y') NOT NULL,
  PRIMARY KEY (`aircraftId`),
  CONSTRAINT `CONSTRAINT_1` CHECK (`aircraft_capacity` >= 0)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Exportiere Daten aus Tabelle airline.aircraft: ~28 rows (ungefähr)
INSERT INTO `aircraft` (`aircraftId`, `aircraft_model`, `aircraft_capacity`, `aircraft_firstclass`) VALUES
	(1, 'Boeing 737-800', 189, 'y'),
	(2, 'Airbus A320', 5, 'y'),
	(3, 'Boeing 777-300ER', 365, 'y'),
	(4, 'Airbus A330-300', 290, 'y'),
	(5, 'Embraer E190', 100, 'n'),
	(6, 'Boeing 787-9', 290, 'y'),
	(7, 'Airbus A350-900', 325, 'y'),
	(8, 'Boeing 747-400', 416, 'y'),
	(9, 'Embraer E175', 76, 'n'),
	(10, 'Bombardier Q400', 78, 'n'),
	(11, 'Airbus A380', 853, 'y'),
	(12, 'Boeing 757-200', 200, 'y'),
	(13, 'Airbus A321', 236, 'y'),
	(14, 'Boeing 767-300ER', 242, 'y'),
	(15, 'Bombardier CRJ700', 78, 'n'),
	(16, 'Airbus A319', 124, 'n'),
	(17, 'Embraer E145', 50, 'n'),
	(18, 'Airbus A330-200', 246, 'y'),
	(19, 'Boeing 737 MAX 8', 189, 'n'),
	(20, 'Airbus A319neo', 140, 'n'),
	(21, 'Boeing 787-10', 330, 'y'),
	(22, 'Embraer E195-E2', 132, 'n'),
	(23, 'Bombardier CS300', 135, 'n'),
	(24, 'Airbus A321XLR', 206, 'n'),
	(25, 'Boeing 767-400ER', 245, 'y'),
	(26, 'Airbus A220-300', 160, 'n'),
	(27, 'Embraer E170', 78, 'n'),
	(28, 'Boeing 757-300', 243, 'y');

-- Exportiere Struktur von Tabelle airline.airport
CREATE TABLE IF NOT EXISTS `airport` (
  `airportId` varchar(4) NOT NULL,
  `airport_location` varchar(50) NOT NULL,
  `airport_name` varchar(100) NOT NULL,
  PRIMARY KEY (`airportId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Exportiere Daten aus Tabelle airline.airport: ~29 rows (ungefähr)
INSERT INTO `airport` (`airportId`, `airport_location`, `airport_name`) VALUES
	('AMS', 'Amsterdam', 'Amsterdam Airport Schiphol'),
	('ARN', 'Stockholm', 'Stockholm Arlanda Airport'),
	('ATH', 'Athens', 'Athens International Airport Eleftherios Venizelos'),
	('BCN', 'Barcelona', 'Barcelona–El Prat Airport'),
	('BEG', 'Belgrade', 'Belgrade Nikola Tesla Airport'),
	('BHX', 'Birmingham', 'Birmingham Airport'),
	('BRU', 'Brussels', 'Brussels Airport'),
	('BUD', 'Budapest', 'Budapest Ferenc Liszt International Airport'),
	('CDG', 'Paris', 'Charles de Gaulle Airport'),
	('CPH', 'Copenhagen', 'Copenhagen Airport'),
	('DUB', 'Dublin', 'Dublin Airport'),
	('FCO', 'Rome', 'Leonardo da Vinci–Fiumicino Airport'),
	('FRA', 'Frankfurt', 'Frankfurt Airport'),
	('GLA', 'Glasgow', 'Glasgow Airport'),
	('IST', 'Istanbul', 'Istanbul Airport'),
	('LHR', 'London', 'London Heathrow Airport'),
	('LIS', 'Lisbon', 'Lisbon Airport'),
	('MAD', 'Madrid', 'Adolfo Suárez Madrid–Barajas Airport'),
	('MUC', 'Munich', 'Munich Airport'),
	('OSL', 'Oslo', 'Oslo Gardermoen Airport'),
	('OTP', 'Bucharest', 'Henri Coanda International Airport'),
	('PRG', 'Prague', 'Václav Havel Airport Prague'),
	('PRN', 'Pristina', 'Pristina International Airport'),
	('SKG', 'Thessaloniki', 'Thessaloniki Airport'),
	('SOF', 'Sofia', 'Sofia Airport'),
	('VIE', 'Vienna', 'Vienna International Airport'),
	('WAW', 'Warsaw', 'Warsaw Chopin Airport'),
	('ZAG', 'Zagreb', 'Zagreb Airport'),
	('ZRH', 'Zurich', 'Zurich Airport');

-- Exportiere Struktur von Tabelle airline.flights
CREATE TABLE IF NOT EXISTS `flights` (
  `flightcode` int(11) NOT NULL AUTO_INCREMENT,
  `flight_miles` float NOT NULL,
  `flight_source` varchar(4) NOT NULL,
  `flight_destination` varchar(4) NOT NULL,
  `flight_weekday` enum('monday','tuesday','wednesday','thursday','friday','saturday','sunday') NOT NULL,
  `flight_arrTime` time NOT NULL,
  `flight_depTime` time NOT NULL,
  `flight_aircraftId` int(11) DEFAULT NULL,
  PRIMARY KEY (`flightcode`),
  KEY `flight_aircraftId` (`flight_aircraftId`),
  KEY `flight_source` (`flight_source`),
  KEY `flight_destination` (`flight_destination`),
  CONSTRAINT `flights_ibfk_1` FOREIGN KEY (`flight_aircraftId`) REFERENCES `aircraft` (`aircraftId`) ON DELETE NO ACTION ON UPDATE CASCADE,
  CONSTRAINT `flights_ibfk_2` FOREIGN KEY (`flight_source`) REFERENCES `airport` (`airportId`) ON DELETE NO ACTION ON UPDATE CASCADE,
  CONSTRAINT `flights_ibfk_3` FOREIGN KEY (`flight_destination`) REFERENCES `airport` (`airportId`) ON DELETE NO ACTION ON UPDATE CASCADE,
  CONSTRAINT `CONSTRAINT_1` CHECK (`flight_miles` >= 0)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Exportiere Daten aus Tabelle airline.flights: ~52 rows (ungefähr)
INSERT INTO `flights` (`flightcode`, `flight_miles`, `flight_source`, `flight_destination`, `flight_weekday`, `flight_arrTime`, `flight_depTime`, `flight_aircraftId`) VALUES
	(1, 409, 'FRA', 'AMS', 'monday', '09:20:00', '08:00:00', 1),
	(2, 1134, 'FRA', 'ARN', 'tuesday', '06:00:00', '09:00:00', 2),
	(3, 1286, 'FRA', 'ATH', 'wednesday', '11:00:00', '09:00:00', 3),
	(4, 750, 'FRA', 'BCN', 'thursday', '19:00:00', '16:00:00', 4),
	(5, 636, 'FRA', 'BEG', 'friday', '14:30:00', '12:30:00', 5),
	(6, 563, 'FRA', 'BHX', 'saturday', '13:45:00', '11:45:00', 6),
	(7, 254, 'FRA', 'BRU', 'sunday', '08:50:00', '07:30:00', 7),
	(8, 633, 'FRA', 'BUD', 'monday', '17:10:00', '15:30:00', 8),
	(9, 259, 'FRA', 'CDG', 'tuesday', '14:55:00', '14:15:00', 9),
	(10, 474, 'FRA', 'CPH', 'wednesday', '17:35:00', '16:00:00', 10),
	(11, 664, 'FRA', 'DUB', 'thursday', '15:45:00', '13:45:00', 11),
	(12, 688, 'FRA', 'FCO', 'friday', '16:30:00', '14:30:00', 12),
	(13, 396, 'FRA', 'LHR', 'saturday', '09:55:00', '08:45:00', 13),
	(14, 1187, 'FRA', 'LIS', 'sunday', '19:00:00', '16:00:00', 14),
	(15, 880, 'FRA', 'MAD', 'monday', '19:15:00', '17:15:00', 15),
	(16, 186, 'FRA', 'MUC', 'tuesday', '11:45:00', '10:45:00', 16),
	(17, 993, 'FRA', 'OSL', 'wednesday', '14:50:00', '13:00:00', 17),
	(18, 1057, 'FRA', 'OTP', 'thursday', '16:30:00', '13:30:00', 18),
	(19, 313, 'FRA', 'PRG', 'friday', '15:00:00', '13:30:00', 19),
	(20, 883, 'FRA', 'PRN', 'saturday', '21:00:00', '18:00:00', 20),
	(21, 1244, 'FRA', 'SKG', 'sunday', '17:30:00', '14:30:00', 21),
	(22, 1039, 'FRA', 'SOF', 'monday', '12:45:00', '09:45:00', 22),
	(23, 394, 'FRA', 'VIE', 'tuesday', '13:40:00', '12:30:00', 23),
	(24, 545, 'FRA', 'WAW', 'wednesday', '13:45:00', '11:45:00', 24),
	(25, 414, 'FRA', 'ZAG', 'thursday', '13:35:00', '12:15:00', 25),
	(26, 251, 'FRA', 'ZRH', 'friday', '09:20:00', '08:00:00', 26),
	(27, 409, 'AMS', 'FRA', 'monday', '12:30:00', '11:00:00', 1),
	(28, 1134, 'ARN', 'FRA', 'tuesday', '17:30:00', '14:30:00', 2),
	(29, 1286, 'ATH', 'FRA', 'wednesday', '22:00:00', '19:00:00', 3),
	(30, 750, 'BCN', 'FRA', 'thursday', '13:30:00', '10:30:00', 4),
	(31, 636, 'BEG', 'FRA', 'friday', '17:15:00', '15:15:00', 5),
	(32, 563, 'BHX', 'FRA', 'saturday', '16:45:00', '14:45:00', 6),
	(33, 254, 'BRU', 'FRA', 'sunday', '11:50:00', '10:30:00', 7),
	(34, 633, 'BUD', 'FRA', 'monday', '13:00:00', '11:00:00', 8),
	(35, 259, 'CDG', 'FRA', 'tuesday', '13:30:00', '12:00:00', 9),
	(36, 474, 'CPH', 'FRA', 'wednesday', '14:30:00', '13:00:00', 10),
	(37, 664, 'DUB', 'FRA', 'thursday', '20:00:00', '18:00:00', 11),
	(38, 688, 'FCO', 'FRA', 'friday', '11:30:00', '08:30:00', 12),
	(39, 396, 'LHR', 'FRA', 'saturday', '12:35:00', '11:15:00', 13),
	(40, 1187, 'LIS', 'FRA', 'sunday', '22:30:00', '19:30:00', 14),
	(41, 880, 'MAD', 'FRA', 'monday', '15:45:00', '12:45:00', 15),
	(42, 186, 'MUC', 'FRA', 'tuesday', '17:00:00', '16:00:00', 16),
	(43, 993, 'OSL', 'FRA', 'wednesday', '11:50:00', '09:30:00', 17),
	(44, 1057, 'OTP', 'FRA', 'thursday', '20:00:00', '17:00:00', 18),
	(45, 313, 'PRG', 'FRA', 'friday', '12:30:00', '11:00:00', 19),
	(46, 883, 'PRN', 'FRA', 'saturday', '16:45:00', '13:45:00', 20),
	(47, 1244, 'SKG', 'FRA', 'sunday', '21:15:00', '18:15:00', 21),
	(48, 1039, 'SOF', 'FRA', 'monday', '17:15:00', '14:15:00', 22),
	(49, 394, 'VIE', 'FRA', 'tuesday', '11:10:00', '10:00:00', 23),
	(50, 545, 'WAW', 'FRA', 'wednesday', '17:15:00', '15:15:00', 24),
	(51, 414, 'ZAG', 'FRA', 'thursday', '14:50:00', '14:30:00', 25),
	(52, 251, 'ZRH', 'FRA', 'friday', '13:50:00', '12:30:00', 26),
	(57, 820, 'FRA', 'GLA', 'monday', '16:30:00', '13:30:00', 27),
	(58, 820, 'GLA', 'FRA', 'tuesday', '20:45:00', '17:45:00', 27),
	(59, 540, 'FRA', 'FCO', 'wednesday', '14:25:00', '12:45:00', 28),
	(60, 540, 'FCO', 'FRA', 'thursday', '17:35:00', '16:00:00', 28);

-- Exportiere Struktur von Tabelle airline.ticketprice
CREATE TABLE IF NOT EXISTS `ticketprice` (
  `pricecategory` enum('short distance','middle distance','long distance') NOT NULL,
  `economy_price` float NOT NULL,
  `business_price` float NOT NULL,
  `firstclass_price` float DEFAULT NULL,
  `luggage_price` float NOT NULL CHECK (`economy_price` >= 0),
  PRIMARY KEY (`pricecategory`),
  CONSTRAINT `CONSTRAINT_1` CHECK (`business_price` >= 0),
  CONSTRAINT `CONSTRAINT_2` CHECK (`firstclass_price` >= 0 or NULL),
  CONSTRAINT `CONSTRAINT_3` CHECK (`luggage_price` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Exportiere Daten aus Tabelle airline.ticketprice: ~3 rows (ungefähr)
INSERT INTO `ticketprice` (`pricecategory`, `economy_price`, `business_price`, `firstclass_price`, `luggage_price`) VALUES
	('short distance', 70, 120, 200, 20),
	('middle distance', 150, 250, 370, 35),
	('long distance', 250, 450, 700, 60);

-- Exportiere Struktur von Tabelle airline.tickets
CREATE TABLE IF NOT EXISTS `tickets` (
  `ticket_name` varchar(100) NOT NULL,
  `ticket_date` date NOT NULL,
  `ticket_miles` float NOT NULL,
  `ticketId` int(11) NOT NULL AUTO_INCREMENT,
  `ticket_purchaseDate` date NOT NULL,
  `ticket_userId` int(11) DEFAULT NULL,
  `ticket_flightcode` int(11) DEFAULT NULL,
  `ticket_class` enum('economy','business','first-class') NOT NULL,
  PRIMARY KEY (`ticketId`),
  KEY `ticket_userId` (`ticket_userId`),
  KEY `ticket_flightcode` (`ticket_flightcode`),
  CONSTRAINT `tickets_ibfk_1` FOREIGN KEY (`ticket_userId`) REFERENCES `user` (`userId`) ON DELETE NO ACTION ON UPDATE CASCADE,
  CONSTRAINT `tickets_ibfk_2` FOREIGN KEY (`ticket_flightcode`) REFERENCES `flights` (`flightcode`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Exportiere Daten aus Tabelle airline.tickets: ~7 rows (ungefähr)
INSERT INTO `tickets` (`ticket_name`, `ticket_date`, `ticket_miles`, `ticketId`, `ticket_purchaseDate`, `ticket_userId`, `ticket_flightcode`, `ticket_class`) VALUES
	('John Doe', '2023-09-20', 100, 2, '2023-09-20', 28, 1, 'economy'),
	('John Doe ', '2023-09-20', 150, 4, '2023-09-20', 28, 2, 'economy'),
	('John Doe', '2023-09-20', 50, 5, '2023-09-20', 28, 2, 'economy'),
	('Jane Smith', '2023-09-20', 50, 7, '2023-09-20', 28, 2, 'economy'),
	('Bob Johnson', '2023-09-20', 100, 8, '2023-09-20', 29, 2, 'economy'),
	('Bob Johnson', '2023-09-20', 100, 9, '2023-09-20', 29, 2, 'economy'),
	('Bob Johnson', '2023-09-20', 100, 10, '2023-09-20', 29, 4, 'economy');

-- Exportiere Struktur von Tabelle airline.request
CREATE TABLE IF NOT EXISTS `request` (
  `requestId` int(11) NOT NULL AUTO_INCREMENT,
  `request_status` enum('pending','in process','completed') NOT NULL DEFAULT 'pending',
  `request_ticketId` int(11) DEFAULT NULL,
  `request_clientId` int(11) NOT NULL,
  `request_employeeId` int(11) DEFAULT NULL,
  PRIMARY KEY (`requestId`),
  KEY `request_ticketId` (`request_ticketId`),
  KEY `request_clientId` (`request_clientId`),
  KEY `request_employeeId` (`request_employeeId`),
  CONSTRAINT `request_ibfk_1` FOREIGN KEY (`request_ticketId`) REFERENCES `tickets` (`ticketId`) ON DELETE NO ACTION ON UPDATE CASCADE,
  CONSTRAINT `request_ibfk_2` FOREIGN KEY (`request_clientId`) REFERENCES `client` (`clientId`) ON DELETE NO ACTION ON UPDATE CASCADE,
  CONSTRAINT `request_ibfk_3` FOREIGN KEY (`request_employeeId`) REFERENCES `employee` (`employeeId`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Exportiere Daten aus Tabelle airline.request: ~0 rows (ungefähr)

-- Exportiere Struktur von Trigger airline.AddMilesToClientsMiles
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `AddMilesToClientsMiles` BEFORE INSERT ON `tickets` FOR EACH ROW BEGIN
	UPDATE client SET miles = miles + NEW.ticket_miles
	WHERE clientId = NEW.ticket_userId;
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Exportiere Struktur von Trigger airline.AddUserToEMployeeOrCLient
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER AddUserToEMployeeOrCLient
AFTER INSERT ON user  
FOR EACH ROW 
BEGIN
	IF NEW.user_type = 'Employee' THEN
		INSERT INTO employee (employeeId) VALUES (NEW.userId);
	ELSE
		INSERT INTO client (clientId) VALUES (NEW.userId);
	END IF;
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Exportiere Struktur von Trigger airline.check_aircraft_availability
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `check_aircraft_availability`
BEFORE INSERT ON `flights`
FOR EACH ROW
BEGIN
    DECLARE aircraft_count INT;
    
    -- Zählen die Anzahl der Flüge mit dem ausgewählten Flugzeug an diesem Tag und Zeitraum
    SET aircraft_count = (
        SELECT COUNT(*)
        FROM flights
        WHERE flight_aircraftId = NEW.flight_aircraftId
        AND flight_weekday = NEW.flight_weekday
        AND NEW.flight_depTime BETWEEN flight_depTime AND ADDTIME(flight_arrTime, '01:00:00')
    );
    
    -- Wenn es bereits einen Flug mit dem Flugzeug an diesem Tag im selben Zeitraum gibt, verhindere das Einfügen
    IF aircraft_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Das ausgewählte Flugzeug wird bereits an diesem Tag im selben Zeitraum verwendet.';
    END IF;
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Exportiere Struktur von Trigger airline.check_ticket_update_capacity
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `check_ticket_update_capacity` BEFORE INSERT ON `tickets` FOR EACH ROW BEGIN
    DECLARE max_capacity INT;
    DECLARE ticket_count INT;
    
    -- Get the count of already purchased tickets for the same flight on the same date
    SELECT COUNT(*) INTO ticket_count
    FROM tickets
    WHERE ticket_flightcode = NEW.ticket_flightcode
    AND ticket_date = NEW.ticket_date;

    -- Get the maximum capacity of the aircraft for the corresponding flight
    SELECT aircraft_capacity INTO max_capacity
    FROM aircraft
    WHERE aircraftId = (
        SELECT flight_aircraftId
        FROM flights
        WHERE flightcode = NEW.ticket_flightcode
    );

    -- Check if the ticket count exceeds the maximum capacity
    IF ticket_count >= max_capacity THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Flight is already fully booked for this date and aircraft.';
    END IF;
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Exportiere Struktur von Trigger airline.RemoveMilesFromClientsMiles
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `RemoveMilesFromClientsMiles` BEFORE DELETE ON `tickets` FOR EACH ROW BEGIN
	UPDATE client SET miles = miles - OLD.ticket_miles
	WHERE clientId = OLD.ticket_userId;
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Exportiere Struktur von Trigger airline.update_clientTier_deleteTicket
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `update_clientTier_deleteTicket` AFTER DELETE ON `tickets` FOR EACH ROW BEGIN
    DECLARE client_miles FLOAT;
    DECLARE new_tier ENUM('bronze', 'silver', 'gold');
    
    -- Get the current miles of the client
    SELECT miles INTO client_miles
    FROM client
    WHERE clientId = OLD.ticket_userId;

    -- Determine the new tier based on the miles
    IF client_miles >= 10000 THEN
        SET new_tier = 'gold';
    ELSEIF client_miles >= 1000 THEN
        SET new_tier = 'silver';
    ELSE
        SET new_tier = 'bronze';
    END IF;
    
    -- Update the client's tier
    UPDATE client
    SET tier = new_tier
    WHERE clientId = OLD.ticket_userId;
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Exportiere Struktur von Trigger airline.update_clientTier_insertTicket
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `update_clientTier_insertTicket` AFTER INSERT ON `tickets` FOR EACH ROW BEGIN
    DECLARE client_miles FLOAT;
    DECLARE new_tier ENUM('bronze', 'silver', 'gold');
    
    -- Get the current miles of the client
    SELECT miles INTO client_miles
    FROM client
    WHERE clientId = NEW.ticket_userId;

    -- Determine the new tier based on the miles
    IF client_miles >= 10000 THEN
        SET new_tier = 'gold';
    ELSEIF client_miles >= 1000 THEN
        SET new_tier = 'silver';
    ELSE
        SET new_tier = 'bronze';
    END IF;
    
    -- Update the client's tier
    UPDATE client
    SET tier = new_tier
    WHERE clientId = NEW.ticket_userId;
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
