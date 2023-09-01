Allows setup of Snowflake Reader account for external client use
===============================================================

Script uses config.ini file to pick Snowflake connection details, databases and commands to run. Script is designed to create VIEWS and other dependent objects for both the Primary and Flash Schema to share with the external clients securely.

Usage
-----

```
--locale LOCALE             Locale for connecting to region-specific snowflake. Based on the locale, Snowflake  
                            connection details are picked from the config.ini file. The default is set to 'eu'. 

--reader_admin              The admin username to be created to access the Snowflake Reader Account with full privileges. The default is set to 
                            'ReaderAdmin'.

--reader_user               The additional user to be created to access the Snowflake Reader Account with limited privileges. The default is set to 
                            'ReaderUser'.                                                        

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

To generate the sql command for clean-up all the objects created for a specific client:

python ./run.py --cleanup

To run the script and create the snowflake reader-account. Note, by default it connects to 'eu' environment and uses the database details from the config.ini

python ./run.py --no-print

To run the script and create the snowflake reader-account with specific user-name. Note, by default it connects to 'eu' environment and uses the database details from the config.ini

python .\run.py --no-print --reader_user='EXT_USER_CLIENT_ID_100'


Understanding config file
-------------------------

1. Config file has explanation for most of the keys. Please take a look at the file.

2. Key [ext_client_name] cannot be blank. It needs the proper external client name with whom the objects will be shared. If the external client name already exist in the mapping table, then script will replace all the objects.

3. Provide a value for the key [context_id] to create shareable objects for the Primary database.

4. Provide a value for the key [event_owner_id] to create shareable objects for the Flash database.
