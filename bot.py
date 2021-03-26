import discord
import json
import re
import shlex

client = discord.Client()
CONFIG_FILE = open('config.json','r')
CONFIG_JSON = json.loads(CONFIG_FILE.read())

PREFIX = CONFIG_JSON['prefix']
TOKEN = CONFIG_JSON['token']

CONFIG_FILE.close()

DATA_FILE = open('data.json','r')
CATALOG = json.loads(DATA_FILE.read())

print('STARTING')

@client.event
async def on_ready():
    print('Bot is logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user or message.author.bot:
        return
    content = message.content.lower()[len(PREFIX):]
    print(content)
    if(content.startswith('counter')):
        await counter(message)
    else:
        await etc(message)

async def counter(message):
    print(message.author.id)
    ret = ''
    for userID in CATALOG[str(message.guild.id)]:
        user = await client.fetch_user(str(userID))
        n = CATALOG[str(message.guild.id)][userID]
        ret += f'{user} has said nice {n} times.\n'
    await message.channel.send(ret)

async def etc(message):
    if re.compile(r'n+i+c+e+').search(message.content) or re.compile(r'n+ *i+ *c+ *e+').search(message.content):
        if(not str(message.guild.id) in CATALOG):
            CATALOG[str(message.guild.id)] = {}
        CATALOG[str(message.guild.id)][str(message.author.id)] = CATALOG.get(str(message.guild.id)).get(str(message.author.id), 0) + 1
        with open('data.json', 'w') as DATA_FILE:
            json.dump(CATALOG, DATA_FILE)
        print(CATALOG)
    

client.run(TOKEN)
DATA_FILE.close()