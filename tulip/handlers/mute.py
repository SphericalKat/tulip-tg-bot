from telegram import ChatPermissions, Update
from telegram.constants import ChatMemberStatus
from telegram.error import BadRequest
from telegram.ext import ContextTypes

from tulip import LOGGER
from tulip.utils.chat_status import is_user_ban_protected
from tulip.utils.decorators import (
    bot_can_restrict,
    require_group_chat,
    user_can_restrict,
)
from tulip.utils.extraction import extract_time, extract_user, extract_user_and_text


@require_group_chat
@bot_can_restrict
@user_can_restrict
async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user  # TODO: use for log channels later
    msg = update.effective_message

    user_id, reason = await extract_user_and_text(msg, context.args)

    if not user_id:
        await msg.reply_text("You need to provide a user to mute.")
        return

    try:
        member = await chat.get_member(user_id)
    except BadRequest as e:
        if e.message == "User not found":
            await msg.reply_text("This user is not in the chat.")
            return
        else:
            raise e

    if await is_user_ban_protected(chat, user_id, member):
        await msg.reply_text("This user is an admin and cannot be muted.")
        return

    if user_id == context.bot.id:
        await msg.reply_text("I can't mute myself!")
        return

    message = f"{member.user.mention_html()} has been muted."
    if reason:
        message += f"\nReason:\n{reason}"

    try:
        await chat.restrict_member(
            user_id, permissions=ChatPermissions.no_permissions()
        )
        await msg.reply_text(message)
    except BadRequest as e:
        if e.message == "Reply message not found":
            await msg.reply_text(message, quote=False)
        else:
            LOGGER.warning(update)
            LOGGER.exception(
                "ERROR muting user %s in chat %s (%s) due to %s",
                user_id,
                chat.title,
                chat.id,
                e.message,
            )
            await message.reply_text(
                "I'm unable to mute this user due to ... unforeseen reasons. This should not have happened."
            )


@require_group_chat
@bot_can_restrict
@user_can_restrict
async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user

    user_id = await extract_user(msg, context.args)

    if not user_id:
        await msg.reply_text("You need to provide a user to unmute.")
        return

    try:
        member = await chat.get_member(user_id)
    except BadRequest as e:
        if e.message == "User not found":
            await msg.reply_text("I can't seem to find this user.")
            return
        else:
            raise e

    if user_id == context.bot.id:
        await msg.reply_text("I can't unmute myself!")
        return

    if member.status != ChatMemberStatus.RESTRICTED:
        await msg.reply_text("This user is not muted in the chat.")
        return

    await chat.restrict_member(user_id, permissions=ChatPermissions.all_permissions())
    await msg.reply_text(f"{member.user.mention_html()} has been unmuted.")


@require_group_chat
@bot_can_restrict
@user_can_restrict
async def tmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message

    user_id, reason = await extract_user_and_text(msg, context.args)

    if not user_id:
        await msg.reply_text("You need to provide a user to temporarily mute.")
        return

    try:
        member = await chat.get_member(user_id)
    except BadRequest as e:
        if e.message == "User not found":
            await msg.reply_text("I can't seem to find this user.")
            return
        else:
            raise e

    if await is_user_ban_protected(chat, user_id):
        await msg.reply_text("This user is an admin and cannot be temporarily muted.")
        return

    if user_id == context.bot.id:
        await msg.reply_text("I can't mute myself!")
        return

    if not reason:
        await msg.reply_text(
            "You need to provide a time to temporarily mute this user for."
        )
        return

    split_reason = reason.split(None, 1)

    time_val = split_reason[0].lower()
    if len(split_reason) > 1:
        reason = split_reason[1]
    else:
        reason = None

    ban_time = await extract_time(msg, time_val)
    if not ban_time:
        return

    try:
        await chat.restrict_member(
            user_id, until_date=ban_time, permissions=ChatPermissions.no_permissions()
        )
        reply_msg = (
            f"{member.user.mention_html()} has been temporarily muted for {time_val}."
        )
        if reason:
            reply_msg += f"\nReason:\n{reason}"
        await msg.reply_text(reply_msg)
    except BadRequest as e:
        if e.message == "Reply message not found":
            await msg.reply_text(reply_msg, quote=False)
        else:
            LOGGER.warning(update)
            LOGGER.exception(
                "ERROR muting user %s in chat %s (%s) due to %s",
                user_id,
                chat.title,
                chat.id,
                e.message,
            )
            await msg.reply_text(
                "I'm unable to temporarily mute this user due to ... unforeseen reasons. This should not have happened."
            )
