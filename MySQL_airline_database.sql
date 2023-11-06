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

-- Exportiere Struktur von Tabelle airline.aircraft
CREATE TABLE IF NOT EXISTS `aircraft` (
  `aircraftId` int(11) NOT NULL AUTO_INCREMENT,
  `aircraft_model` varchar(30) NOT NULL,
  `aircraft_capacity` int(11) NOT NULL,
  `aircraft_firstclass` enum('n','y') NOT NULL,
  PRIMARY KEY (`aircraftId`),
  CONSTRAINT `CONSTRAINT_1` CHECK (`aircraft_capacity` >= 0)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Daten Export vom Benutzer nicht ausgewählt

-- Exportiere Struktur von Tabelle airline.airport
CREATE TABLE IF NOT EXISTS `airport` (
  `airportId` varchar(4) NOT NULL,
  `airport_location` varchar(50) NOT NULL,
  `airport_name` varchar(100) NOT NULL,
  PRIMARY KEY (`airportId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Daten Export vom Benutzer nicht ausgewählt

-- Exportiere Struktur von Tabelle airline.checkin_status
CREATE TABLE IF NOT EXISTS `checkin_status` (
  `ticketId` int(11) NOT NULL,
  `checkinstatus` enum('checkedin','notcheckedin') NOT NULL DEFAULT 'notcheckedin',
  KEY `FK__tickets` (`ticketId`),
  CONSTRAINT `FK__tickets` FOREIGN KEY (`ticketId`) REFERENCES `tickets` (`ticketId`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Daten Export vom Benutzer nicht ausgewählt

-- Exportiere Struktur von Tabelle airline.client
CREATE TABLE IF NOT EXISTS `client` (
  `clientId` int(11) DEFAULT NULL,
  `miles` float DEFAULT 0,
  `tier` enum('bronze','silver','gold') DEFAULT 'bronze',
  KEY `clientId` (`clientId`),
  CONSTRAINT `client_ibfk_1` FOREIGN KEY (`clientId`) REFERENCES `user` (`userId`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Daten Export vom Benutzer nicht ausgewählt

-- Exportiere Struktur von Tabelle airline.employee
CREATE TABLE IF NOT EXISTS `employee` (
  `employeeId` int(11) DEFAULT NULL,
  KEY `employeeId` (`employeeId`),
  CONSTRAINT `employee_ibfk_1` FOREIGN KEY (`employeeId`) REFERENCES `user` (`userId`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Daten Export vom Benutzer nicht ausgewählt

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
  KEY `flights_ibfk_1` (`flight_aircraftId`),
  KEY `flights_ibfk_2` (`flight_source`),
  KEY `flights_ibfk_3` (`flight_destination`),
  CONSTRAINT `flights_ibfk_1` FOREIGN KEY (`flight_aircraftId`) REFERENCES `aircraft` (`aircraftId`) ON UPDATE CASCADE,
  CONSTRAINT `flights_ibfk_2` FOREIGN KEY (`flight_source`) REFERENCES `airport` (`airportId`) ON UPDATE CASCADE,
  CONSTRAINT `flights_ibfk_3` FOREIGN KEY (`flight_destination`) REFERENCES `airport` (`airportId`) ON UPDATE CASCADE,
  CONSTRAINT `CONSTRAINT_1` CHECK (`flight_miles` >= 0)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Daten Export vom Benutzer nicht ausgewählt

-- Exportiere Struktur von Funktion airline.GetRemainingCapacity
DELIMITER //
CREATE FUNCTION `GetRemainingCapacity`(`flight_code` VARCHAR(255),
    `ticketdate` DATE
) RETURNS int(11)
BEGIN
    DECLARE max_capacity INT;
    DECLARE ticket_count INT;
    
    -- Get the count of already purchased tickets for the same flight on the same date
    SELECT COUNT(*) INTO ticket_count
    FROM tickets
    WHERE ticket_flightcode = flight_code
    AND ticket_date = ticketdate;
 
    -- Get the maximum capacity of the aircraft for the corresponding flight
    SELECT aircraft_capacity INTO max_capacity
    FROM aircraft
    WHERE aircraftId = (
       SELECT flight_aircraftId
       FROM flights
       WHERE flightcode = flight_code
       LIMIT 1
     );
    -- Calculate the remaining capacity
    IF ticket_count > max_capacity THEN
         RETURN 0; -- or any other appropriate value to indicate no remaining capacity
     ELSE
     RETURN max_capacity - ticket_count;
     END IF;
END//
DELIMITER ;

-- Exportiere Struktur von Tabelle airline.request
CREATE TABLE IF NOT EXISTS `request` (
  `requestId` int(11) NOT NULL AUTO_INCREMENT,
  `request_status` enum('pending','accepted','declined') NOT NULL DEFAULT 'pending',
  `request_ticketId` int(11) DEFAULT NULL,
  `request_clientId` int(11) NOT NULL,
  `request_employeeId` int(11) DEFAULT NULL,
  `request_information` text DEFAULT NULL,
  PRIMARY KEY (`requestId`),
  KEY `request_clientId` (`request_clientId`),
  KEY `request_employeeId` (`request_employeeId`),
  KEY `request_ibfk_1` (`request_ticketId`),
  CONSTRAINT `request_ibfk_1` FOREIGN KEY (`request_ticketId`) REFERENCES `tickets` (`ticketId`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `request_ibfk_2` FOREIGN KEY (`request_clientId`) REFERENCES `client` (`clientId`) ON DELETE NO ACTION ON UPDATE CASCADE,
  CONSTRAINT `request_ibfk_3` FOREIGN KEY (`request_employeeId`) REFERENCES `employee` (`employeeId`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=92 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Daten Export vom Benutzer nicht ausgewählt

-- Exportiere Struktur von Ereignis airline.ResetMilesAndTierEvent
DELIMITER //
CREATE EVENT `ResetMilesAndTierEvent` ON SCHEDULE EVERY 1 YEAR STARTS '2023-01-01 00:00:00' ON COMPLETION NOT PRESERVE ENABLE DO BEGIN
    DECLARE clientIdToUpdate INT;
    DECLARE currentMiles FLOAT;
    DECLARE currentTier ENUM('bronze', 'silver', 'gold');

    -- Erhalte die Kunden-ID, Meilen und Tier-Ebene des Kunden
    SELECT clientId, miles, tier
    INTO clientIdToUpdate, currentMiles, currentTier
    FROM client;

    -- Wenn die Meilen bereits 0 sind, erfolgt ein Tier-Downgrade
    IF currentMiles < 1000 THEN
      SET currentTier = 'bronze';
    ELSEIF currentMiles >= 1000 AND currentMiles< 10000 THEN
    	SET currentTier = 'silver';
    ELSE
	 	SET currentTier = 'gold';	
    END IF;

    -- Setze die Meilen auf 0 und aktualisiere die Tier-Ebene
    UPDATE client
    SET miles = 0, tier = currentTier
    WHERE clientId = clientIdToUpdate;
END//
DELIMITER ;

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

-- Daten Export vom Benutzer nicht ausgewählt

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
  `offer` enum('free coffee','free meal','complementary champagne') DEFAULT NULL,
  PRIMARY KEY (`ticketId`),
  KEY `ticket_userId` (`ticket_userId`),
  KEY `tickets_ibfk_2` (`ticket_flightcode`),
  CONSTRAINT `tickets_ibfk_1` FOREIGN KEY (`ticket_userId`) REFERENCES `user` (`userId`) ON DELETE NO ACTION ON UPDATE CASCADE,
  CONSTRAINT `tickets_ibfk_2` FOREIGN KEY (`ticket_flightcode`) REFERENCES `flights` (`flightcode`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Daten Export vom Benutzer nicht ausgewählt

-- Exportiere Struktur von Tabelle airline.user
CREATE TABLE IF NOT EXISTS `user` (
  `userId` int(10) NOT NULL AUTO_INCREMENT,
  `user_password` varchar(256) NOT NULL DEFAULT '0',
  `user_type` enum('Employee','Client') DEFAULT 'Client',
  `user_email` varchar(50) NOT NULL,
  `user_name` varchar(100) NOT NULL,
  PRIMARY KEY (`userId`),
  UNIQUE KEY `user_email` (`user_email`),
  CONSTRAINT `CONSTRAINT_1` CHECK (`user_email` like '%@%.%')
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Daten Export vom Benutzer nicht ausgewählt

-- Exportiere Struktur von Trigger airline.AddMilesToClientsMiles
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `AddMilesToClientsMiles` AFTER INSERT ON `tickets` FOR EACH ROW BEGIN
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

-- Exportiere Struktur von Trigger airline.checkin
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `checkin` AFTER INSERT ON `tickets` FOR EACH ROW BEGIN
	INSERT INTO checkin_status (ticketId) VALUES (NEW.ticketId);
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
