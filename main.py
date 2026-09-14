import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# ================== CẤU HÌNH ==================
# Token đọc từ Environment Variable trên Render (KHÔNG viết token vào đây!)
TOKEN = os.environ.get("TOKEN")
WELCOME_CHANNEL_ID = 1548691233143128064
WELCOME_IMAGE_URL = "https://i.pinimg.com/originals/a7/11/6f/a7116f6d34c68356e727635462c35db9.gif"
# ===============================================

# --- Server web giữ cho Render không tắt bot ---
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot dang chay! ✅"

def run_web():
    app.run(host="0.0.0.0", port=8080)

# ----------------- BOT -----------------
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # BẮT BUỘC để nhận sự kiện thành viên mới

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ Bot đã hoạt động: {bot.user}")
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="thành viên mới vào server 👀"
        )
    )
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="🤖 Bot Online!",
            description=f"**{bot.user.name}** đã hoạt động và sẵn sàng phục vụ!",
            color=discord.Color(0xFFFFFF)
        )
        embed.set_thumbnail(url=bot.user.display_avatar.url)
        embed.set_footer(text=f"Ping: {round(bot.latency * 1000)}ms")
        await channel.send(embed=embed)


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel is None:
        return

    embed = discord.Embed(
        title="🎉 CHÀO MỪNG THÀNH VIÊN MỚI!",
        description=(
            f"Chào **{member.mention}** đã đến với "
            f"**{member.guild.name}**! 🥳\n\n"
            f"📖 Đọc luật ở kênh <#{WELCOME_CHANNEL_ID}>\n"
            f"💬 Chat cùng mọi người nhé!"
        ),
        color=discord.Color(0xFFFFFF)
    )
    embed.set_image(url=WELCOME_IMAGE_URL)
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="👤 Tên", value=member.name, inline=True)
    embed.add_field(
        name="📊 Thành viên thứ",
        value=f"{member.guild.member_count}",
        inline=True
    )
    embed.set_footer(text=f"ID: {member.id} • Vào lúc {member.joined_at}")

    await channel.send(content=f"👋 {member.mention}", embed=embed)

    # Gửi sticker (nếu server có)
    try:
        stickers = member.guild.stickers
        if len(stickers) > 0:
            await channel.send(sticker=stickers[0])
    except Exception as e:
        print(f"⚠️ Lỗi gửi sticker: {e}")


if __name__ == "__main__":
    # Chạy web server ở luồng riêng (chống Render tắt service)
    Thread(target=run_web, daemon=True).start()
    bot.run(TOKEN)
