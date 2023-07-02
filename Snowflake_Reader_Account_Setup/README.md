Allows setup of Snowflake Reader account for external user use
===============================================================

Script uses config.ini file to pick Snowflake connection details, databases and commands to run.

Usage
-----

```
--locale LOCALE             Locale for connecting to region-specific snowflake. Based on the locale, Snowflake  
                            connection details are picked from the config.ini file. The default is set to 'eu'. 

--reader_admin_credentials  The admin password to be set for Snowflake Reader Account. The default is set to 
                            'Admin@123!'.

--reader_user_credentials   The external user password to be set for Snowflake Reader Account. The default is set to 
                            'User@123!'.

--print-only                To generate SQL command without actually running them. Default is True.

--cleanup                   To delete all the objects setup for Snowflake Reader Account for a particular context.
                            Context ID is picked from the config file. Default is False.

```

Usage Example
-------------

To generate the sql command. Note, by default it connects to 'eu' environment

python ./run.py
python ./run.py --print-only

To generate the sql command for a specific environment:

python ./run.py --locale='us'
python ./run.py --locale='us' --print-only

To generate the sql command for clean-up task:

python ./run.py --clean-up

To run the script and create the snowflake reader-account. Note, by default it connects to 'eu' environment and uses the context details from config.ini

python ./run.py --no-print