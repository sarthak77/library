PRAGMA FOREIGN_KEY = ON;



create table if not exists admins (
id integer primary key autoincrement,
username varchar(50) not null,
password varchar(100) not null,
phone varchar(50) not null,
email text not null

);


create table if not exists books (
name varchar(100) not null ,
id integer primary key autoincrement,
author varchar(50) not null ,
category text 



);



create table if not exists students (
id integer primary key autoincrement,
cardnum integer unique,
name varchar(50),
dob date,
doj date,
address text,
phone varchar(50),
borrowlimit integer default 2,
password varchar(150) not null,
email text not null


);


create table if not exists issue (
transID integer primary key autoincrement,
bookid integer,
studentid integer,
adminid integer,
issuedate date,
foreign key(bookid) references books(id) on update cascade on delete cascade,
foreign key(studentid) references students(id) on update cascade on delete cascade,
foreign key(adminid) references admins(id) on update cascade on delete cascade



);


create table if not exists issue_history (
transID integer primary key,
bookid integer,
studentid integer,
issuedbyid integer,
issueDate date,
returnDate date,
lateFees integer,
foreign key(bookid) references books(id) on update cascade on delete cascade,
foreign key(studentid) references students(id) on update cascade on delete cascade,
foreign key(issuedbyid) references admins(id) on update cascade on delete cascade



);


create table if not exists student_reg(
regID integer primary key autoincrement,
name varchar(50),
dob date,
address text,
phone varchar(10),
password varchar(150) not null,
email text not null

);

