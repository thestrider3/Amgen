drop table columbiaamgen.Courses;
drop table columbiaamgen.References;
drop table columbiaamgen.studentData;
desc columbiaamgen.References;
delete from columbiaamgen.studentData where Username = ('shivani.b.gupta@gmail.com');
delete from columbiaamgen.References where Email like 'v.patanjali*';
select * from columbiaamgen.References where Email = 'v.patanjali@gmail.com';
update columbiaamgen.studentData set password='temp' where Username = ('v.patanjali@gmail.com');
select * from columbiaamgen.studentData;
select * from columbiaamgen.Mentors;
Insert into Mentors values (246,'')
select count(*) from columbiaamgen.Courses;
select * from columbiaamgen.References;
update columbiaamgen.studentData set Transcript=null where Username in ('shivani','tulika')
update columbiaamgen.studentData set UserType='Student' where Username in ('shivani','tulika')
update columbiaamgen.studentData set ApplicationStatus='IncompleteApplication' where Username in ('shivani','tulika')
update columbiaamgen.studentData set ApplicationStatus='UnderReview' where Username in ('shivani','tulika')
update columbiaamgen.studentData set ApplicationStatus='ReferencesRequired' 
Insert into columbiaamgen.studentData(Username,Password) values ('patan','temp')
Insert into columbiaamgen.studentData(Username,Password,UserType) values ('admin','temp','Admin')
select Transcript from columbiaamgen.studentData where username='shivani'
CREATE TABLE `columbiaamgen`.`studentData` (
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
  `Mentor1` VARCHAR(50) NULL,
  `Mentor2` VARCHAR(50) NULL,
  `Mentor3` VARCHAR(50) NULL,
  `Mentor4` VARCHAR(50) NULL,
  `Mentor5` VARCHAR(50) NULL,
  `Mentor6` VARCHAR(50) NULL,
  `Mentor7` VARCHAR(50) NULL,
  `Mentor8` VARCHAR(50) NULL,
  `Transcript` VARCHAR(200) NULL,
  `ApplicationStatus` VARCHAR(30) NULL,
  `ReviewWaiver` VARCHAR(5) NULL,
  `HowDidYouHearUniversityName` VARCHAR(50) NULL,
  `HowDidYouHearConferenceName` VARCHAR(100) NULL,
  `HowDidYouHearOtherUniversityName` VARCHAR(100) NULL,
  `HowDidYouHearOther` VARCHAR(100) NULL,
  `UserType` VARCHAR(45) NOT NULL DEFAULT 'Student',
  `EthnicityOther` VARCHAR(30) NULL,
  `PlaceOfBirth` VARCHAR(30) NULL,
  `AdvancedDegreeObjectiveOther` VARCHAR(30) NULL,
  PRIMARY KEY (`Username`));
  


CREATE TABLE `columbiaamgen`.`References` (
  `Username` VARCHAR(24) NOT NULL,
  `Name` VARCHAR(100) NULL,
  `Email` VARCHAR(100) NULL,
  `Status` VARCHAR(30) NULL,
  PRIMARY KEY (`UserName`,`Email`));

CREATE TABLE `columbiaamgen`.`Courses` (
  `UserId` VARCHAR(24) NOT NULL,
  `Title` VARCHAR(100) NOT NULL,
  `Credits` INT NULL,
  `Grade` VARCHAR(5) NULL,
  PRIMARY KEY (`UserId`, `Title`));
