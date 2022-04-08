# John Cronin Data Engineering Overview

These files are code that closely approximates some scripts I wrote for a previous position of mine as a Data Engineer, creating Tableau dashboards displaying usage and engagement data for the frequent national conferences of a large professional society for scientists.

This repo contains code samples in both Python and SQL. Together these sets of code represent just a few of the dozen or more scripts or so that I would write (across both SQL and Python) for a single conference. 

I can provide images of the dashboards these code pieces supported upon request.

**PYTHON**  
The Python code is stored in the appropriately named folder. Much of the remote portions of all of the conferences were hosted in Zoom, and the Python scripts here were designed to extract data on attendance for those meetings (who attended what meetings when) from Zoom's API, then clean, relabel, and tweak that data before exporting it to a table in the organization's SQL database. I would then use Tableau to draw from that table to help create dashboards allowing conference stakeholders to monitor how attendees were interacting with the different sessions available to them at a given conference. I chose these files not only because they deal with data from a well-known company (Zoom) but they represent a siloed and easy-to-follow portion of one of the data pipelines that I would design and manage.

`run_zoom_session_attendance.py` is a wrapper for `zoom_session_attendance_runner.py` and is designed to be the actual piece
of code that is run either in the command line or via any sort of automation. It not only runs `zoom_session_attendance_runner.py` but also allows the user to modify the parameters that the wrapped file uses when it is run.

`zoom_session_attendance_runner.py` contains almost all of the actual "work" of querying the Zoom API, modifying the data, and writing it to the SQL Server. Each entry in the data that this script imports represents a single attendee to one Zoom meeting and contains, among other fields, an ID for the user logging in, the an ID for the meeting being logged into, and when the user both logged in and when they logged off.

`_types.py` and `jwt_tokenizer` are small functional files containing either classes or functions the other files need.

**SQL**   
The SQL code can also be found in the accordingly named folder. It contains a single SQL (`Report.Meetings_Dashboard_Event_Registration_w_Payments.View`) file that creates a SQL view used by a Tableau dashboard designed to show executive leadership the state of visitor registrations for upcoming conferences. It draws on various source tables to create a unified view containing an entry for each conference registrant. It was not the only piece of SQL code used to support the aforementioned dashboard, but it demonstrates succinctly the proficiency with SQL I want to communicate.

