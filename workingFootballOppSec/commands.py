from commandOpperators.gptCall import gptCaller

#import nickname command function
from commandOpperators.nick import nickNameApperatus
from commandOpperators.members import listMembers
from commandOpperators.mimic import theMimic
from commandOpperators.directMessage import messageUser

import discord
import openai
import json


messages = None
config = None

with open('johnConfig.json') as johnConfig:
    config = json.load(johnConfig)

with open('johnPersonality.json') as johnInstructions:
    instructions = json.load(johnInstructions)

#client = openai.OpenAI(api_key=config["gptKey"])
gptKey = config["gptKey"]
chatInstance = gptCaller(gptKey)


async def chooseAction(intendedMessage):

    nickFunction = nickNameApperatus()
    listMembersFunction = listMembers()
    mimicObject = theMimic()
    dmObject = messageUser()

    messageAsSeenOnTv = intendedMessage.messageContents

    #dont do shit if no spaces to begin with so we gotta try catch later
    orderOfOperations = messageAsSeenOnTv.split()


    try:
        currCommand = orderOfOperations[0].lower()
    
    except:
        currCommand = messageAsSeenOnTv

    potCommands = {
        #"vc" : (),
        #"play" : (),
        #"lights OFF": (),
        #"lights ON": (),
        #"channels": (),
        #"servers": (),
        "dm": (dmObject),
        "help":(lambda: help(intendedMessage,potCommands)),
        "say": (mimicObject),
        "members": (listMembersFunction), #list members
        "test": (lambda: test("pong")),
        "nick": (nickFunction)
    }

    #if the thing in there is not the object we think it is then continue

    try:
        
        commandObject = potCommands.get(currCommand)

        #if it was able to retrieve anything
        if (commandObject):
            print('relivant command found')
            #await delete_message(intendedMessage.messageObject)

            #if its an object
            if callable(commandObject):
                
                action = commandObject
            #if its a basic command
            else:
                action = lambda: commandObject.start(intendedMessage)
        
        #if it didnt find anything corresponding to the given command
        else:
            action = lambda: what(intendedMessage)

    
    except:
        await what(intendedMessage)


    #return to the main function with the command output    
    return await action()

async def test(string):
    return (string)

async def delete_message(message):
    try:
        await message.delete()
        print("Message deleted successfully.")
    except discord.Forbidden:
        print("Permission denied to delete the message.")
    except discord.HTTPException as e:
        print(f"Failed to delete the message: {e}")



async def what(intendedMessage):
    #return (f"I do not understand what you mean by this: '{message}'")
    #in this case start serves as like a normal response functiojn
    return await chatInstance.start(intendedMessage)







async def help(messageContainingObject, commandDict):

    majorDefinition = "**"

    minorDefinition = "*"

    channel = messageContainingObject.messageObject.channel

    helpMessage = ""

    for key, value in commandDict.items():
        if callable(value):
            continue

        command = key.upper()

        commandDescription = await value.describe()

        helpMessage += f"{majorDefinition}{command}{majorDefinition}"
        helpMessage += "\n"
        helpMessage += f"\t{minorDefinition}{commandDescription}"

        if value.dmOnly:
            helpMessage += f"\n\t(dm only){minorDefinition}"
        else:
            helpMessage += f"{minorDefinition}"

        helpMessage += "\n"
        

    #I dont care we do this at runtime it takes like minimal time for now

    helpMessage += f"``` SUFFIX"

    helpMessage += "\n"
    helpMessage +=f"\t"

    helpMessage +="COMEIING IF I NEED IT NOT IMPLIMENTED"
    helpMessage +="\n"
    helpMessage +="\tspecify a server and/or channel to be executed in/for."
    helpMessage +="\n"
    helpMessage +="\t[command in full] in [server] in [channel]"

    helpMessage +=f"```"

    #await channel.send(helpMessage)

    return helpMessage