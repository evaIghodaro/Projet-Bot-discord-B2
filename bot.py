import os
import discord
import random
from discord.ext import commands
from dotenv import load_dotenv

from history.save_manager import SaveManager
from history.history_manager import HistoryManager
from tree.tree_manager import TreeManager
from features.feature1 import PointsManager
from features.feature2 import UnlockManager
from features.feature3 import RandomRecipe

# TOKEN
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN environment variable is not set.")

# INTENTS
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# BOT
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)
bot.remove_command("help")

# MANAGERS
save_manager = SaveManager("data/save.json")
history_managers = {}
tree_manager = TreeManager()
points_manager = PointsManager(save_manager)
unlock_manager = UnlockManager(save_manager)
random_recipe = RandomRecipe(save_manager)

# READY EVENT
@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")

# HELP
@bot.command()
async def help(ctx):
    text = (
        "📌 Commandes :\n"
        "!help → Aide\n"
        "!start → Lance la discussion\n"
        "!reset → Reset la discussion\n"
        "!history → Historique\n"
        "!clearhistory → Efface l’historique\n"
        "!recette → Recette aléatoire\n"
        "!viplist → Liste VIP\n"
        "!unlock <num> → Débloquer VIP\n"
        "!speak about <mot> → Vérifie si existe"
    )
    await ctx.send(text)

# START
@bot.command()
async def start(ctx):
    user_id = str(ctx.author.id)
    tree_manager.reset(user_id)
    text = tree_manager.get_current_text(user_id)

    history_managers.setdefault(user_id, HistoryManager(save_manager)).add("!start")
    await ctx.send(text)

# RESET
@bot.command()
async def reset(ctx):
    user_id = str(ctx.author.id)
    tree_manager.reset(user_id)
    history_managers.setdefault(user_id, HistoryManager(save_manager)).add("!reset")
    await ctx.send("🔄 Discussion réinitialisée.")

# HISTORY
@bot.command()
async def history(ctx):
    user_id = str(ctx.author.id)
    hm = history_managers.setdefault(user_id, HistoryManager(save_manager))
    cmds = hm.get_all()

    if not cmds:
        await ctx.send("Aucune commande enregistrée.")
    else:
        await ctx.send("Historique :\n" + "\n".join(cmds))

# CLEAR HISTORY
@bot.command()
async def clearhistory(ctx):
    user_id = str(ctx.author.id)
    history_managers.setdefault(user_id, HistoryManager(save_manager)).clear()
    await ctx.send("✅ Historique effacé.")

# RECETTE ALEATOIRE
@bot.command()
async def recette(ctx):
    user_id = str(ctx.author.id)
    msg = random_recipe.get_random(user_id)
    await ctx.send(msg)

# LISTE VIP
@bot.command()
async def viplist(ctx):
    user_id = str(ctx.author.id)
    vip = unlock_manager.get_vip_list()
    points = points_manager.get_points(user_id)

    text = "\n".join(f"{i+1}. {v['name']} (coût: {v['cost']} pts)" for i, v in enumerate(vip))
    await ctx.send(f"🍰 Recettes VIP :\n{text}\n\n💰 Points : {points}")

# UNLOCK VIP
@bot.command()
async def unlock(ctx, num: int):
    user_id = str(ctx.author.id)
    msg = unlock_manager.unlock_by_number(user_id, num)
    await ctx.send(msg)

# SPEAK ABOUT
@bot.command()
async def speak(ctx, *, term: str):
    words = term.split()
    if words and words[0].lower() == "about":
        words = words[1:]

    term = " ".join(words).strip()
    exists = tree_manager.speak_about(term)
    await ctx.send("✅ Oui" if exists else "❌ Non")

# SYSTEME DE DISCUSSION PAR MENTION
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    ctx = await bot.get_context(message)
    if ctx.valid:
        await bot.process_commands(message)
        return

    if bot.user not in message.mentions:
        return

    user_id = str(message.author.id)

    content = (
        message.content
        .replace(f"<@!{bot.user.id}>", "")
        .replace(f"<@{bot.user.id}>", "")
        .strip()
    )

    if not content:
        await message.channel.send("ℹ️ Mentionnez-moi suivi de votre réponse.")
        return

    hm = history_managers.setdefault(user_id, HistoryManager(save_manager))
    hm.add(content)

    node = tree_manager.answer(user_id, content)

    if not node:
        await message.channel.send("❌ Je ne comprends pas.")
        return

    if node.is_leaf():
        dessert = random.choice(node.desserts)
        await message.channel.send(
            f"{dessert['name']}\nRecette: {dessert['recipe']}\nPoints: {dessert['points']}"
        )
        points_manager.award_from_node(user_id, dessert)
    else:
        await message.channel.send(node.display_text())

# RUN
bot.run(TOKEN)
