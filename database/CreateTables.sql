CREATE TABLE `amgen`.`LoginData` (
  `Username` VARCHAR(45) NULL,
  `Password` VARCHAR(45) NULL,
  `FirstName` VARCHAR(45) NULL,
  `LastName` VARCHAR(45) NULL,
  `UserType` VARCHAR(45) NOT NULL DEFAULT 'Student'
  PRIMARY KEY (`Username`));
  
CREATE TABLE `amgen`.`studentData` (
  `Username` VARCHAR(45) NULL,
  `Password` VARCHAR(45) NULL,
  `FirstName` VARCHAR(45) NULL,
  `LastName` VARCHAR(45) NULL,
  `DOB` VARCHAR(20) NULL,
  `Email` VARCHAR(100) NULL,
  `AlternativeEmail` VARCHAR(100) NULL,
  `Phone` VARCHAR(20) NULL,
  `PermStreetAdr1` VARCHAR(50) NULL,
  `PermStreetAdr2` VARCHAR(45) NULL,
  `PermanentCity` VARCHAR(45) NULL,
  `PermanentState` VARCHAR(45) NULL,
  `PermanentZipCode` INT NULL,
  `CampusAdr1` VARCHAR(45) NULL,
  `CampusAdr2` VARCHAR(45) NULL,
  `CampusCity` VARCHAR(45) NULL,
  `CampusState` VARCHAR(45) NULL,
  `CampusZipCode` INT NULL,
  `HomeCity` VARCHAR(45) NULL,
  `HomeState` VARCHAR(45) NULL,
  `Gender` VARCHAR(1) NULL,
  `Ethnicity` VARCHAR(45) NULL,
  `CitizenshipStatus` VARCHAR(45) NULL,
  `MotherDegree` VARCHAR(45) NULL,
  `FatherDegree` VARCHAR(45) NULL,
  `ClassCompletedSpring` VARCHAR(25) NULL,
  `GraduationMonth` VARCHAR(45) NULL,
  `GraduationYear` INT NULL,
  `CumulativeGPA` FLOAT NULL,
  `AdvancedDegreeObjective` VARCHAR(45) NULL,
  `IsUndergraduateResearchProgramOffered` VARCHAR(5) NULL,
  `HowDidYouHear` VARCHAR(250) NULL,
  `AnyOtherAmgenScholarsSite` VARCHAR(5) NULL,
  `YesOtherAmgenScholarsSite` VARCHAR(100) NULL,
  `PastAmgenScholarParticipation` VARCHAR(5) NULL,
  `OriginalResearchPerformed` VARCHAR(5) NULL,
  `CanArriveAtColumbiaMemorialDay` VARCHAR(5) NULL,
  `ArriveAtColumbiaComments` VARCHAR(200) CHARACTER SET 'dec8' NULL,
  `CurrentlyAttendingUniversity` VARCHAR(45) NULL,
  `Major` VARCHAR(45) NULL,
  `DateSpringSemesterEnds` VARCHAR(20) NULL,
  `ScienceExperience` VARCHAR(750) NULL,
  `CareerPlans` VARCHAR(550) NULL,
  `AspirationNext20Yrs` VARCHAR(550) NULL,
  `Mentor1` VARCHAR(50) NULL,
  `Mentor2` VARCHAR(50) NULL,
  `Mentor3` VARCHAR(50) NULL,
  `Mentor4` VARCHAR(50) NULL,
  `Mentor5` VARCHAR(50) NULL,
  `Mentor6` VARCHAR(50) NULL,
  `Mentor7` VARCHAR(50) NULL,
  `Mentor8` VARCHAR(50) NULL,
  `Transcript` VARCHAR(500) NULL,
  `ApplicationStatus` VARCHAR(30) NULL,
  `ReviewWaiver` VARCHAR(5) NULL,
  `HowDidYouHearUniversityName` VARCHAR(50) NULL,
  `HowDidYouHearConferenceName` VARCHAR(100) NULL,
  `HowDidYouHearOtherUniversityName` VARCHAR(100) NULL,
  `HowDidYouHearOther` VARCHAR(100) NULL,
  `EthnicityOther` VARCHAR(30) NULL,
  `PlaceOfBirth` VARCHAR(30) NULL,
  `AdvancedDegreeObjectiveOther` VARCHAR(30) NULL,
  PRIMARY KEY (`Username`));
  


CREATE TABLE `amgen`.`References` (
  `Username` VARCHAR(24) NOT NULL,
  `Name` VARCHAR(100) NULL,
  `Email` VARCHAR(100) NULL,
  `Status` VARCHAR(30) NULL,
  `ReferalFilePath` VARCHAR(500) NULL,
  PRIMARY KEY (`UserName`,`Email`));

CREATE TABLE `amgen`.`Courses` (
  `UserId` VARCHAR(24) NOT NULL,
  `Title` VARCHAR(100) NOT NULL,
  `Credits` INT NULL,
  `Grade` VARCHAR(5) NULL,
  PRIMARY KEY (`UserId`, `Title`));

Insert into amgen.LoginData(Username,Password,UserType) values ('admin','temp','Admin')

CREATE TABLE `amgen`.`Mentors` (
  `Id` INT NOT NULL,
  `Name` VARCHAR(45) NULL,
  PRIMARY KEY (`Id`));