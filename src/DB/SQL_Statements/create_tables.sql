-- Drop active_fellows table if exists;
-- Create active_fellows table if not exists;
DROP TABLE IF EXISTS active_fellows CASCADE;

CREATE TABLE IF NOT EXISTS active_fellows (
	leetcode_user_name				varchar(50)	PRIMARY KEY ,
	first_name						varchar(50),
	last_name						varchar(50),
	email							varchar(50),
	program						   varchar(5),
	session_location			    varchar(5),
	session_code				    varchar(5),
	job_searching					boolean
);



-- Drop leetcode_records table if exists;
-- Create leetcode_records table if not exists;
DROP TABLE IF EXISTS leetcode_records CASCADE;

CREATE TABLE IF NOT EXISTS leetcode_records (
	record_id 						varchar(70) PRIMARY KEY ,
	user_name						varchar(50)	REFERENCES active_fellows(leetcode_user_name),
	num_solved						INTEGER,
	num_accepts						INTEGER,
	num_submissions			    	INTEGER,
	accepted_percentage				NUMERIC,
	finished_contests				INTEGER,
	record_date						DATE
);



