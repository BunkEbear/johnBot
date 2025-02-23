#the john file if you will
import discord
import json
import os
from discord.ext import commands
import openai


class gptCaller:

######################################################################################
    def __init__(self, gptKey):

        self.dmOnly = False
        self.description = "Mimics a personality based on a given chat history and instructions"
        self.syntax = "anything that gets johns attention that is not otherwise a command"


        print('gpt call object has been made')

        #gpt call function has been made

        self.client = openai.OpenAI(api_key=gptKey)


        self.historyJsonPath = None
        self.history = []

        self.config = None

        self.name = None

        #configFile = os.path.join(os.path.dirname(__file__), '../johnConfig.json')
        selectedPersonality = os.path.join(os.path.dirname(__file__), '../johnPersonality.json')

        #with open('../johnConfig.json') as johnConfig:
        #    self.config = json.load(johnConfig)

        self.personality = None

        with open(selectedPersonality) as johnInstructions:
            self.personality = json.load(johnInstructions)
            self.name = self.personality["name"]

        #../../ is in discBot, not workingFootball
#pp = personality path lol
        pp = os.path.join(os.path.dirname(__file__), f'../../histories/{self.personality["name"]}.json')
        psHistory = None

        self.historyJsonPath = pp


        #if the file exists, read it
        if os.path.exists(pp):
            print("I think johns history exists for this personality")

            with open(pp) as history:
                #personality specific history
                psHistory = json.load(history)

                self.history = psHistory["messages"]
        else:
            print("making john's history file for this personality")

            # Create johnPersonality.json with default content
            newJsonPersonalityHistory = {
                "messages": []
            }
            with open(pp, 'w') as historyFile:
                            #dictionary to json, filename, indent
                json.dump(newJsonPersonalityHistory, historyFile, indent=4) #indent is just how many spaces used for intents
            
            self.history = newJsonPersonalityHistory["messages"]

        self.messages = []

        for instruction in self.personality["instructions"]:
            self.messages.append({"role": "system", "content": f"{instruction}"})


        self.messages.append({"role": "system", "content": "previously it was assumed that you have just recieved instructions on a personality you should mimic"})
        self.messages.append({"role": "system", "content": "MIMIC THIS PERSONALITY TO THE BEST OF YOUR ABILITY"})
        self.messages.append({"role": "system", "content": "next you will be given a chat history between you as this personality and an entity called chat in full or in summary if there is one to provide"})
        self.messages.append({"role": "system", "content": "do not forget who you are while reading the chats, you will be asked to respond to a new message from chat afterwards"})


        #append would add the array as an element so we extend
        self.messages.extend(self.history)






    async def describe(self):
        
        howTo = ""
        
        howTo += self.description
        howTo += "\n"
        howTo += "\tSYNTAX: " + self.syntax

        return howTo


######################################################################################
    #if I Could I would rename this to noirmal function instead of start but conformity has taken hold
    async def start(self, context):
        print('gpt call function call has been made')

        #something about a deeep copy idk i gotta retake data structures
        currMessages = self.messages.copy()

        currMessages.extend([
            {"role": "system", "content": "previous to this message you have been presumably given personality instructions, and a message history in full or partial summary if they exist."},
            {"role": "system", "content": "the next message from the user role is the latest from the entity with which this personality has been interacting with"},
            {"role": "system", "content": "this entity is assumed to be called chat."},
            {"role": "system", "content": "Apply what you know of the personality you're mimicking and chat history to reply to this next message!!!!!!!!!!!!!!"},
            {"role": "user", "content": context.messageObject.content},
            {"role": "system", "content": "Keep responses under 1900 characters!!!!!!!!!!!!!!!!!"}
        ])

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=currMessages,
                #messages = [{"role": "user", "content": "What is the capital of France?"}],
            )

            await context.messageObject.channel.send(response.choices[0].message.content)



            return

        except Exception as e:
            await context.messageObject.channel.send(str(f"Error: {e}"))
            return str(f"Error: {e}")