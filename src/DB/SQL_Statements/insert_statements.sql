-- Remove data from active_fellows if necessary
DELETE FROM active_fellows;

-- Upsert sample Data in the active_fellows table;
INSERT INTO active_fellows (leetcode_user_name, first_name, last_name, email, program, session_location, session_code, job_searching)
VALUES
 (
 'zl1761',
 'Heng',
 'Lee',
 'zl1761@nyu.edu',
 'DE',
 'NYC',
 '18c',
 True
 ) 
ON CONFLICT (leetcode_user_name) 
DO
 UPDATE
   SET leetcode_user_name = EXCLUDED.leetcode_user_name,
   		first_name = EXCLUDED.first_name,
   		last_name = EXCLUDED.last_name,
   		email = EXCLUDED.email,
   		session_location = EXCLUDED.session_location,
   		session_code = EXCLUDED.session_code;
		
		
-- Upsert sample Data in the active_fellows table;
INSERT INTO active_fellows (leetcode_user_name, first_name, last_name, email, program, session_location, session_code, job_searching)
VALUES
 (
 'hideaki',
 'Heng',
 'Lee',
 'zl1761@nyu.edu',
 'DE',
 'NYC',
 '18c',
 True
 ) 
ON CONFLICT (leetcode_user_name) 
DO
 UPDATE
   SET leetcode_user_name = EXCLUDED.leetcode_user_name,
   		first_name = EXCLUDED.first_name,
   		last_name = EXCLUDED.last_name,
   		email = EXCLUDED.email,
   		session_location = EXCLUDED.session_location,
   		session_code = EXCLUDED.session_code;




-- Upsert sample Data in the active_fellows table;
INSERT INTO active_fellows (leetcode_user_name, first_name, last_name, email, program, session_location, session_code, job_searching)
VALUES
 (
 'oreki47',
 'Heng',
 'Lee',
 'zl1761@nyu.edu',
 'DE',
 'NYC',
 '18c',
  True
 ) 
ON CONFLICT (leetcode_user_name) 
DO
 UPDATE
   SET leetcode_user_name = EXCLUDED.leetcode_user_name,
   		first_name = EXCLUDED.first_name,
   		last_name = EXCLUDED.last_name,
   		email = EXCLUDED.email,
   		session_location = EXCLUDED.session_location,
   		session_code = EXCLUDED.session_code;



-- Sample select data to ensure if the previous update was success.
SELECT leetcode_user_name
FROM active_fellows
WHERE job_searching = True;





-- Remove data from leetcode_records if necessary
DELETE FROM leetcode_records;

-- Upsert sample Data in the active_fellows table;
INSERT INTO leetcode_records (record_id, user_name, num_solved, num_accepts, num_submissions, accepted_percentage, finished_contests, record_date )
VALUES
 (
 'oreki47_2019-01-14',
 'oreki47',
 '245',
 '408',
 '500',
 '59.1',
 '3',
 '2019-01-14'
 ) 
ON CONFLICT (record_id) 
DO
 UPDATE
   SET num_solved = EXCLUDED.num_solved,
   		num_accepts = EXCLUDED.num_accepts,
   		num_submissions = EXCLUDED.num_submissions,
   		accepted_percentage = EXCLUDED.accepted_percentage,
   		finished_contests = EXCLUDED.finished_contests;

-- Query 

SELECT * 
FROM leetcode_records;