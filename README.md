# responses-bot
Discord bot for custom responses

## Requirements
- discord.py (pip install discord)
- python 3 environment
- a discord bot token
- an internet connection

## Commands
### addresponse 
- Command for adding new response.
- Usage: addresponse <trigger> <response>
- Quotation marks are required if the given message contains more than one word or backslashes
- Server Admin only
- Aliases: acr, addcustreact

### deleteresponse
- Command for deleting an existing response.
- Usage: deleteresponse <trigger> <index>
- Quotation marks are required if the given message contains more than one word or backslashes
- index starts from 0 with the first message in the list of reactions to this trigger. Use -1 or leave blank to delete all reactions to this trigger
- Server Admin only
- Aliases: dcr, delcustreact

### editresponse
- Command for editing an existing response
- Usage: editresponse <trigger> <index> <new response>
- Quotation marks are required if the given message contains more than one word
- index starts from 0 with the first message in the list of reactions to this trigger.
- Server Admin only
- Aliases: ecr, editcustreact

### listtriggers
- Command for listing all triggers
- Usage: listtriggers
		    Aliases: lcr, lts
		
### listresponses
- Command for listing all responses for a given trigger
- Usage: listresponses <trigger>
- Quotation marks are required if the given message contains spaces
- Aliases: lrs

### reload
- Command for reloading all messages from responses.json file
- Usage: reload
- Bot Owner (as specified in settings.json) only

## Setup
1. Provide your bot token and owner ID in the settings.json file
2. Build your own settings.json file and save in the same dir
	- token: str - Your Discord Bot Token
	- owner: int - The User ID of the Owner
	- prefix: str - Prefix for the Commands above
	- ignore_bot: boolean - If Bot messages should be ignored or not
3. run the main.py file using python

## Functionality
randomly select a message from the respective list and replies with the message when the trigger word is sent in a channel the bot is in
