--drop table if exists MemberProfile;
create table MemberProfile(
ID uniqueidentifier,
Email nvarchar(255) not null,
FName nvarchar(255) not null,
LName nvarchar(255) not null,
Interests nvarchar(255),
Major nvarchar(255),
GradYear int,
About nvarchar(MAX),
UserType nvarchar(50) not null,
primary key (ID));

--drop table if exists MajorGroup;
create table MajorGroup (
ID uniqueidentifier not null,
Title nvarchar(255) not null,
Email nvarchar(255) not null,
MemberID uniqueidentifier,
MeetupID uniqueidentifier,
primary key (ID),
foreign key (MemberID) references MemberProfile(ID),
foreign key (MeetupID) references Meetup(ID) on delete cascade);

--drop table if exists Meetup;
create table Meetup(
ID uniqueidentifier not null,
Title nvarchar(255) not null,
Place nvarchar(255),
TimeDate datetime,
Attendees uniqueidentifier,
primary key (ID),
foreign key (attendees) references MemberProfile(ID) on delete cascade);

--drop table if exists Interests;
create table Interests(
ID uniqueidentifier not null,
Title nvarchar(255) not null,
MemberID uniqueidentifier,
MeetupID uniqueidentifier,
primary key (ID),
foreign key (MemberID) references MemberProfile(ID),
foreign key (MeetupID) references Meetup(ID) on delete cascade);

