import discord

class listMembers:

    #I hope you like passing around strings lol
    from discord.ext import commands

    #all prim and propper like

######################################################################################

    #in this case context is supposed to be a list of strings
    def __init__(self):
        """
        Changes the nickname of a specified user.
        Expected input: [command, user_id or username, new nickname]
        """

        self.dmOnly = True
        self.syntax = "members"
        self.description = "lists all members in the DEFAULT SERVER, or can be specified in SUFFIX"

    #to do: make a master class
    async def describe(self):
        
        howTo = ""
        
        howTo += self.description
        howTo += "\n"
        howTo += "\tSYNTAX: " + self.syntax

        return howTo

######################################################################################
 
    async def start(self, context):

        if context.interactionType == 'public':
            return "this command is only available in dms"
        
        guild = context.guild  # Get the guild from the context from the default

        members = guild.members

        #membersMentionStringsList = []

        for member in members:
            print(member.name)

            #change this shit back if I get banned
            await context.messageObject.channel.send(member.mention)  # send a list of member names

            #membersMentionStringsList.append(member.mention)

        #await context.messageObject.channel.send('\n'.join(membersMentionStringsList))  # send a list of member names

