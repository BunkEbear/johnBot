#import interaction node class
from interactions import interactionNode
#import async function which actually does the stuff
from commands import chooseAction
import asyncio

import json
import discord

print("STARTTTTT")

with open('johnConfig.json') as johnConfig:
    config = json.load(johnConfig)

token = config['discordToken']



async def storeInteraction(currentIntNode):

    def generateId(currentIntNode):
        currentIntNode.id = None

    return


#set up for later to lock into desired server
defaultServer = None
defaultChannel = None

###############################################################

intents = discord.Intents.all()
#intents.message_content = True
#intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():

    activity = discord.Activity(type=discord.ActivityType.listening, name="@john help")  
    await client.change_presence(activity=activity)

    print(f'WE ARE INSIDE OF {client.user}')


#when a message happens anywhere it can see
@client.event
async def on_message(message):

    global defaultServer

    #if the message is not from the bot itself (infinite loop moment), if its in a dm, or if the message starts with the bot's mention
    if (message.author == client.user) and (isinstance(message.channel, discord.DMChannel)):
        return

    asyncio.create_task(handle_message(message))


async def handle_message(message):

    global defaultServer
    global defaultChannel


    print("seen")


    observedMessage = interactionNode()
    
    observedMessage.client = client

    #unless specified its passive
    observedMessage.naturalInteraction = True

    observedMessage.messageContents = message.content

    observedMessage.sender = message.author

    #if its a dm
    if (isinstance(message.channel, discord.DMChannel)):
        observedMessage.interactionType = 'dm'
        observedMessage.naturalInteraction = False
    else:
        observedMessage.interactionType = 'public'
    

    #if someone pings the bot
    if (message.content.startswith(client.user.mention)):
        #remove the mention from the message
        content_after_mention = message.content[len(client.user.mention):].strip()
        observedMessage.messageContents = content_after_mention
        observedMessage.naturalInteraction = False

        
    
    if(observedMessage.naturalInteraction):            
        await storeInteraction(observedMessage)
        return

    #only continues if it was directed at bot
    print("seen seeing")

    #try:
    print("trying to see if default server")
    
    #if there is a default server set
    if defaultServer:

        importanceChecker = observedMessage.messageContents.strip()
        if not (importanceChecker):
            await message.channel.send(f'hi')
            return

        print(f'attempting to run in default server {defaultServer}')
        
        #allows dm commands to run in the servers
        observedMessage.guild = defaultServer
        observedMessage.channel = defaultChannel
        


        observedMessage.messageObject = message



############################    CHOOOSE ACTION CALL   ################################################################
        response = await chooseAction(observedMessage)

        #no use in storing commands I think
        #storeInteraction(observedMessage)

        #embed whatever the response is into a string for got sake

        #finish(response)

        #def finish(message):

        #if theres a real response
        if response:
             #if its a tuple it has a file
            if isinstance(response, tuple):
                await message.channel.send(content=response[0], files=response[1])

            #if its just a texticular message
            else:
                await message.channel.send(response)

    else:
        if message.guild:
            defaultServer = message.guild
            defaultChannel = message.channel

            

            print("default server set")
            print("LOCKED IN LOCKED IN LOCKED IN LOCKED IN")
            #await message.channel.send(f'LOCKED IN LOCKED IN LOCKED IN LOCKED IN')
            await handle_message(message)

            

        else:
            await message.channel.send(f'no default server set, cannot run commands')
            return


###############################################################


client.run(token)