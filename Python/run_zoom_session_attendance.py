'''
This file serves as a wrapper for 'zoom_session_attendance_runner.py' and is designed to be the actual piece
of code that is run either in the command line or via any sort of automation
It not only runs 'zoom_session_attendance_runner.py' but also allows the user to modify the parameters that
the wrapped file uses when it is run
'''

from fall_meeting_2021.librum import _types
from fall_meeting_2021 import zoom_session_attendance_runner as runner

import typing
import pytz

class ParametersType:


    #if this variable is true, no actual deleting or writing will be done
    #the script will query the API and prepare DataFrames for export, but not actually write them anywhere
    dry_run: bool = True

    #if this variable is True, code will be run that will delete all the data in the target SQL table before any new data is written to it
    #In order to maintain idempotency, this should always be True for any actual runs
    delete_data: bool = False
    


    #Read Sql Engine Params (required by SQLAlchemy to generate a connection to the SQL Server)
    read_category: str = 'category'
    read_environment: str = 'environment'
    read_server: str = 'server'
    read_port: typing.Optional[str] = None
    read_user: str = 'user'
    read_database: str = 'database'
    read_sql_kind: str = 'sql_kind

    read_sql_query: str = str.format(
        ('SELECT * FROM {schema_name}.{table_name}'),
        schema_name= 'FM_2021_Zoom',
        table_name= 'Zoom_Session_Details'
        )

    #Write Sql Engine Params (required by SQLAlchemy to generate a connection to the SQL Server)
    write_category: str = 'category'
    write_environment: str = 'development'
    write_server: str = 'server'
    write_port: typing.Optional[str] = None
    write_user: str = 'user'
    write_database: str = 'database'
    write_sql_kind: str = 'sql_kind'

    #Schema and Table for SQL Table to be written to
    schema_name: str = 'FM_2021_Zoom'
    table_name: str = 'Attendance'

    #API Query URL
    url: str = 'https://api.zoom.us/v2/metrics/meetings/{meeting_id}/participants'

    #the timezone that the API returns any datetime data in (generally UTC)
    source_tz: str = 'Etc/UTC'

    #the timezone you want the datatime data to be written to the SQL table in
    target_tz: str = 'US/Eastern'




parameters: _types.ParametersType = ParametersType()


runner.run(
    parameters
)
