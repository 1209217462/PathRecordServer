create database pathrecord;
use pathrecord;

create table record (
  id integer NOT NULL AUTO_INCREMENT,
  username varchar(255) not null ,
  distance VARCHAR(255) NOT NULL ,
  duration VARCHAR(255) NOT NULL ,
  averagespeed VARCHAR(255) NOT NULL ,
  pathline  TEXT NOT NULL ,
  startpoint VARCHAR(255) NOT NULL ,
  endpoint VARCHAR(255) NOT NULL ,
  date DATETIME,
  primary key (id));

create table user (
  id integer NOT NULL AUTO_INCREMENT,
  username varchar(255) not null,
  password varchar(255) not null,
  recordnum INTEGER NOT NULL  DEFAULT 0,
  primary key (id));

show tables;

create trigger add_record after insert
on record for each row
begin
  update user set recordnum = user.recordnum + 1 where username = new.username;
end;

create trigger delete_record after delete
on record for each row
begin
  update user set recordnum = user.recordnum - 1 where username = old.username;
end;

SHOW TRIGGERS;