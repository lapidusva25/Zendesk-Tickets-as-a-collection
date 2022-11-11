# Zendesk-Tickets-as-a-collection

Quick start: 
Edit zendesk_tickets.py and ensure lines 7-14 are correctly populated.

Requirements:

You are using orgs within Zendesk.
You have a field on the org in Zendesk which matches to a field within your Totango attributes.
You have admin rights to Zendesk
You have admin rights to Totango
You have an AWS bucket with an AWS_key / AWS_secret
You have the ability to read and write to this bucket

High level overview:

This code is meant to run on a scheduled timeline.

It checks to see if there was file output previously and if so, it grabs the max value of the last modified date, and uses that in the query.  If it does not find a file it fetches all tickets.

To minimize API calls, because Zendeks doesn't directly reveal the requesters email address/org ID but rather an ID that points to a reference within another table.  The code saves the lookup list of requesters/orgs it has previously interacted with, and creates two support files (org/requesters).

