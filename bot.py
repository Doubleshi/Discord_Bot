# import two libraries
import openai
import discord

#open and close key.txt file
with open('keys.txt') as f:
	# converting our text file to list of lines
	lines = f.read().split('\n')
	# openai api key
	openai.api_key = lines[0]
	# discord token
	DISCORD_TOKEN = lines[1]
# close the file
f.close()

#chat completion with chat-gpt
response = openai.ChatCompletion.create(
	model="gpt-3.5-turbo",
	messages=[
	{"role": "system", "content": "You are a verbose art graduate student and a little insufferable."},
	{"role": "assistant", "content": "Most art is derivative"},
	{"role": "user", "content": "What makes great art?"}
	]
)

print(response)