import discord
from discord.ext import commands
import random
import os

TOKEN = os.getenv("TOKEN")  

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

last_word = None
last_player = None
game_active = False
scores = {}

starter_words = [
    "auto", "torba", "kafa", "more", "kapa", "telefon",
    "kuca", "igra", "banana", "leto", "riba", "prsten",
    "slika", "sto", "vino", "polje"
]

dead_end_pairs = [
    "nj", "lj", "dž", "q", "w", "x", "y", "z",
    "rd", "nt", "ač", "ic", "lje", "nje", "anj", "rt",
    "rk", "mb", "zd", "št", "žd", "dl", "mp", "tv", "pt"
]

@bot.event
async def on_ready():
    print(f"✅ Bot je online kao {bot.user}")

@bot.command()
async def start(ctx):
    global last_word, game_active, last_player
    if game_active:
        await ctx.send("⚠️ Igra već traje! Ako hoćeš novu, kucaj `!reset`.")
        return

    last_word = random.choice(starter_words)
    last_player = None
    game_active = True
    await ctx.send(
        f"🎮 **Nova igra Kaladont počinje!**\n"
        f"➡ Pravilo: *Moraš nastaviti niz rečju koja počinje na **zadnja dva slova** prošle reči.*\n"
        f"➡ Ne možeš igrati sam/sama na svoju reč.\n"
        f"➡ Ako se reč završi na nemogući nastavak ({', '.join(dead_end_pairs)}), igrač **pobeđuje**.\n\n"
        f"Prva reč je **{last_word}**.\n"
        f"Sledeća mora početi na **{last_word[-2:]}**"
    )

@bot.command()
async def kaladont(ctx, *, word: str):
    global last_word, last_player, game_active, scores

    if not game_active:
        await ctx.send("⚠️ Igra nije pokrenuta. Kucaj `!start` da počnemo!")
        return

    word = word.lower()
    user = ctx.author.name

    if last_player == user:
        await ctx.send(f"❌ **{user}**, ne možeš igrati sam/sama na svoju reč! Sačekaj drugog igrača.")
        return

    if word.startswith(last_word[-2:]):
        if word == "kaladont":
            _add_score(user)
            await ctx.send(
                f"🎉 **{ctx.author.name}** je rekao/la **KALADONT** i pobedio/la!\n"
                f"📊 Pogledaj rezultate sa `!score`."
            )
            _end_game()
            return

        for dead_end in dead_end_pairs:
            if word.endswith(dead_end):
                _add_score(user)
                await ctx.send(
                    f"🏆 **{ctx.author.name}** je rekao/la **{word}**, koje se završava na **{dead_end}** i nema nastavak!\n"
                    f"✅ **{ctx.author.name} POBEĐUJE!**\n"
                    f"📊 Pogledaj rezultate sa `!score`."
                )
                _end_game()
                return

        _add_score(user)
        last_word = word
        last_player = user
        await ctx.send(
            f"✅ **{ctx.author.name}** je uneo/la validnu reč **{word}**!\n"
            f"Sledeća mora početi na **{last_word[-2:]}**"
        )
    else:
        await ctx.send(
            f"❌ **{ctx.author.name}**, moraš početi na **{last_word[-2:]}**, "
            f"a ti si rekao/la **{word}**.\n➡ Pravilo: *Moraš nastaviti niz rečju koja počinje na zadnja dva slova prošle reči.*"
        )

@bot.command()
async def reset(ctx):
    _end_game()
    await ctx.send("🔄 Igra je resetovana! Kucaj `!start` za novu.")

@bot.command()
async def score(ctx):
    if not scores:
        await ctx.send("📊 Nema još poena. Igraj prvo pa vidi ko vodi!")
        return

    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    scoreboard_text = "\n".join([f"🏅 **{user}** – {points} poena" for user, points in sorted_scores])
    await ctx.send(f"📊 **Trenutni scoreboard:**\n{scoreboard_text}")

def _add_score(user):
    global scores
    if user not in scores:
        scores[user] = 0
    scores[user] += 1

def _end_game():
    global last_word, last_player, game_active
    last_word = None
    last_player = None
    game_active = False

