# John Cronin Code Samples

These files are code I wrote for my previous position as a Data Engineer at the ACS, creating Tableau dashboards displaying usage and engagement data for the ACS's frequent national conferences.

This repo contains code samples in both Python and SQL. Together these sets of code represent just a few of the dozen or more scripts or so that I would write (across both SQL and Python) for a single conference. 

**PYTHON**  
The Python code is stored in the appropriately named folder. Much of the remote portions of all of the ACS's conferences were hosted in Zoom, and the Python scripts here were designed to extract data on attendance for those meetings (who attended what meetings when) from Zoom's API, then clean, relabel, and tweak that data before exporting it to a table in the ACS's collection of SQL Servers. I would then use Tableau to draw from that table to help create dashboards allowing conference stakeholders to monitor how attendees were interacting with the different sessions available to them at a given ACS conference. I chose these files not only because they deal with data from a well-known company (Zoom) but they represent a siloed and easy-to-follow portion of one of the data pipelines that I would design and manage at the ACS.

`run_zoom_session_attendance.py` is a wrapper for `zoom_session_attendance_runner.py` and is designed to be the actual piece
of code that is run either in the command line or via any sort of automation. It not only runs `zoom_session_attendance_runner.py` but also allows the user to modify the parameters that the wrapped file uses when it is run.

`zoom_session_attendance_runner` contains almost all of the actual "work" of querying the Zoom API, modifying the data, and writing it to the SQL Server. 

`_types.py` and `jwt_tokenizer` are small functional files containing either classes or functions the other files need.

*The dashboard pictured below, created by me, was supported by Python code identical to what I have provided here.*\*
![Conference_Engagement_Summary](https://github.com/croninjohn/code_examples/blob/master/Dashboards/Conference_Engagement_Summary.png?raw=true)

**SQL**   
The SQL code can also be found in the accordingly named folder. It contains a single SQL (`Report.Meetings_Dashboard_Event_Registration_w_Payments.View`) file that creates a SQL view used by a Tableau dashboard designed to show executive leadership the state of visitor registrations for upcoming ACS conferences. It draws on various source tables to create a unified view containing an entry for each conference registrant. It was not the only piece of SQL code used to support the aforementioned dashboard, but it demonstrates better than others the proficiency with SQL I want to communicate.

*This dashboard, also created by me, is the one that draws on the SQL code I've provided*
![Conference_Registrations_Summary](https://github.com/croninjohn/code_examples/blob/master/Dashboards/Conference_Registrations_Summary.png?raw=true)



Documentation for the Zoom API Endpoint used here:
https://marketplace.zoom.us/docs/api-reference/zoom-api/dashboards/dashboardmeetingparticipants

A bit of Zoom's own Documentation on their use of JWTs:
https://marketplace.zoom.us/docs/guides/auth/jwt


\* *Digitell* as it appears in this dashboard refers to the virtual platform host for the conferences; for reasons not worth exploring, some conference meetings were hosted in Zoom, while others used Digitell's built-in meeting system.
