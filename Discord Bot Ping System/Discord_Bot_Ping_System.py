import discord
import openai
import random
from discord import app_commands
from datetime import datetime, timedelta


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.ping_trigger_enabled = True
        self.disable_trigger_time = None
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        await self.tree.sync(guild=discord.Object(id=335903736142626827))
        await self.tree.sync()
        self.tree.copy_global_to(guild=discord.Object(id=335903736142626827))

# Time of the last embed message
last_embed_time = None

intents = discord.Intents.default()
client = MyClient(intents=intents)
openai.api_key = "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"


EmbedFooter = 'Serperior Pinging Services | Version 2.2.1 | -Snivy Films'

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="your discussions"))
    print(f'{client} has successfully connected')

# List of customizable messages
with open("messages.txt", "r", encoding="utf-8") as f:
    messages = [line.strip() for line in f]
# List of customizable gifs
with open("gifs.txt", "r", encoding="utf-8") as f:
    gifs = [line.strip() for line in f]
# List of logs
with open("logs.txt", "r", encoding="utf-8") as f:
    logs = [line.strip() for line in f]

@client.event
async def on_message(message):
    global last_embed_time
    if client.ping_trigger_enabled and message.mentions:
        if message.mentions:
            # Check if 2 minutes have passed since the last embed message
            if last_embed_time is None or datetime.now() - last_embed_time > timedelta(minutes=2):
                if random.random() < 0.5:
                    response = random.choice(messages)
                    embed = discord.Embed(title="Ping Trigger", description=f"{message.author.mention} - {response}", color=0x00ffbd)
                    embed.set_footer(text= EmbedFooter)
                else:
                    response = random.choice(gifs)
                    embed = discord.Embed(title="Ping Trigger", description=f"{message.author.mention}", color=0x00ffbd)
                    embed.set_footer(text= EmbedFooter)
                    embed.set_image(url=response)
                await message.channel.send(embed=embed)
                last_embed_time = datetime.now()

#Add new messages to the ping trigger
@client.tree.command(name = "add-message", description = "Add a new message to the ping trigger")
async def self(interaction: discord.Interaction, message:str):
    try:
        with open("messages.txt", "a", encoding='utf-8') as f:
            f.write(message + "\n")
        with open("logs.txt", "a", encoding='utf-8') as f:
            f.write(f"{datetime.now()} - {interaction.user} added a new message: {message} in {interaction.guild}\n")
        embed = discord.Embed(title="New Ping Trigger Message", description=f"{interaction.user.mention} - You have sucessfully added a new message: {message}", color=0x00ffbd)
        embed.set_footer(text= EmbedFooter)
        await interaction.response.send_message(embed=embed)
        with open("messages.txt", "r") as f:
            messages = [line.strip() for line in f]
    except UnicodeEncodeError:
        embed = discord.Embed(title="Error Code 1", description="The message could not be added because it is not in the UTF-8 format. Please try again. If you are sure that the message is in UTF-8 format please contact the bot handler.", color=0xff0000)
        embed.set_footer(text= EmbedFooter)
        await interaction.response.send_message(embed=embed)

#Add new gifs to the ping trigger
@client.tree.command(name = "add-gifs", description = "Add a new gif to the ping trigger")
async def self(interaction: discord.Interaction, gif:str):
    try:
        with open("gifs.txt", "a", encoding='utf-8') as f:
            f.write(gif + "\n")
        with open("logs.txt", "a", encoding='utf-8') as f:
            f.write(f"{datetime.now()} - {interaction.user} added a new gif: {gif} in {interaction.guild}\n")
        embed = discord.Embed(title="New Ping Trigger Message", description=f"{interaction.user.mention} - You have sucessfully added a new gif", color=0x00ffbd)
        embed.set_footer(text=EmbedFooter)
        embed.set_image(url=gif)
        await interaction.response.send_message(embed=embed)
        with open("gifs.txt", "r") as f:
            gifs = [line.strip() for line in f]
    except UnicodeEncodeError:
        embed = discord.Embed(title="Error Code 3", description="The gif could not be added because the link is not in the UTF-8 format. Please try again. If you are sure that the message is in UTF-8 format please contact the bot handler.", color=0xff0000)
        embed.set_footer(text= EmbedFooter)
        await interaction.response.send_message(embed=embed)

