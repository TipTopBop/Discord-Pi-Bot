import discord
from discord.ext import commands
import random
import os.path
import socket
import sys
from forex_python.bitcoin import BtcConverter



TOKEN = 'BOT TOKEN HERE'

bot = commands.Bot(command_prefix = '!')



@bot.event
async def on_ready():
    print('Logged in as\n' + bot.user.name + '\n' + bot.user.id + '\n' + 'Python: {}'.format(sys.version) + '\n------')

    with open('status.txt', 'r') as f_o:
        await bot.change_presence(game=discord.Game(name=f_o.readline()), status=None, afk=False)



@bot.event
async def on_server_role_delete(role):
    if os.path.isfile('/home/pi/pi_bot/roles/' + role.server.id + '.txt'):
        with open('/home/pi/pi_bot/roles/' + role.server.id + '.txt', 'r') as f_o:
            rolefile = f_o.readline()
            if role.id in rolefile:
                rolefile = rolefile.replace(role.id + 'x', '', 1)
            if rolefile == '':
                os.remove('/home/pi/pi_bot/roles/' + role.server.id + '.txt')
            else:
                with open('/home/pi/pi_bot/roles/' + role.server.id + '.txt', 'w') as f_o:
                    f_o.write(rolefile)



@bot.event
async def on_member_join(member):
    if os.path.isfile('/home/pi/pi_bot/autoassign/' + member.server.id + '.txt'):
        for item in member.server.roles:
            with open('/home/pi/pi_bot/autoassign/' + member.server.id + '.txt', 'r') as f_o:
                if item.id in f_o.readline():
                    await bot.add_roles(member, item)



