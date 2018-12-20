-- Drop active_fellows table if exists;
-- Create active_fellows table if not exists;
DROP TABLE IF EXISTS active_fellows CASCADE;

CREATE TABLE IF NOT EXISTS active_fellows (
	leetcode_user_name				varchar(50)	PRIMARY KEY ,
	first_name						varchar(50),
	last_name						varchar(50),
	email							varchar(50),
	session_location			    varchar(50),
	session_code				    varchar(20)
);



-- Drop leetcode_records table if exists;
-- Create leetcode_records table if not exists;
DROP TABLE IF EXISTS leetcode_records CASCADE;

CREATE TABLE IF NOT EXISTS active_fellows (
	user_name						varchar(50)	REFERENCES active_fellows(leetcode_user_name),
	num_solved						INTEGER,
	num_accepts						INTEGER,
	num_submissions			    	INTEGER,
	solved_percentage				NUMERIC,
	finished_contests				INTEGER,
	record_date						DATE
);
