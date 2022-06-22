# John Cronin Data Engineering Overview

**NOTE:**
*While you're welcome to peruse this repo and I'm proud of the work inside, please consider checking out [this repo](https://github.com/croninjohn/games_savings_etl) first; the ETL project it contains is better documented, uses  modern cloud DE tools, and supports an active, public [dashboard](http://18.212.173.53:3000/public/dashboard/cda4da01-2386-433a-b4ce-c3ae2ec5ee75). If I sent you the link to this repo specifically, that was an accident on my part – check out my whole profile!* 





These files are code that closely approximates some scripts I wrote for a previous position of mine as a Data Engineer, creating data pipelines supporting analytics dashboards for the frequent virtual academic conferences of a large professional society for scientists.

This repo contains code samples in both Python and SQL. Together these sets of code represent just a few of the dozen or more scripts or so that I would write (across both SQL and Python) for a single conference. 

I can provide images of the dashboards these code pieces supported upon request.

**PYTHON**  
The Python code is stored in the appropriately named folder. Much of the remote portions of all of the conferences were hosted in Zoom, and the Python scripts here were designed to extract data on attendance for those meetings (who attended what meetings when) from Zoom's API, then clean, relabel, and tweak that data before exporting it to a table in the organization's SQL database. I would then use Tableau to draw from that table to help create dashboards allowing conference stakeholders to monitor how attendees were interacting with the different sessions available to them at a given conference. I chose these files not only because they deal with data from a well-known company (Zoom) but they represent a siloed and easy-to-follow portion of one of the data pipelines that I would design and manage.

[`run_zoom_session_attendance.py`](https://github.com/croninjohn/data_pipeline_code_samples/blob/master/Python/run_zoom_session_attendance.py) is a wrapper for `zoom_session_attendance_runner.py` and is designed to be the actual piece
of code that is run either in the command line or via any sort of automation. It not only runs `zoom_session_attendance_runner.py` but also allows the user to modify the parameters that the wrapped file uses when it is run.

[`zoom_session_attendance_runner.py`](https://github.com/croninjohn/data_pipeline_code_samples/blob/master/Python/fall_meeting_2021/zoom_session_attendance_runner.py) contains almost all of the actual "work" of querying the Zoom API, modifying the data, and writing it to the SQL Server. Each entry in the data that this script imports represents a single attendee to one Zoom meeting and contains, among other fields, an ID for the user logging in, the an ID for the meeting being logged into, and when the user both logged in and when they logged off.


[`_types.py`](https://github.com/croninjohn/data_pipeline_code_samples/blob/master/Python/fall_meeting_2021/librum/_types.py) and [`jwt_tokenizer.py`](https://github.com/croninjohn/data_pipeline_code_samples/blob/master/Python/fall_meeting_2021/librum/jwt_tokenizer.py) are small functional files containing either classes or functions the other files need.

**SQL**   
The SQL code can also be found in the accordingly named folder. It contains a single file ([`Report.Meetings_Dashboard_Event_Registration_w_Payments.View`](https://github.com/croninjohn/data_pipeline_code_samples/blob/master/SQL/Report.Meetings_Dashboard_Event_Registration_w_Payments.View.sql))  that creates a SQL view used by a Tableau dashboard designed to show executive leadership the state of visitor registrations for upcoming conferences. It draws on various source tables to create a unified view containing an entry for each conference registrant. It was not the only piece of SQL code used to support the aforementioned dashboard, but it demonstrates succinctly the proficiency with SQL I want to communicate.

