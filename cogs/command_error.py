import discord
from discord.ext import commands
from discord.ext.commands import errors

from .utils import custom_errors
from.utils.misc import Color
from .utils.i18n import use_current_gettext as _


class CommandError(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def send_error(ctx, error_message):
        embed = discord.Embed(
            title="<:error:797539791545565184> Erreur",
            url="https://discord.gg/Drbgufc",
            description=error_message,
            timestamp=ctx.message.created_at,
            color=Color.black().discord
        )
        embed.set_author(
            name=f'{ctx.author.name}#{ctx.author.discriminator}',
            icon_url=ctx.author.avatar_url
        )
        embed.set_footer(
            text=_("{ctx.bot.user.name}#{ctx.bot.user.discriminator} open-source project").format(**locals()),
            icon_url=ctx.bot.user.avatar_url
        )

        await ctx.send(embed=embed, delete_after=10)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await self.bot.set_actual_language(ctx.author)
        if isinstance(error, errors.CommandNotFound):
            return

        if isinstance(error, custom_errors.NotAuthorizedChannels):
            formatted_text = (_("You can't execute this command in <#{ctx.channel.id}>. Try in one of these channels :\n\n").format(**locals()) +
                              f"<#{'>, <#'.join(str(chan_id) for chan_id in error.list_channels_id)}>")
            return await self.send_error(ctx, formatted_text)
        if isinstance(error, custom_errors.NotAuthorizedRoles):
            formatted_text = (_("You can't execute this command, you need one of these roles :\n\n").format(**locals()) +
                              f"<@&{'>, <@&'.join(str(role_id) for role_id in error.list_roles_id)}>")
            return await self.send_error(ctx, formatted_text)
        if isinstance(error, commands.MissingRequiredArgument):
            formatted_text = (_("A required argument is missing in the command !\n") +
                              f"`{ctx.command.usage}`")
            return await self.send_error(ctx, formatted_text)
        if isinstance(error, errors.PrivateMessageOnly):
            return await self.send_error(ctx, _('This command must be executed in Private Messages'))
        if isinstance(error, errors.CheckFailure):
            return
        if isinstance(error, commands.CommandError):
            return await self.send_error(ctx, str(error))

        self.bot.logger.error(error)


def setup(bot):
    bot.add_cog(CommandError(bot))
    bot.logger.info("Extension [command_error] loaded successfully.")
