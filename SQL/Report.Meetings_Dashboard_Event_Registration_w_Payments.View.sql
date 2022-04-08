/*
This script draws on a number of different tables the organization I worked for uses to store data it receives from partnered vendors to create a single view that captures as much information
about every registrant to the conferences that the organization hosts.

See the README for the Tableau dashboard that the view that this script creates supports.
The different data sources and the overall function of the code is described inline.
*/


USE [ODS]
GO

DROP VIEW IF EXISTS [Report].[Meetings_Dashboard_Event_Registration_w_Payments]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE OR ALTER VIEW [Report].[Meetings_Dashboard_Event_Registration_w_Payments]
AS
	SELECT 
		[Registrant].[ID_Registrant]
		,[Event].[Event_Code]
		,[Event].[Event_Category]
		,[Event].[Event_Season]
		,[Event].[Event_Region]
		,[Event].[Show_Code]
		,[Event].[Show_Name]
		,[Event].[Event_Title]
		,[Event].[Event_Start_Date]
		,[Event].[Event_End_Date]
		,[Registrant].[Badge]
		,[Registrant].[Constituent_ID]
		,[Registrant].[Last_Name]
		,[Registrant].[First_Name]
		,[Registrant].[RegClass_Code]
		,[Registrant].[ExtraInfo40] AS [Abstract_Accepted]
		,[Metadata].to_proper_case([Registrant].RegClass_Long_Name) AS RegClass_Long_Name -- calls simple function to clean up some messy strings
		,[Registrant].[Registration_DateTime]
		,[Registrant].[State_Province]
		,[Registrant].[Country]
		,[firstmtg].[Answer_Text] AS [First_Meeting]
		,[cst].[Industry_Description]
		,[cnv].[Conversion_Flag]
		,[Registration_Vendor_Event_Extended].[Registration_Target]
		,[Registration_Vendor_Event_Extended].[Revenue_Target]
		,[payments].[Total_Revenue] AS [Total_Revenue]
		,[payments].[Total_Revenue] AS [Registrant_Total_Paid]
	FROM
		[Registration_Vendor_Schema].[Registrant] --The primary table that this view draws on; contains one record for each registrant but limited other information
		INNER JOIN [Registration_Vendor_Schema].[Event] --Contains supplementary information about different conferences being held; used to flesh out the info found in Registration_Vendor_Schema.Registrant
			ON [Registrant].[ID_Event] = [Event].[ID_Event]
		LEFT JOIN [Report].[Registration_Vendor_Event_Extended] --This is a small static table containing, when available, registration and revenue targets for different conferences
			ON [Event].[Event_Code] = [Registration_Vendor_Event_Extended].[Event_Code]

		/*
		This code section connects Registration_Vendor.Registrants to Registration_Vendor.Demo, a table containing registrant's responses
		during registration to several supplementary questions. In doing so, the script isolates only the entries for questions
		that asked if this was a registrant's first conference, and matched the question's answer back to the relevant registrants in Registration_Vendor.Registrant, 
		ignoring duplicates in Registration_Vendor.Demo along the way.
		*/
		LEFT JOIN (
			SELECT
				[ID_Registrant]
				,[ID_Event]
				,[Badge]
				,[Event_Code]
				,[Question_Text]
				,[Answer_Text]
				,ROW_NUMBER() OVER(
                    PARTITION BY 
                    	[Event_Code] 
                    	,[Badge] 
                    ORDER BY [Record_Status_Date] DESC
                ) AS ROW_NUM
			FROM
				[Registration_Vendor_Schema].[Demo]
			WHERE 
				[Question_Text] IN (
                    '* Is this your first Meeting?'
                    ,'Is this your first Meeting?'
                )
		) AS [firstmtg]
			ON [Registrant].[ID_Event] = [firstmtg].[ID_Event] 
			AND [Registrant].[ID_Registrant] = [firstmtg].[ID_Registrant]
			AND [firstmtg].[ROW_NUM] = 1

		/*
		This section links, as best as possible, every registrant in Registration_Vendor_Schema.Registrant back to an entry in Membership_Schema.Constituent,
		the organizations's central table for details about individual members. It does this to attempt to match each Registrant back to a description
		of the industry they work in that would be stored in their member profile.
		*/
		LEFT JOIN (
			SELECT
				[Registrant].[Event_Code],
				[Constituent].[Constituent_ID],
				[Constituent].[Industry_Description],
				ROW_NUMBER() OVER(
                    PARTITION BY 
                        [Registrant].[Event_Code], 
                        [Registrant].[Constituent_ID] 
                    ORDER BY [Modified_DateTime] DESC
                ) AS [ROW_NUM]
			FROM
				[Registration_Vendor_Schema].[Registrant]
				INNER JOIN [SDS].[Constituent]
				    ON [Registrant].[Constituent_ID] = [Constituent].[Constituent_ID] 
		) AS [cst]
			ON [Registrant].[Event_Code] = [cst].[Event_Code]
			AND [Registrant].[Constituent_ID] = [cst].[Constituent_ID]
			AND [cst].[ROW_NUM] = 1

		/*
		This section links each registrant in Registration_Vendor.Registrant back to any memberships they purchased while
		registering. Without noting the details of that new membership, it merely records whether or not they purchased a membership
		*/
		LEFT JOIN (
			SELECT DISTINCT
				[Event].[ID_Event],
				[Event].[Event_Code],
				[Event].[Event_Title],
				[Registrant].[ID_Registrant],
				[Registrant].[Badge],
				1 AS [Conversion_Flag]
			FROM 
				[Registration_Vendor_Schema].[Event_Item]
				INNER JOIN [Registration_Vendor_Schema].[Registrant]
					ON [Event_Item].[ID_Registrant] = [Registrant].[ID_Registrant]
				INNER JOIN [Registration_Vendor_Schema].[Event]
					ON [Event_Item].[ID_Event] = [Event].[ID_Event]
			WHERE 
				[Item_Code] IN ('DAFE', 'DRME', 'DRMSTE', 'DSMUGE') --These item codes indicate an item was a new organization membership
		) AS cnv
			ON [Registrant].[ID_Event] = [cnv].[ID_Event] 
			AND [Registrant].[ID_Registrant] = [cnv].[ID_Registrant]

		/*
		This section links each registrant in Registration_Vendor_Schema.Registrant back to any purchases that were associated with their registration,
		sums the total value of those purchases, and thereby calculates for each registrant the total revenue that they generated
		*/
		LEFT JOIN (
			SELECT
                [Meetings_Dashboard_Event_Payment].[ID_Registrant], 
                SUM([Meetings_Dashboard_Event_Payment].[Amount_Paid]) AS [Total_Revenue]
			FROM [Report].[Meetings_Dashboard_Event_Payment]
			GROUP BY [Meetings_Dashboard_Event_Payment].[ID_Registrant]
		) AS [payments]
			ON [Registrant].[ID_Registrant] = [payments].[ID_Registrant]

GO


