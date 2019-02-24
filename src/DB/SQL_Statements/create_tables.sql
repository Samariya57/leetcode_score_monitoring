-- Drop active_fellows table if exists;
-- Create active_fellows table if not exists;
DROP TABLE IF EXISTS active_fellows CASCADE;

CREATE TABLE IF NOT EXISTS active_fellows (
	leetcode_user_name				varchar(50)	PRIMARY KEY ,
	first_name						varchar(50),
	last_name						varchar(50),
	email							varchar(50),
	program							varchar(5),
	session_location			    varchar(5),
	session_code				    varchar(5)
);