bot.run(TOKEN)import discord
from discord.ext import commands
import random
import os

TOKEN = os.getenv("TOKEN")  

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

last_word = None
last_player = None
game_active = False
scores = {}

starter_words = [
    "auto", "torba", "kafa", "more", "kapa", "telefon",
    "kuca", "igra", "banana", "leto", "riba", "prsten",
    "slika", "sto", "vino", "polje"
]

dead_end_pairs = [
    "nj", "lj", "dž", "q", "w", "x", "y", "z",
    "rd", "nt", "ač", "ic", "lje", "nje", "anj", "rt",
    "rk", "mb", "zd", "št", "žd", "dl", "mp", "tv", "pt"
]

@bot.event
async def on_ready():
    print(f"✅ Bot je online kao {bot.user}")

@bot.command()
async def start(ctx):
    global last_word, game_active, last_player
    if game_active:
        await ctx.send("⚠️ Igra već traje! Ako hoćeš novu, kucaj `!reset`.")
        return

    last_word = random.choice(starter_words)
    last_player = None
    game_active = True
    await ctx.send(
        f"🎮 **Nova igra Kaladont počinje!**\n"
        f"➡ Pravilo: *Moraš nastaviti niz rečju koja počinje na **zadnja dva slova** prošle reči.*\n"
        f"➡ Ne možeš igrati sam/sama na svoju reč.\n"
        f"➡ Ako se reč završi na nemogući nastavak ({', '.join(dead_end_pairs)}), igrač **pobeđuje**.\n\n"
        f"Prva reč je **{last_word}**.\n"
        f"Sledeća mora početi na **{last_word[-2:]}**"
    )

@bot.command()
async def kaladont(ctx, *, word: str):
    global last_word, last_player, game_active, scores

    if not game_active:
        await ctx.send("⚠️ Igra nije pokrenuta. Kucaj `!start` da počnemo!")
        return

    word = word.lower()
    user = ctx.author.name

    if last_player == user:
        await ctx.send(f"❌ **{user}**, ne možeš igrati sam/sama na svoju reč! Sačekaj drugog igrača.")
        return

    if word.startswith(last_word[-2:]):
        if word == "kaladont":
            _add_score(user)
            await ctx.send(
                f"🎉 **{ctx.author.name}** je rekao/la **KALADONT** i pobedio/la!\n"
                f"📊 Pogledaj rezultate sa `!score`."
            )
            _end_game()
            return

        for dead_end in dead_end_pairs:
            if word.endswith(dead_end):
                _add_score(user)
                await ctx.send(
                    f"🏆 **{ctx.author.name}** je rekao/la **{word}**, koje se završava na **{dead_end}** i nema nastavak!\n"
                    f"✅ **{ctx.author.name} POBEĐUJE!**\n"
                    f"📊 Pogledaj rezultate sa `!score`."
                )
                _end_game()
                return

        _add_score(user)
        last_word = word
        last_player = user
        await ctx.send(
            f"✅ **{ctx.author.name}** je uneo/la validnu reč **{word}**!\n"
            f"Sledeća mora početi na **{last_word[-2:]}**"
        )
    else:
        await ctx.send(
            f"❌ **{ctx.author.name}**, moraš početi na **{last_word[-2:]}**, "
            f"a ti si rekao/la **{word}**.\n➡ Pravilo: *Moraš nastaviti niz rečju koja počinje na zadnja dva slova prošle reči.*"
        )

@bot.command()
async def reset(ctx):
    _end_game()
    await ctx.send("🔄 Igra je resetovana! Kucaj `!start` za novu.")

@bot.command()
async def score(ctx):
    if not scores:
        await ctx.send("📊 Nema još poena. Igraj prvo pa vidi ko vodi!")
        return

    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    scoreboard_text = "\n".join([f"🏅 **{user}** – {points} poena" for user, points in sorted_scores])
    await ctx.send(f"📊 **Trenutni scoreboard:**\n{scoreboard_text}")

def _add_score(user):
    global scores
    if user not in scores:
        scores[user] = 0
    scores[user] += 1

def _end_game():
    global last_word, last_player, game_active
    last_word = None
    last_player = None
    game_active = False

bot.run(TOKEN)
