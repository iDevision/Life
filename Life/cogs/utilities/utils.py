import codecs
import os
import pathlib
import random
import time

import discord
from discord.ext import commands


class Utils:

    def __init__(self, bot):
        self.bot = bot

    async def ping(self, ctx: commands.Context):

        latency_ms = f"{round(self.bot.latency * 1000)}ms"

        if self.bot.pings:
            pings = [latency for datetime, latency in list(self.bot.pings)]
            average_latency_ms = f"{round((sum(pings) / len(pings)))}ms"
        else:
            average_latency_ms = "Failed"

        typing_start = time.monotonic()
        await ctx.trigger_typing()
        typing_end = time.monotonic()
        typing_ms = f"{round((typing_end - typing_start) * 1000)}ms"

        discord_start = time.monotonic()
        async with self.bot.session.get("https://discordapp.com/") as resp:
            if resp.status == 200:
                discord_end = time.monotonic()
                discord_ms = f"{round((discord_end - discord_start) * 1000)}ms"
            else:
                discord_ms = "Failed"

        return latency_ms, average_latency_ms, typing_ms, discord_ms

    def linecount(self):

        docstring = False
        file_amount, functions, lines, classes = 0, 0, 0, 0

        for dirpath, dirname, filenames in os.walk("."):
            for name in filenames:

                if not name.endswith(".py"):
                    continue
                file_amount += 1

                with codecs.open("./" + str(pathlib.PurePath(dirpath, name)), "r", "utf-8") as files_lines:
                    for line in files_lines:
                        line = line.strip()
                        if len(line) == 0:
                            continue
                        elif line.startswith('"""'):
                            if docstring is False:
                                docstring = True
                            else:
                                docstring = False
                        elif docstring is True:
                            continue
                        if line.startswith("#"):
                            continue
                        if line.startswith(("def", "async def")):
                            functions += 1
                        if line.startswith("class"):
                            classes += 1
                        lines += 1

        return file_amount, functions, lines, classes

    def format_time(self, seconds: int, friendly: bool = False):

        minute, second = divmod(seconds, 60)
        hour, minute = divmod(minute, 60)
        day, hour = divmod(hour, 24)

        days, hours, minutes, seconds, = round(day), round(hour), round(minute), round(second)

        if friendly is True:
            formatted = f"{days}d {hours}h {minutes}m {seconds}s"
        else:
            formatted = f"{minutes:02d}:{seconds:02d}"
            if hours is not 0:
                formatted = f"{hours:02d}:{formatted}"
            if days is not 0:
                formatted = f"{days:02d}:{formatted}"

        return formatted

    def random_colour(self):
        return "#%02X%02X%02X" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def member_activity(self, member: discord.Member):

        if not member.activity or not member.activities:
            return "N/A"

        message = "\n"

        for activity in member.activities:

            if activity.type == discord.ActivityType.custom:
                message += f"• "
                if activity.emoji:
                    message += f"{activity.emoji} "
                if activity.name:
                    message += f"{activity.name}"
                message += "\n"

            elif activity.type == discord.ActivityType.playing:

                message += f"• Playing **{activity.name}** "
                if not isinstance(activity, discord.Game):
                    if activity.details:
                        message += f"**| {activity.details}** "
                    if activity.state:
                        message += f"**| {activity.state}** "
                    message += "\n"

            elif activity.type == discord.ActivityType.streaming:
                message += f"• Streaming **[{activity.name}]({activity.url})** on **{activity.platform}**\n"

            elif activity.type == discord.ActivityType.watching:
                message += f"• Watching **{activity.name}**\n"

            elif activity.type == discord.ActivityType.listening:

                if isinstance(activity, discord.Spotify):
                    url = f"https://open.spotify.com/track/{activity.track_id}"
                    message += f"• Listening to **[{activity.title}]({url})** by **{', '.join(activity.artists)}** "
                    if activity.album and not activity.album == activity.title:
                        message += f"from the album **{activity.album}** "
                    message += "\n"
                else:
                    message += f"• Listening to **{activity.name}**\n"

        return message

    def member_status(self, member: discord.Member):
        status = {
            discord.Status.online: "Online",
            discord.Status.idle: "Idle",
            discord.Status.dnd: "Do not disturb",
            discord.Status.offline: "Offline"
        }
        return status[member.status]

    def member_colour(self, member: discord.Member):
        colours = {
            discord.Status.online: 0x008000,
            discord.Status.idle: 0xFF8000,
            discord.Status.dnd: 0xFF0000,
            discord.Status.offline: 0x808080
        }
        return colours[member.status]

    def member_avatar(self, member: discord.Member):

        return str(member.avatar_url_as(format="gif" if member.is_avatar_animated() is True else "png"))

    def guild_icon(self, guild: discord.Guild):

        return str(guild.icon_url_as(format="gif" if guild.is_icon_animated() is True else "png"))

    def guild_region(self, guild: discord.Guild):
        regions = {
            discord.VoiceRegion.amsterdam: "Amsterdam",
            discord.VoiceRegion.brazil: "Brazil",
            discord.VoiceRegion.eu_central: "EU-Central",
            discord.VoiceRegion.eu_west: "EU-West",
            discord.VoiceRegion.europe: "Europe",
            discord.VoiceRegion.frankfurt: "Frankfurt",
            discord.VoiceRegion.hongkong: "Hong kong",
            discord.VoiceRegion.india: "India",
            discord.VoiceRegion.japan: "Japan",
            discord.VoiceRegion.london: "London",
            discord.VoiceRegion.russia: "Russia",
            discord.VoiceRegion.singapore: "Singapore",
            discord.VoiceRegion.southafrica: "South Africa",
            discord.VoiceRegion.sydney: "Sydney",
            discord.VoiceRegion.us_central: "US-Central",
            discord.VoiceRegion.us_east: "US-East",
            discord.VoiceRegion.us_south: "US-South",
            discord.VoiceRegion.us_west: "US-West"
        }
        return regions[guild.region]

    def guild_mfa_level(self, guild: discord.Guild):
        mfa_levels = {
            0: "Not required",
            1: "Required"
        }
        return mfa_levels[guild.mfa_level]

    def guild_verification_level(self, guild: discord.Guild):
        verification_levels = {
            discord.VerificationLevel.none: "None - No criteria set.",
            discord.VerificationLevel.low: "Low - Must have a verified email.",
            discord.VerificationLevel.medium: "Medium - Must have a verified email and be registered on discord for more than 5 minutes.",
            discord.VerificationLevel.high: "High - Must have a verified email, be registered on discord for more than 5 minutes and be a member of the guild for more then 10 minutes.",
            discord.VerificationLevel.extreme: "Extreme - Must have a verified email, be registered on discord for more than 5 minutes, be a member of the guild for more then 10 minutes and a have a verified phone number."
        }
        return verification_levels[guild.verification_level]

    def guild_content_filter_level(self, guild: discord.Guild):
        explicit_content_filters = {
            discord.ContentFilter.disabled: "None - Content filter disabled.",
            discord.ContentFilter.no_role: "No role - Content filter enabled only for users with no roles.",
            discord.ContentFilter.all_members: "All members - Content filter enabled for all users.",
        }
        return explicit_content_filters[guild.explicit_content_filter]

    def guild_user_status(self, guild: discord.Guild):
        online = sum(1 for member in guild.members if member.status == discord.Status.online)
        idle = sum(1 for member in guild.members if member.status == discord.Status.idle)
        dnd = sum(1 for member in guild.members if member.status == discord.Status.do_not_disturb)
        offline = sum(1 for member in guild.members if member.status == discord.Status.offline)
        return online, idle, dnd, offline
