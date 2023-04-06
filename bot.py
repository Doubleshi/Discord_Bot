# import libraries
import requests
import time
import os
from PIL import Image
import discord

#open and close key.txt file
with open('keys.txt') as f:
	# converting our text file to list of lines
	lines = f.read().split('\n')
	# openai api key
	api_key = lines[0]
	# discord token
	DISCORD_TOKEN = lines[1]
	# open api_base
	api_base = lines[2]
# close the file
f.close()

api_type = "azure"
api_version = "2022-08-03-preview"

# specifying our server
GUILD = '{Shi&Shi}'

# create an object that will control our discord bot
client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
	for guild in client.guilds:
		if guild.name == GUILD:
			break
	# print out nice statement saying our bot is online
	print(f'{client.user} has connected to Discord!')
@client.event
async def on_message(message):
	# this prevents inifinte loops of bot talking to bot
	# if author of the message is the bot, don't do anything
	if message.author == client.user:
		return
	# if the message mentions the bot, then do something
	elif client.user.mentioned_in(message): 
		url = "{}dalle/text-to-image?api-version={}".format(api_base, api_version)
		headers= { "api-key": api_key, "Content-Type": "application/json" }
		body = {
			"caption": message.content,
			"resolution": "1024x1024"
		}
		submission = requests.post(url, headers=headers, json=body)
		operation_location = submission.headers['Operation-Location']
		retry_after = submission.headers['Retry-after']
		status = ""
		while (status != "Succeeded"):
			time.sleep(int(retry_after))
			response = requests.get(operation_location, headers=headers)
			print(response)
			status = response.json()['status']
		image_url = response.json()['result']['contentUrl']
		await message.channel.send(image_url)
		

#chat completion with chat-gpt
# response = openai.ChatCompletion.create(
# 	engine="GPT-4",
# 	messages=[
# 	{"role": "system", "content": "You are a small child, most things amuse you. Make sure all responses are less than 2000 characters"},
# 	{"role": "user", "content": "What's the best thing to do when your code is broken?"}
# 	]
# )
# print(response.choices[0].message.content)

client.run(DISCORD_TOKEN) 