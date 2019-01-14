-- Remove data from active_fellows if necessary
DELETE FROM active_fellows;

-- Upsert sample Data in the active_fellows table;
INSERT INTO active_fellows (leetcode_user_name, first_name, last_name, email, session_location, session_code)
VALUES
 (
 'zl1761',
 'Heng',
 'Lee',
 'zl1761@nyu.edu',
 'NYC',
 '18c'
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
SELECT * 
FROM active_fellows
WHERE leetcode_user_name = 'zl1761';