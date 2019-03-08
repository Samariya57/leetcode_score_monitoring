# Leetcode Score Monitoring Project Set up


## Step 0 - Project Environment Set up 
### Set up Python environment and source it

    mkdir ~/python-virtual-environments
    
    cd ~/python-virtual-environments
    
    python3 -m venv env
    
    source ~/python-virtual-environments/env/bin/activate


### Permanently add project environment variables to .profile
    
    # For Leetcode project
    export LEETCODE_PROJECT_ENV=~/python-virtual-environments/env/bin/activate
    export LEETCODE_PROJECT_SCRAPER_PATH=~/leetcode_score_monitoring/src/Scraper/leetCode_spider

After added the above lines in to ~/.profile then source the profile by 

    source ~/.profile
  
Source the LEETCODE_PROJECT_ENV

    source $LEETCODE_PROJECT_ENV

## Step 1 - Install Project Dependencies  

##### May need to update to python3-pip
    sudo apt install python3-pip

## Install requirements 
    pip3 install wheel
    pip3 install -r requirements.txt

## Step 2 - Install and Configure Database  

### Set up db_configs.ini in your project path

change directory to the ../leetcode_score_monitoringsrc/DB

    cd ../leetcode_score_monitoring/src/DB
    vi db_configs.ini

Modified the <...> fileds and copy and paste the content into db_configs.ini

    [DB_Configs]
    DB_TYPE = postgresql
    DB_DRIVER = psycopg2
    DB_USER = <DB_USER NAME>
    DB_PASS = <DB_USER_PASSWARD>
    DB_HOST = localhost
    DB_PORT = 5432
    DB_NAME = <DB_NAME>
    POOL_SIZE = 50
    TABLENAME =<DB_TABLE_NAME>


### Set up PostgreSQL
#### Install PostgreSQL if you haven't

The following pages have detailed instructions for installing PostgreSQL in MacOS and Ubuntu 18.04 

[Getting Started with PostgreSQL on Mac OSX](https://www.codementor.io/engineerapart/getting-started-with-postgresql-on-mac-osx-are8jcopb)

[How To Install and Use PostgreSQL on Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04)


You may need to install the following 

    sudo apt install postgresql-client-common



### Create new database user role

    sudo -u postgres createuser --interactive -P

    Enter name of role to add: <user_name>
    Enter password for new role: 
    Enter it again: 
    Shall the new role be a superuser? (y/n) n
    Shall the new role be allowed to create databases? (y/n) y
    Shall the new role be allowed to create more new roles? (y/n) y
    

### Sign in to psql as super-user postgres
   
    sudo -u postgres psql



### Create airflow and leetcode_score_monitoring databases

    CREATE DATABASE airflow;
    CREATE DATABASE leetcode_score_monitoring;

### Grant all privileges on the previous created databases to newly created user

    GRANT ALL PRIVILEGES ON DATABASE airflow TO <user_name>;
    GRANT ALL PRIVILEGES ON DATABASE leetcode_score_monitoring TO <user_name>;


### Create tables in database leetcode_score_monitoring and insert sample data 

    psql -U <user_name> -h 127.0.0.1 -d leetcode_score_monitoring

#### Create tables with the sql statements in repo
All sql statements can be found in create_tables.sql 

You can run the following command to execute all the sql statements to create the tables you needed.

    psql -U <user_name> -h 127.0.0.1 -d leetcode_score_monitoring -a -f ~/leetcode_score_monitoring/src/DB/SQL_Statements/create_tables.sql

#### Insert sample data into database for testing with the sql statements in repo
All sql statements can be found in insert_statements.sql

You can run the following command to execute all the sql statements to insert the sample data you needed.

    psql -U <user_name> -h 127.0.0.1 -d leetcode_score_monitoring -a -f ~/leetcode_score_monitoring/src/DB/SQL_Statements/insert_statements.sql


## Step 3 -  Test Run Scrapy Spider Project and Dash Webapp 

### Test scraping with run.sh

    sh ~/leetcode_score_monitoring/src/Scraper/leetCode_spider/run.sh


### Test Run Dash Board
    
    python ~/leetcode_score_monitoring/src/webapp/dash_board.py


## Step 4 - Set up Airflow

Go to the airflow folder

    cd ../leetcode_score_monitoring/src/airflow

#### You can run this line every-time when you need to run Airflow
#### Or set this as an environment variable and replace `pwd` with ~/leetcode_score_monitoring/src/airflow 

    export AIRFLOW_HOME=`pwd`/airflow_home


### Init airflow 

   airflow version


### Update Airflow Configurations

Details can be found from this page 

https://gist.github.com/rosiehoyem/9e111067fe4373eb701daf9e7abcc423

go to airflow.cfg and update this configuration to LocalExecutor:


    # The executor class that airflow should use. Choices include
    # SequentialExecutor, LocalExecutor, CeleryExecutor
    executor = LocalExecutor

Also update the SequelAlchemy string to point to a database you are about to create.

    # The SqlAlchemy connection string to the metadata database.
    # SqlAlchemy supports many different database engine, more information
    # their website
    sql_alchemy_conn = postgresql+psycopg2://<username>:<password>@localhost:5432/airflow



### Init Databae for Airflow

    airflow initdb



### Set up airflow Admin

Details can be found in this page: 

https://airflow.apache.org/security.html


### Start airflow with the following commands. Both should be running.

    airflow scheduler
    airflow webserver



