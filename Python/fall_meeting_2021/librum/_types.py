"""
new types for important data-structures in the code.

The 'type-annotations' will never be needed to make  
the code function, but they will improve the life of anyone 
supporting the code later.
"""

import typing
import pytz

'''
this class serves as the bridge connecting 'run_zoom_session_attendance.py' and the 'zoom_session_attendance_runner.py',
the former serving as a wrapper for the latter. An instance of this class is defined in 'run_zoom_session_attendance.py', where it then passed
to 'zoom_session_attendance_runner.py' where it is used to control how that script makes its API calls, modifies the data it pulls, and writes it elsewhere

'''
class ParametersType:

    # dry_run: if True, do not write values, simply report results
    #   This is useful for testing the connections, without changing data
    dry_run: bool = True

    # delete_data: if True, will delete all data in a an output/'write' table
    #   before inserting into it
    delete_data: bool = False

    #    Read Target
    read_category: str
    read_environment: str
    read_server: str
    read_port: str
    read_user: str
    read_database: str
    read_sql_connector: str
    read_sql_kind: str
    read_password: typing.Optional[str]

    #       Write Target
    write_category: str
    write_environment: str
    write_server: str
    write_port: typing.Optional[str]
    write_user: str
    write_database: str
    write_sql_connector: str
    write_sql_kind: str
    write_password: typing.Optional[str]

    #Analytics dashboard specific variables

    #SQL and schema to which data will be written
    schema_name: str
    table_name: str

    #API Query URL
    url: str

    #the timezone that the API returns any datetime data in (generally UTC)
    source_tz : str
    #the timezone you want the datatime data to be written to the SQL table in
    target_tz : str

    #if the script requires reading data from an already existing SQL table in the SDS,
    #include the SQL query to pull that data here
    read_sql_query : str



