import discord

class nickNameApperatus:
    import json
    import os
    #I hope you like passing around strings lol
    import discord
    from discord.ext import commands

    #all prim and propper like
    currentDir = os.path.dirname(os.path.abspath(__file__))
    configPath = os.path.join(currentDir, '../johnConfig.json')

    with open(configPath) as johnConfig:
        config = json.load(johnConfig)

    token = config['discordToken']


######################################################################################
    #in this case context is supposed to be a list of strings
    def __init__(self):
        """
        Changes the nickname of a specified user.
        Expected input: [command, user_id or username, new nickname]
        """
        self.dmOnly = False
        self.syntax = "nick [user] [new nickname]"
        self.description = "changes the nickname of a user in the default server, or can be specified in SUFFIX"





    async def describe(self):
        
        howTo = ""
        
        howTo += self.description
        howTo += "\n"
        howTo += "\tSYNTAX: " + self.syntax

        return howTo

######################################################################################
    async def start(self, context):

        guild = context.guild  # Get the guild from the context from the default

        message = context.messageContents
        message = message.split()

        print(f"changing a nick in {guild}")
        print(message)


        # Error handling for missing arguments
        #nick, user, nickName
        if len(message) < 3:
            print('has detected a lack of arguments')
            return "please issue a propper 'nick user nickName' command"
            
        #get the command parts
        guyChanging = message[1]  # User ID or name
        guyChanging = guyChanging.strip("<@!>")  # Handles both <@ID> and <@!ID> (nickname mentions)


        newNick = " ".join(message[2:])  # Combine nickname parts


        try:
            # Fetch member using ID or username
            if guyChanging.isdigit():
                
                print("searching by id")
                #make member actual member object via id
                member = await guild.fetch_member(int(guyChanging))
                print(f'found member {member}')
                #return f'found member {member}'
            else:
                print("searching by name")
                #make member actual member object via name
                member = discord.utils.get(guild.members, name=guyChanging)
                print(f'found member {member}')

            if not member:
                #if no such member
                return f"{guyChanging} is MIA :^("

            # Change nickname
            await member.edit(nick=newNick)
            print(f"{member.display_name} is now {newNick}")
            return f"{member.display_name} is now {newNick}"


        except discord.Forbidden:
            return "can't do that im afraid"
        except discord.HTTPException:
            return "im afraid"
