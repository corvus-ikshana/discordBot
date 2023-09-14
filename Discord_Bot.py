import discord
import requests
import random
import time
import base64
import faker
from github import Github

# Discord Bot Token
DISCORD_BOT_TOKEN = 'YOUR_DISCORD_BOT_TOKEN'

# GitHub Token and Repository Information
GITHUB_TOKEN = 'YOUR_GITHUB_TOKEN'
GITHUB_USERNAME = 'YOUR_GITHUB_USERNAME'
REPO_NAME = 'YOUR_REPO'

# Initialize Discord client with intents
intents = discord.Intents.default()
intents.message_content = True
intents.typing = False 

client = discord.Client(intents=intents)

# Initialize GitHub client
github = Github(GITHUB_TOKEN)
repo = github.get_user(GITHUB_USERNAME).get_repo(REPO_NAME)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    try:
        # It will Get the current README content and SHA
        readme = repo.get_contents('README.md')
        current_content = base64.b64decode(readme.content).decode('utf-8')
        current_sha = readme.sha

        # This will Generate random text within the range of 20 to 200 lines
        random_text_lines = [faker.Faker().sentence() for _ in range(random.randint(20, 200))]
        random_text = '\n'.join(random_text_lines)

        # This will Update the README with random text
        repo.update_file(
            path='README.md',
            message=f'Update README with random text ({time.strftime("%Y-%m-%d %H:%M:%S")})',
            content=random_text,
            sha=current_sha,
            branch='main'  # Replace with your branch name
        )

        print(f'Updated README with random text: {time.strftime("%Y-%m-%d %H:%M:%S")}')

    except Exception as e:
        print('Error:', str(e))

# Run the bot
client.run(DISCORD_BOT_TOKEN)
