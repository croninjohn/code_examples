'''
This file contains almost all of the actual "work" of querying the Zoom API, modifying the data, and writing it to the SQL Server
It is run using the "run_zoom_session_attendance.py" file.

Each entry in the data that this script imports represents a single attendee to one Zoom meeting,
contain, among other fields, the an ID for the user logging in, the an ID for the meeting being logged into,
and when the user both logged in and when they logged off.

Visit the readme for a link to the relevant documentation for the Zoom API
'''

# Standard packages
import typing
import datetime
import time

# External Packages
import requests
import sqlalchemy  
import pandas as pd  
import requests
import pytz

# Local Packages
import secure_package
from fall_meeting_2021.librum import jwt_tokenizer,_types

#converts each participant in the API return into a dict that can be feed into a pandas dataframe (as part of a list of dicts)
def participant_converter(parameters, meeting_id, series, participant):

	participant_dict = {}

	participant_dict['zoom_meeting_id'] = meeting_id
	participant_dict['session_id'] = series['Meeting_Id']

	'''
	This code is a little convoluted, but was the only way I could manage to integrate dynamic timezone adjustments
	given the restrictions of different python/pandas/numpy datetime data types AND the pecularities of SQLAlchemy (the team's preferred SQL-Python module)
	
	Essentially, the pandas datatime data type called Timestamp IS timezone aware, but CANNOT be read into SQL with SQL Alchemy
	The numpy datetime data type called Datetime64 IS NOT timezone aware, but CAN be read into SQL with SQL Alchemy

	Datetimes are given as strings in the API call returns; each of these lines converts such a string into a Pandas Timestamp,
	assigns it the source timezone zone given in the parameters, converts it from that timezone to the target timezone in parameters,
	then converts the object to a Numpy datetime64 object, which is timezone naive but preserves the adjustment that has already been made
	'''

	participant_dict['entrance_time'] = pd.Timestamp(participant['join_time'], tz = pytz.timezone(parameters.source_tz)).tz_convert(pytz.timezone(parameters.target_tz)).tz_localize(tz = None).to_datetime64() 
	participant_dict['exit_time'] = pd.Timestamp(participant['leave_time'], tz = pytz.timezone(parameters.source_tz)).tz_convert(pytz.timezone(parameters.target_tz)).tz_localize(tz = None).to_datetime64()
	participant_dict['session_start_time'] = pd.Timestamp(series['Date'].year,series['Date'].month,series['Date'].day,series['Start_Time'].hour,series['Start_Time'].minute,series['Start_Time'].second).to_datetime64()
	participant_dict['session_end_time'] =  pd.Timestamp(series['Date'].year,series['Date'].month,series['Date'].day,series['End_Time'].hour,series['End_Time'].minute,series['End_Time'].second).to_datetime64()

	#no hour or minute data means no reason to swap timezones, which means this can be converted right to datetime64
	participant_dict['session_date'] = series['Date'].to_datetime64()
	participant_dict['entrance_date'] =  pd.Timestamp(participant['join_time']).date().to_datetime64()

	participant_dict['unique_id'] = str(participant['user_id']) + str(meeting_id)
	participant_dict['user_id'] = participant['user_id']

	participant_dict['session_title'] = series['Title']
	participant_dict['session_duration'] = series['Duration']
	participant_dict['session_type'] = series['Session_Type']
	participant_dict['session_location'] = series['Location']


	return participant_dict

