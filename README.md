# data_pipeline_example

These files are code I wrote for my previous position as a Data Engineer at the ACS, creating Tableau dashboards displays the usage and engagement data for the ACS's frequent national conferences.

This repo contains examples of both my Python and my SQL code. Normally they would be be stored together this way, but for the sake of convenience they are. Together these sets of code represent just a few of the dozen or more scripts or so that I would write (across both SQL and Python) for a single conference. 

**PYTHON**  
The Python code is stored in the appropriately named folder. Much of the remote portions of all of the ACS's conferences were hosted in Zoom, and the Python scripts here were designed to extract data on attendance for those meetings (who attended what meetings when) from Zoom's API, then clean, relabel, and tweak that data before exporting it to a table in the ACS's collection of SQL Servers. I would then use Tableau to draw from that table to help create dashboards allowing conference stakeholders to monitor how attendees were interacting with the different sessions available to them at a given ACS conference. I chose these files not only because they deal with data from a well-known company (Zoom) but they represent a linear and relatively easy to follow portion of one of the data pipelines that I would design and manage at the ACS.

*The dashboard pictured below, created by me, was supported by Python code identical to what I have provided here.*

**SQL** 
The SQL code can also be found in the accordingly named folder. It contains a single SQL file that creates a SQL view used by a Tableau dashboard designed to show executive leadership the state of visitor registrations for upcoming ACS conferences. It draws on various source tables from different source systems to create a unified view containing an entry for each conference registrant. It was not the only piece of SQL code used to support the aforementioned dashboards, but it demonstrates better than others the proficiency with SQL I want to communicate.

*This dashboard, also created by me, is the one that draws on the SQL code I've provided*




Documentation for the Zoom API Endpoint used here:
https://marketplace.zoom.us/docs/api-reference/zoom-api/dashboards/dashboardmeetingparticipants

A bit of Zoom's own Documentation on their use of JWTs:
https://marketplace.zoom.us/docs/guides/auth/jwt