import discord

class theMimic:

    from discord.ext import commands

######################################################################################
    def __init__(self):
        self.dmOnly = True
        self.syntax = "say [message]"
        self.description = "repeats [message] in the DEFAULT CHANNEL, or can be specificed in SUFFIX"

    async def describe(self):
        
        howTo = ""
        
        howTo += self.description
        howTo += "\n"
        howTo += "\tSYNTAX: " + self.syntax

        return howTo
######################################################################################

    async def start(self, context):


        #repeatMessage = context.messageObject.content.removeprefix("say ").strip()
        
        repeatMessage = context.messageContents.removeprefix("say ").strip()

        

        #if context.messageObject. == 'public':
        #    return "this command is only available in dms"
        
        channel = context.channel  # Get the guild from the context from the default

        # Check for attachments
        if context.messageObject.attachments:

            if (repeatMessage == "say"):
                repeatMessage = ""

            files = [await attachment.to_file() for attachment in context.messageObject.attachments]
            await channel.send(content=repeatMessage, files=files)
        else:
            if (repeatMessage == "say"):
                await context.messageObject.channel.send("what do you want me to say?")
                return
                #await channel.send(await self.fuckedUp())
            await channel.send(repeatMessage)
    

    #async def fuckedUp(self):
    #    return "you fucked up"