#main function that is run by run_zoom_session_attendance.py
def run(
	parameters: _types.ParametersType
	):

	start = datetime.datetime.now().strftime("%H:%M:%S")

	#create sql engine for the read server
	read_sql_engine: sqlalchemy.engine.base.Engine = secure_package.create_engine(
	    category = parameters.read_category,
	    environment = parameters.read_environment, 
	    server = parameters.read_server,
	    user = parameters.read_user,
	    database = parameters.read_database,
	    port = parameters.read_port,
	    sql_kind = parameters.read_sql_kind,
	)

	#create sql engine for the write server
	write_sql_engine: sqlalchemy.engine.base.Engine = secure_package.create_engine(
	    category = parameters.write_category,
	    environment = parameters.write_environment, 
	    server = parameters.write_server,
	    user = parameters.write_user,
	    database = parameters.write_database,
	    port = parameters.write_port,
	    sql_kind = parameters.write_sql_kind,
	)

	#establishes connections
	write_connection = write_sql_engine.connect()
	read_connection = read_sql_engine.connect()

	#reads in Zoom Meeting Details

	'''
	Zoom Meeting Details is a crosswalk table on the relevant SQL server that links each meeting's Zoom Meeting Id 
	(which is used to query for each meeting against the Zoom API) to the organization's internal id number for the session (session_id)
	which is then used by a SQL view not included here to join this data imported from Zoom with pertinent session details
	'''

	#query check
	print("Reading via query: "+ parameters.read_sql_query)

	# queries the read server, places the return into pandas dataframe
	session_details_df = pd.io.sql.read_sql(parameters.read_sql_query, con=read_connection)

	#Access creds
	#These obviously are not stored on git
	#this pulls the api key and api secret from a secure local package
	api_key: str = secure_package.passwords["Zoom"]["production"]["api_key"]
	api_secret: str = secure_package.passwords["Zoom"]["production"]["api_secret"]

	#Creates the credential token used to access the API
	headers = jwt_tokenizer.generate_token(api_key, api_secret)

	#params for the call
	params = {'type': 'past',
	          'page_size': '50',}

	'''
	each query made against the Zoom API generates a return, and if the meeting you're querying about
	had more attendees than an individual return can contain, then the return will contain as many attendees
	as it can fit (50, as per the `page_size` parameter) as well as a new call you can make for the next set of attendees for the original meeting you made your 
	query about. This code is set up to automatically call these embedded queries and extract their data one after another until there aren't any left
	'''

	#variables needed for the looped queries being made below
	next_pagination = ""
	total_participants = 0
	import_list = []

	for index, series in session_details_df.iterrows():
		meeting_id = int(series['Meeting_ID'])

		#each meeting id can't be passed as a param to the query; it's embedded in the endpoint url
		url = str.format(parameters.url, meeting_id = meeting_id)
		
		#this line is where the actual call to the Zoom API is made. "response" stores what is returned
		response = requests.get(url = url, params = params, headers = headers)

		time.sleep(.25) #included to prevent the script from hitting the API's built-in query limit

		#extracts the contents of the response as an easily parsed set of lists and dicts embedded within each other
		data = response.json()
		'''
		 "code" only appears in as a key in the return dict if the query was a failure.
		The check prevents any failed queries (like queries for meetings that haven't happened yet)
		from causing a lethal crash
		'''
		if 'code' not in data.keys():

			total_participants += len(data['participants'])

			for participant in data['participants']:

				import_list.append(participant_converter(parameters, meeting_id, series, participant))
			'''
			each API response contains just 50 entries, but also contains the full query required to get the next 50. this while loop
			iterates through each pagination until there are none left
			'''
			next_pagination = data['next_page_token']

			#the loop only ends when 'next_pagination' is empty, indicating there are no further pages to call
			while len(next_pagination) > 0:

				inner_params = {'type': 'past',
		    					'page_size': '50',}

				inner_params['next_page_token'] = next_pagination			

				inner_response = requests.get(url = url, params = inner_params, headers = headers)
				time.sleep(.25)
				inner_data = inner_response.json()
				total_participants += len(inner_data['participants'])

				for participant in inner_data['participants']:

					import_list.append(participant_converter(parameters, meeting_id, series, participant))

				next_pagination = inner_data['next_page_token']
	
		else:
			print(str.format("Issue encountered for the following meeting: {x}", x = data['message']))

	import_df = pd.DataFrame(import_list)

	print("Import complete; misc. fields dropped.")

	'''
	On rare occasions, when writing large Pandas dataframes to remote servers, SQLAlchemy (the module used here to write to the SQL Server) will spontaneously fail,
	crashing the script. This generally occurs due to slight hiccups in internet connection. The code here splits the very large dataframe created above into
	smaller dataframes segmented by the day on which the zoom meeting occurred. Each of these smaller dataframes is then written individually. This is MUCH more reliable
	'''

	#these lines split the df of all attendees into smaller dfs grouped by day for the sake of keeping the dfs being written a managable size
	grouped = import_df.groupby('entrance_date')
	split_dfs = [group for _, group in grouped]

	if parameters.delete_data and:
		print('Program set to delete data before importing new')
		print(str.format(
			"Deleting data from {server}.{db}.{schema}.{table}",
			server=parameters.write_server,
			db=parameters.write_database,
			schema= parameters.schema_name,
			table= parameters.table_name
		))
		if parameters.dry_run:
			print("However, this is a dry-run, so skipping data write")
		else:

			delete_query = str.format(
				"DELETE FROM {db}.{schema}.{table}",
				db=parameters.write_database,
				schema= parameters.schema_name,
				table= parameters.table_name
			)
			#runs the delete statement
			result = write_connection.execute(delete_query)

	chunk_count = 1
	for sub_df in split_dfs:
		if parameters.dry_run == False and import_df.size > 0:
			print(str.format("Writing Chunk #{x}", x = chunk_count))
			chunk_count += 1
			sub_df.to_sql(
				schema = parameters.schema_name,
				name = parameters.table_name,
				if_exists = 'append',
				con = write_sql_engine,
				chunksize = 500,
				index = False
				)

	print('COMPLETE')
	print("START : " + start)
	print("END : " + datetime.datetime.now().strftime("%H:%M:%S"))	