#Get the count of messages that can be sent
@client.tree.command(name="message-count", description="Get the amount of messages for the ping trigger")
async def self(interaction: discord.Interaction):
    try:
        with open("messages.txt", "r", encoding='utf-8') as f:
            messages = [line.strip() for line in f]
            count = len(messages)
            embed = discord.Embed(title="Message Count", description=f"{interaction.user.mention} - There are {count} messages in the ping trigger messages file", color=0x00ffbd)
            embed.set_footer(text=EmbedFooter)
            await interaction.response.send_message(embed=embed)
            with open("logs.txt", "a", encoding="utf-8") as f:
                f.write(f"{datetime.now()} - {interaction.user} checked the message count in {interaction.guild}\n")
    except Exception as e:
        embed = discord.Embed(title="Error Code 2", description=f"Something has gone critically wrong. Contact the bot master immediately. Include what you were doing to cause the error to occur", color=0xff0000)
        embed.set_footer(text=EmbedFooter)
        await interaction.response.send_message(embed=embed)

#Get the count of gifs that can be sent
@client.tree.command(name="gif-count", description="Get the amount of gifs for the ping trigger")
async def self(interaction: discord.Interaction):
    try:
        with open("gifs.txt", "r", encoding='utf-8') as f:
            gifs = [line.strip() for line in f]
            count = len(gifs)
            embed = discord.Embed(title="Message Count", description=f"{interaction.user.mention} - There are {count} messages in the ping trigger gifs file", color=0x00ffbd)
            embed.set_footer(text=EmbedFooter)
            await interaction.response.send_message(embed=embed)
            with open("logs.txt", "a", encoding="utf-8") as f:
                f.write(f"{datetime.now()} - {interaction.user} checked the gif count in {interaction.guild}\n")
    except Exception as e:
        embed = discord.Embed(title="Error Code 2", description=f"Something has gone critically wrong. Contact the bot master immediately. Include what you were doing to cause the error to occur", color=0xff0000)
        embed.set_footer(text=EmbedFooter)
        await interaction.response.send_message(embed=embed)
        
#Disables the ping trigger
@client.tree.command(name="disable-ping-trigger", description="Disable the ping trigger for 5 minutes")
async def disable_ping_trigger(interaction: discord.Interaction):
    if client.ping_trigger_enabled:
        client.ping_trigger_enabled = False
        client.disable_trigger_time = datetime.now() + timedelta(minutes=5)
        embed = discord.Embed(
            title="Ping Trigger Disabled",
            description=f"{interaction.user.mention} - The ping trigger has been disabled for 5 minutes. Ping away",
            color=0x00ffbd,
        )
        embed.set_footer(text=EmbedFooter)
        await interaction.response.send_message(embed=embed)
        with open("logs.txt", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()} - {interaction.user} disabled the ping trigger in {interaction.guild} for 5 minutes\n")
    else:
        embed = discord.Embed(
            title="Ping Trigger Already Disabled",
            description=f"{interaction.user.mention} - The ping trigger is already disabled.",
            color=0xff0000,
        )
        embed.set_footer(text=EmbedFooter)
        await interaction.response.send_message(embed=embed)
        
#Update log
@client.tree.command(name="update-log", description="Gets what most recently changed")
async def update_log(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Update Log",
        description=f"{interaction.user.mention}\n With update 2.2.1 ChatGPT command has been updated with formatting for prompt and responces.\nWith update 2.2.0 a new command has been added called /chatgpt which allows you to use chatgpt.",
        color=0x00ffbd,
    )
    embed.set_footer(text=EmbedFooter)
    await interaction.response.send_message(embed=embed)
    
#ChatGPT
@client.tree.command(name="chatgpt", description="Use ChatGPT")
async def ChatGPT(interaction: discord.Interaction, prompt:str):
    # Send an initial response
    initial_response = await interaction.response.defer()

    # Generate the response from the model
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt
            },
        ],
    )

    # Create the embed message
    embed = discord.Embed(
        title="ChatGPT 3.5",
        description=f"`Your Prompt:` {prompt}\n \n `Response:`\n \n{response.choices[0].message.content}",
        color=0x00ffbd,
    )
    embed.set_footer(text=EmbedFooter)
    embed = embed
    # Edit the initial response with the generated content
    msg = await interaction.original_response()
    await msg.edit(embed=embed)

    # Log the usage
    with open("logs.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} - {interaction.user} used ChatGPT with the prompt {prompt} in {interaction.guild}\n")


client.run("Bot Token")