@bot.event
async def on_message(message):
    
    
    
    #Commands
    if not message.author.id == '375343366126436355' and message.content.startswith('!'):
        
        
        
        #Bool checks
        purgecheck = 'placeholder'
        
        
        
        #Help Commands
        if message.content.startswith ('!help'):
            embed = discord.Embed(title='Help', description='Subcommands for help on categories.')
            embed.add_field(name='!help', value='Shows this message.', inline=True)
            embed.add_field(name='!rolehelp', value='Role System Commands', inline=True)
            embed.add_field(name='!adminhelp', value='Admin-only commands.', inline=True)
            embed.add_field(name='!mischelp', value='Miscellaneous Commands.', inline=True)
            embed.add_field(name='Twitter Updates:', value='https://twitter.com/discord_pi_bot')
            embed.set_footer(text='Use !help, !rolehelp, !adminhelp, or !mischelp for other commands.')
            await bot.send_message(message.channel, embed=embed)
        elif message.content.startswith('!rolehelp'):
            embed = discord.Embed(title='!role Subcommands', description='A list of roles members can choose between.')
            embed.add_field(name='!role', value='Subcommands:\nview - Sends the list\nset - Gives you the role you specify in the list (NOT @mention).\nAdmin-only Subcommands:\nadd - Adds the @mentioned role to the list.\nremove - Removes the @mentioned role from the list.\nclear - Clears the list.', inline=False)
            embed.set_footer(text='Use !help, !rolehelp, !adminhelp, or !mischelp for other commands.')
            await bot.send_message(message.channel, embed=embed)
        elif message.content.startswith('!adminhelp'):
            embed = discord.Embed(title='Admin-Only Commands', description='Only members with the Administrator permission can use these commands.')
            embed.add_field(name='!purge', value='Mass deletes messages. Ex: !purge 20', inline=False)
            embed.add_field(name='!addroles', value='Adds roles you specify to a list of roles, members can assign themselves one of them with !setrole. Ex: !addroles @role1 @role2', inline=False)
            embed.add_field(name='!autoassign', value='Adds a role to be automatically assigned to a user when they join.\nSubcommands:\nview - Shows the autoassign list.\nadd - adds the @mentioned roles to the list.\nremove - removes the @mentioned roles from the list.\nclear - Clears the list.', inline=False)
            embed.set_footer(text='Use !help, !rolehelp, !adminhelp, or !mischelp for other commands.')
            await bot.send_message(message.channel, embed=embed)
        elif message.content.startswith('!mischelp'):
            embed = discord.Embed(title='Miscellaneous Commands', description='Commands that don\'t fall under any !help category')
            embed.add_field(name='!lfg', value='Adds or removes you from the "Looking for game" list in that channel.', inline=False)
            embed.add_field(name='!lfg list', value='Shows the "Looking for game" list in that channel.', inline=False)
            embed.add_field(name='!btc', value='Sends the Bitcoin Exchange rate.', inline=False)
            embed.add_field(name='!pfp', value='Gets the profile picture of the @mentioned user.', inline=False)
            embed.set_footer(text='Use !help, !rolehelp, !adminhelp, or !mischelp for other commands.')
            await bot.send_message(message.channel, embed=embed)
            
        
        
        
        if not message.channel.is_private:
            
            
            
            #Dev Commands
            if message.author.id == 'YOUR ID HERE':
                if message.content.startswith('!setstatus'):
                    status = message.content[11:len(message.content)]
                    with open('status.txt', 'w') as f_o:
                        f_o.write(status)
                    await bot.change_presence(game=discord.Game(name=status), status=None, afk=False)
                    await bot.send_message(message.channel, message.author.mention + ' changed status to ' + status)
                elif message.content.startswith('!say'):
                    await bot.send_message(message.channel, message.content.replace('!say ', '', 1))
                elif message.content.startswith('!send'):
                    channel = message.content[0:24].replace('!send ', '', 1)
                    await bot.send_message(bot.get_channel(channel), message.content[25:len(message.content)])
                elif message.content.startswith('!servers'):
                    msg = ''
                    for item in bot.servers:
                        msg = msg + item.name + ' ' + str(len(item.members)) + '\n'
                    await bot.send_message(message.channel, msg)
                elif message.content.startswith('!announcement'):
                    for server in bot.servers:
                        for channel in server.channels:
                            if channel.type == discord.ChannelType.text:
                                if channel.permissions_for(server.me).send_messages:
                                    if channel.name == 'general':
                                        embed=discord.Embed(title='Message From Developer ' + message.author.name, description=message.content.replace('!announcement ', '', 1))
                                        await bot.send_message(channel, embed=embed)
                                        break
            
            
            
            #Administrator-Only Commands
            if message.author.server_permissions.administrator or message.author.id == '268138118270418954':
                if message.content.startswith('!purge'):
                    if int(message.content[7:10]) == 0:
                        await bot.send_message(message.channel, message.author.mention + ' Cannot delete 0 messages.')
                    else:
                        purgecheck = 'a'
                        await bot.delete_message(message)
                        deleted = await bot.purge_from(message.channel, limit=int(message.content[7:10]), check=None)
                        await bot.send_message(message.channel, message.author.mention + ' Successfully deleted {} message(s).'.format(len(deleted)))
                elif message.content.startswith('!autoassign'):
                    if message.content[12:16] == 'view':
                        if not os.path.isfile('/home/pi/pi_bot/autoassign/' + message.server.id + '.txt'):
                            await bot.send_message(message.channel, message.author.mention + ' The autoassign list is empty.')
                        else:
                            with open('/home/pi/pi_bot/autoassign/' + message.server.id + '.txt', 'r') as f_o:
                                fileline = f_o.readline()
                            rolelist = ''
                            for item in message.server.roles:
                                if item.id in fileline:
                                    rolelist = rolelist + item.name + '\n'
                            embed = discord.Embed(title='Autoassign List:', description=rolelist)
                            embed.set_footer(text='Requested by ' + message.author.name)
                            await bot.send_message(message.channel, embed=embed)
                    elif message.content[12:17] == 'clear':
                        if os.path.isfile('/home/pi/pi_bot/autoassign/' + message.server.id + '.txt'):
                            os.remove('/home/pi/pi_bot/autoassign/' + message.server.id + '.txt')
                            await bot.send_message(message.channel, message.author.mention + ' Cleared autoassign list.')
                        else:
                            await bot.send_message(message.channel, message.author.mention + ' The autoassign list is already empty.')
                    elif message.content[12:15] == 'add':
                        if len(message.role_mentions) == 0:
                            await bot.send_message(message.channel, message.author.mention + ' Make sure to mention the role(s) to add.')
                        else:
                            if not os.path.isfile('/home/pi/pi_bot/autoassign/' + message.server.id + '.txt'):
                                with open('/home/pi/pi_bot/autoassign/' + message.server.id + '.txt', 'w') as f_o:
                                    f_o.write('')
                            with open('/home/pi/pi_bot/autoassign/' + message.server.id + '.txt', 'r') as f_o:
                                fileline = f_o.readline()
                            with open('/home/pi/pi_bot/autoassign/' + message.server.id + '.txt', 'w') as f_o:
                                for item in message.role_mentions:
                                    fileline = fileline + item.id + 'x'
                                f_o.write(fileline)
                            addedroles = ''
                            for item in message.role_mentions:
                                if item.id in fileline:
                                    addedroles = addedroles + item.name + ' '
                            rolelist = ''
                            for item in message.server.roles:
                                if item.id in fileline:
                                    rolelist = rolelist + item.name + '\n'
                            embed = discord.Embed(title='Autoassign List:', description=rolelist)
                            embed.add_field(name='Added Roles:', value=addedroles, inline=False)
                            embed.set_footer(text='Requested by ' + message.author.name)
                            await bot.send_message(message.channel, embed=embed)
                    elif message.content[12:18] == 'remove':
                        if not os.path.isfile('/home/pi/pi_bot/autoassign/' + message.server.id + '.txt'):
                            await bot.send_message(message.channel, message.author.mention + ' The autoassign list is empty.')
                        else:
                            with open('/home/pi/pi_bot/autoassign/' + message.server.id + '.txt', 'r') as f_o:
                                fileline = f_o.readline()
                            removedroles = ''
                            for item in message.role_mentions:
                                if item.id in fileline:
                                    fileline = fileline.replace(item.id + 'x', '', 1)
                                    removedroles = removedroles + item.name + ' '
                            if fileline == '':
                                os.remove('/home/pi/pi_bot/autoassign/' + message.server.id + '.txt')
                                await bot.send_message(message.channel, message.author.mention + ' Cleared autoassign list.')
                            else:
                                if removedroles == '':
                                    await bot.send_message(message.channel, message.author.mention + ' Mentioned roles aren\'t in the list.')
                                else:
                                    with open('/home/pi/pi_bot/autoassign/' + message.server.id + '.txt', 'w') as f_o:
                                        f_o.write(fileline)
                                    rolelist = ''
                                    for item in message.server.roles:
                                        if item.id in fileline:
                                            rolelist = rolelist + item.name + '\n'
                                    embed = discord.Embed(title='Autoassign List:', description=rolelist)
                                    embed.add_field(name='Removed Roles:', value=removedroles, inline=False)
                                    embed.set_footer(text='Requested by ' + message.author.name)
                                    await bot.send_message(message.channel, embed=embed)
                    else:
                        embed = discord.Embed(title='Not a valid subcommand')
                        embed.add_field(name='!autoassign (Subcommand)', value='view - Shows the autoassign list.\nadd - adds the @mentioned roles to the list.\nremove - removes the @mentioned roles from the list.\nclear - Clears the list.', inline=False)
                        embed.set_footer(text='Requested by ' + message.author.name)
                        await bot.send_message(message.channel, embed=embed)
                
                
            
            
            #Role Commands
            if message.content.startswith('!role') and not message.content.startswith('!rolehelp'):
                if message.content[6:10] == 'view':
                    if not os.path.isfile('/home/pi/pi_bot/roles/' + message.server.id + '.txt'):
                        await bot.send_message(message.channel, message.author.mention + ' The role list is empty.')
                    else:
                        with open('/home/pi/pi_bot/roles/' + message.server.id + '.txt', 'r') as f_o:
                            fileline = f_o.readline()
                        rolelist = ''
                        for item in message.server.roles:
                            if item.id in fileline:
                                rolelist = rolelist + item.name + '\n'
                        embed = discord.Embed(title='Role List:', description=rolelist)
                        embed.set_footer(text='Requested by ' + message.author.name)
                        await bot.send_message(message.channel, embed=embed)
                elif message.content[6:9] == 'set':
                    if not os.path.isfile('/home/pi/pi_bot/roles/' + message.server.id + '.txt'):
                        await bot.send_message(message.channel, message.author.mention + ' The role list is empty.')
                    else:
                        rolelist = await bot.get_server_roles(message.server)
                        removerole = ''
                        real = False
                        for role in rolelist:
                            if role in message.author.roles:
                                removerole = role
                            if role.name == message.content.replace('!role set ', '', 1):
                                setrole = role
                                real = True
                        if real == False:
                            await bot.send_message(message.channel, message.author.mention + ' That role doesn\'t exist, use !rolehelp for help.')
                        else:
                            embed = discord.Embed(title='Set role to:', description=setrole.name)
                            if not removerole == '':
                                await bot.remove_roles(message.author, removerole)
                                embed.add_field(name='Removed role:', value=removerole.name, inline=True)
                            embed.set_footer(text='Requested by ' + message.author.name)
                            await bot.add_roles(message.author, setrole)
                            await bot.send_message(message.channel, embed=embed)
                elif message.author.server_permissions.administrator or message.author.id == '268138118270418954':
                    if message.content[6:11] == 'clear':
                        if os.path.isfile('/home/pi/pi_bot/roles/' + message.server.id + '.txt'):
                            os.remove('/home/pi/pi_bot/roles/' + message.server.id + '.txt')
                            await bot.send_message(message.channel, message.author.mention + ' Cleared role list.')
                        else:
                            await bot.send_message(message.channel, message.author.mention + ' The role list is already empty.')
                    elif message.content[6:9] == 'add':
                        if len(message.role_mentions) == 0:
                            await bot.send_message(message.channel, message.author.mention + ' Make sure to mention the role(s) to add.')
                        else:
                            if not os.path.isfile('/home/pi/pi_bot/roles/' + message.server.id + '.txt'):
                                with open('/home/pi/pi_bot/roles/' + message.server.id + '.txt', 'w') as f_o:
                                    f_o.write('')
                            with open('/home/pi/pi_bot/roles/' + message.server.id + '.txt', 'r') as f_o:
                                fileline = f_o.readline()
                            with open('/home/pi/pi_bot/roles/' + message.server.id + '.txt', 'w') as f_o:
                                for item in message.role_mentions:
                                    fileline = fileline + item.id + 'x'
                                f_o.write(fileline)
                            addedroles = ''
                            for item in message.role_mentions:
                                if item.id in fileline:
                                    addedroles = addedroles + item.name + ' '
                            rolelist = ''
                            for item in message.server.roles:
                                if item.id in fileline:
                                    rolelist = rolelist + item.name + '\n'
                            embed = discord.Embed(title='Role List:', description=rolelist)
                            embed.add_field(name='Added Roles:', value=addedroles, inline=False)
                            embed.set_footer(text='Requested by ' + message.author.name)
                            await bot.send_message(message.channel, embed=embed)
                    elif message.content[6:12] == 'remove':
                        if not os.path.isfile('/home/pi/pi_bot/roles/' + message.server.id + '.txt'):
                            await bot.send_message(message.channel, message.author.mention + ' The role list is empty.')
                        else:
                            with open('/home/pi/pi_bot/roles/' + message.server.id + '.txt', 'r') as f_o:
                                fileline = f_o.readline()
                            removedroles = ''
                            for item in message.role_mentions:
                                if item.id in fileline:
                                    fileline = fileline.replace(item.id + 'x', '', 1)
                                    removedroles = removedroles + item.name + ' '
                            if fileline == '':
                                os.remove('/home/pi/pi_bot/roles/' + message.server.id + '.txt')
                                await bot.send_message(message.channel, message.author.mention + ' Cleared role list.')
                            else:
                                if removedroles == '':
                                    await bot.send_message(message.channel, message.author.mention + ' Mentioned roles aren\'t in the list.')
                                else:
                                    with open('/home/pi/pi_bot/roles/' + message.server.id + '.txt', 'w') as f_o:
                                        f_o.write(fileline)
                                    rolelist = ''
                                    for item in message.server.roles:
                                        if item.id in fileline:
                                            rolelist = rolelist + item.name + '\n'
                                    embed = discord.Embed(title='Role List:', description=rolelist)
                                    embed.add_field(name='Removed Roles:', value=removedroles, inline=False)
                                    embed.set_footer(text='Requested by ' + message.author.name)
                                    await bot.send_message(message.channel, embed=embed)
                    else:
                        embed = discord.Embed(title='Not a valid subcommand')
                        embed.add_field(name='!role (Subcommand)', value='view - Shows the role list.\nadd - adds the @mentioned roles to the list.\nremove - removes the @mentioned roles from the list.\nclear - Clears the list.', inline=False)
                        embed.set_footer(text='Requested by ' + message.author.name)
                        await bot.send_message(message.channel, embed=embed)
            
            
            
            #Misc. Commands
            if message.content.startswith('!lfg'):
                if message.content[5:9] == 'list':
                    if not os.path.isfile('/home/pi/pi_bot/lfg/' + message.channel.id + '.txt'):
                        embed=discord.Embed(title='There is currently no one looking for a game')
                    else:
                        with open('/home/pi/pi_bot/lfg/' + message.channel.id + '.txt', 'r') as f_o:
                            file = f_o.readline()
                        msg = ''
                        for member in message.server.members:
                            if member.id in file:
                                msg = msg + member.name + '\n'
                        embed=discord.Embed(title='User(s) looking for a game:', description=msg)
                else:
                    if not os.path.isfile('/home/pi/pi_bot/lfg/' + message.channel.id + '.txt'):
                        with open('/home/pi/pi_bot/lfg/' + message.channel.id + '.txt', 'w') as f_o:
                            f_o.write(message.author.id + 'x')
                            embed=discord.Embed(title='You are now looking for game')
                    else:
                        with open('/home/pi/pi_bot/lfg/' + message.channel.id + '.txt', 'r') as f_o:
                            file = f_o.readline()
                        if message.author.id in file:
                            file = file.replace(message.author.id + 'x', '', 1)
                            if file == '':
                                await bot.send_message(message.channel, 'here')
                                os.remove('/home/pi/pi_bot/lfg/' + message.channel.id + '.txt')
                            else:
                                with open('/home/pi/pi_bot/lfg/' + message.channel.id + '.txt', 'w') as f_o:
                                    f_o.write(file)
                            embed=discord.Embed(title='You are no longer looking for a game')
                        else:
                            file = file + message.author.id + 'x'
                            embed=discord.Embed(title='You are now looking for a game')
                            with open('/home/pi/pi_bot/lfg/' + message.channel.id + '.txt', 'w') as f_o:
                                f_o.write(file)
                embed.set_footer(text='Requested By: ' + message.author.name)
                await bot.send_message(message.channel, embed=embed)
            elif message.content.startswith('!pfp'):
                if len(message.mentions) == 0:
                    await bot.send_message(message.channel, message.author.mention + ' Make sure to mention the user.')
                else:
                    await bot.send_message(message.channel, message.mentions[0].avatar_url)
            elif message.content.startswith('!btc'):
                await bot.delete_message(message)
                loadingmsg = await bot.send_message(message.channel, 'Getting bitcoin rates...')
                btc = BtcConverter(force_decimal=True)
                embed = discord.Embed(title='Bitcoin -> Currency:', description='USD: $' + str(btc.get_latest_price('USD'))[0:8] + '\nCAD: $' + str(btc.get_latest_price('CAD'))[0:8] + '\nEUR: €' + str(btc.get_latest_price('EUR'))[0:8] + '\nAUD: $' + str(btc.get_latest_price('AUD'))[0:8])
                embed.add_field(name='Currency -> Bitcoin:', value='USD: ฿' + str(btc.convert_to_btc(1, 'USD'))[0:10] + '\nCAD: ฿' + str(btc.convert_to_btc(1, 'CAD'))[0:10] + '\nEUR: ฿' + str(btc.convert_to_btc(1, 'EUR'))[0:10] + '\nAUD: ฿' + str(btc.convert_to_btc(1, 'AUD'))[0:10], inline=False)
                embed.set_thumbnail(url="https://bitcoin.org/img/icons/opengraph.png")
                embed.set_footer(text='Requested by ' + message.author.name)
                await bot.send_message(message.channel, embed=embed)
                await bot.delete_message(loadingmsg)
                return
	    
	    
	    
	    #End Of Command Constants
            if purgecheck == 'placeholder':
                await bot.delete_message(message)



#Misc Fuctions
@bot.event
async def get_server_roles(server):
    serverrolesfunc = []
    with open('/home/pi/pi_bot/roles/' + server.id + '.txt', 'r') as f_o:
        fileline = f_o.readline()
        for role in server.roles:
            if role.id in fileline:
                serverrolesfunc.append(role)
        return serverrolesfunc

bot.run(TOKEN)