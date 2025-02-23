import discord

class messageUser:

    from discord.ext import commands

######################################################################################
    def __init__(self):
        self.dmOnly = False
        self.syntax = "dm [user] [message]"
        self.description = "repeats [message] in a [user]'s dms from the default server, or can be specificed in SUFFIX"


    async def describe(self):
        
        howTo = ""
        
        howTo += self.description
        howTo += "\n"
        howTo += "\tSYNTAX: " + self.syntax

        return howTo
######################################################################################

    async def start(self, context):


        #repeatMessage = context.messageObject.content.removeprefix("say ").strip()
        
        orderOfOperations = context.messageContents.split()

        if len(orderOfOperations) < 2:
            await context.messageObject.channel.send("please issue a propper command with the syntax:" + self.syntax)
            return

        if len(orderOfOperations) < 3 and context.messageObject.attachments:
            await context.messageObject.channel.send("please issue a propper command with the syntax:" + self.syntax)
            return

        #repeatMessage = context.messageContents.removeprefix("dm ").strip()

        recipient = orderOfOperations[1]
        recipient = recipient.strip("<@!>")  # Handles both <@ID> and <@!ID> (nickname mentions)

        orderOfOperations = orderOfOperations[2:]

        message = " ".join(orderOfOperations)

        guild = context.guild  # Get the guild from the context from the default

        try:
            # Fetch member using ID or username
            if recipient.isdigit():
                
                print("searching by id")
                #make member actual member object via id
                member = await guild.fetch_member(int(recipient))
                print(f'found member {member}')
                #return f'found member {member}'
            else:
                print("searching by name")
                #make member actual member object via name
                member = discord.utils.get(guild.members, name=recipient)
                print(f'found member {member}')

            if not member:
                #if no such member
                return f"{recipient} is MIA :^("

            print(f"attempting to send message to {member}")

            if context.messageObject.attachments:

                files = [await attachment.to_file() for attachment in context.messageObject.attachments]
                await member.send(content=message, files=files)

            else:
                await member.send(message)


            #await context.messageObject.channel.send("sent")

            return "sent"
        
            #return

        except discord.Forbidden:
            return "can't do that im afraid"
        except discord.HTTPException:
            return "im afraid"
