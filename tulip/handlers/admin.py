from telegram import Update
from telegram.constants import ChatMemberStatus, ChatType
from telegram.error import BadRequest
from telegram.ext import ContextTypes

from tulip.utils.decorators import (
    bot_can_pin,
    bot_can_promote,
    require_group_chat,
    user_can_pin,
    user_can_promote,
)
from tulip.utils.extraction import extract_user, extract_user_and_text


@bot_can_promote
@user_can_promote
@require_group_chat
async def promote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message

    user_id, title = await extract_user_and_text(msg, context.args)
    if not user_id:
        await msg.reply_text("You need to provide a user to promote.")
        return

    user_member = await chat.get_member(user_id)
    if user_member.status == ChatMemberStatus.LEFT:
        await msg.reply_text("This user is not in the chat.")
        return

    if user_member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        await msg.reply_text("This user is already an admin.")
        return

    if user_id == context.bot.id:
        await msg.reply_text("I can't promote myself!")
        return

    bot_member = await chat.get_member(context.bot.id)

    # Promote the user with the same permissions as the bot
    await chat.promote_member(
        user_id=user_id,
        can_change_info=bot_member.can_change_info,
        can_post_messages=bot_member.can_post_messages,
        can_edit_messages=bot_member.can_edit_messages,
        can_delete_messages=bot_member.can_delete_messages,
        can_invite_users=bot_member.can_invite_users,
        can_restrict_members=bot_member.can_restrict_members,
        can_pin_messages=bot_member.can_pin_messages,
        can_promote_members=bot_member.can_promote_members,
        is_anonymous=False,  # anonymous admins cause problems for the bot
        can_manage_chat=bot_member.can_manage_chat,
        can_manage_video_chats=bot_member.can_manage_video_chats,
        can_manage_topics=bot_member.can_manage_topics,
        can_post_stories=bot_member.can_post_stories,
        can_edit_stories=bot_member.can_edit_stories,
        can_delete_stories=bot_member.can_delete_stories,
    )

    # Set the custom title if provided
    if title:
        await context.bot.set_chat_administrator_custom_title(chat.id, user_id, title)
        await msg.reply_text(
            f"{user_member.user.mention_html()} is now an admin with the custom title <code>{title}</code>."
        )
    else:
        await msg.reply_text(f"{user_member.user.mention_html()} is now an admin.")


async def demote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message

    user_id = await extract_user(msg, context.args)
    if not user_id:
        await msg.reply_text("You need to provide a user to demote.")
        return

    user_member = await chat.get_member(user_id)

    if user_member.status == ChatMemberStatus.LEFT:
        await msg.reply_text("This user is not in the chat.")
        return

    if user_member.status != ChatMemberStatus.ADMINISTRATOR:
        await msg.reply_text("This user is not an admin.")
        return

    if user_id == context.bot.id:
        await msg.reply_text("I can't demote myself!")
        return

    # Demote the user by setting all permissions to False
    try:
        await chat.promote_member(
            user_id=user_id,
            can_change_info=False,
            can_post_messages=False,
            can_edit_messages=False,
            can_delete_messages=False,
            can_invite_users=False,
            can_restrict_members=False,
            can_pin_messages=False,
            can_promote_members=False,
            is_anonymous=False,
            can_manage_chat=False,
            can_manage_video_chats=False,
            can_manage_topics=False,
            can_post_stories=False,
            can_edit_stories=False,
            can_delete_stories=False,
        )
        await msg.reply_text(
            f"{user_member.user.mention_html()} is no longer an admin."
        )
    except BadRequest:
        await msg.reply_text(
            f"Could not demote {user_member.user.mention_html()}. The admin status "
            "might be appointed by another user, so I can't demote them."
        )


@bot_can_pin
@user_can_pin
async def pin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message

    if update.effective_chat.type not in [
        ChatType.PRIVATE,
        ChatType.GROUP,
        ChatType.SUPERGROUP,
    ]:
        # ignore channels
        return

    if not msg.reply_to_message:
        await msg.reply_text("Reply to a message to pin it.")
        return

    silent = True
    if len(context.args) and context.args[0].lower() == "loud":
        silent = False

    try:
        await msg.reply_to_message.pin(disable_notification=silent)
    except BadRequest as e:
        if e.message == "Chat_not_modified":
            pass
        else:
            raise e


@bot_can_pin
@user_can_pin
async def unpin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message

    try:
        await msg.chat.unpin_message()
    except BadRequest as e:
        if e.message == "Chat_not_modified":
            pass
        else:
            raise e
