import discord
from discord.ext import commands
import random, json, os

TOKEN = "OVDE_STAVI_TOKEN"  

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

scores_file = "scores.json"
used_words_file = "used_words.json"

last_word = None
last_player = None
game_active = False
used_words = []


def load_json_file(filename, default):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return default

def save_json_file(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

scores = load_json_file(scores_file, {})
used_words = load_json_file(used_words_file, [])

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
    """Pokreće igru nasumičnom rečju"""
    global last_word, last_player, game_active, used_words

    if game_active:
        await ctx.send("⚠️ Igra već traje! Ako hoćeš novu, kucaj `!reset`.")
        return

    
    last_word = random.choice(starter_words)
    last_player = None
    game_active = True
    used_words = [last_word]
    save_json_file(used_words_file, used_words)

    await ctx.send(
        f"🎮 **Nova igra Kaladont počinje!**\n"
        f"➡ Pravilo: *Moraš nastaviti niz rečju koja počinje na **zadnja dva slova** prošle reči.*\n"
        f"➡ Ne možeš igrati dva puta za redom.\n"
        f"➡ Ne smeš ponavljati već korišćene reči.\n"
        f"➡ Ako se reč završi na nemogući nastavak ({', '.join(dead_end_pairs)}), igrač **pobeđuje**.\n\n"
        f"▶️ **Prva reč je:** **{last_word}**\n"
        f"Sledeća mora početi na **{last_word[-2:]}**"
    )

@bot.command()
async def reset(ctx):
    """Resetuje igru"""
    _end_game()
    await ctx.send("🔄 Igra je resetovana! Kucaj `!start` za novu.")

@bot.command()
async def score(ctx):
    """Prikazuje scoreboard"""
    if not scores:
        await ctx.send("📊 Još nema poena.")
        return

    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    scoreboard_text = "\n".join([f"🏅 **{user}** – {points} poena" for user, points in sorted_scores])
    await ctx.send(f"📊 **Trenutni scoreboard:**\n{scoreboard_text}")

@bot.event
async def on_message(message):
    """Prati sve poruke bilo gde"""
    global last_word, last_player, game_active, used_words

    if message.author.bot:
        return  

    await bot.process_commands(message)  

    if not game_active:
        return

    user = message.author.name
    word = message.content.strip().lower()

    if last_player == user:
        await message.add_reaction("❌")
        await message.channel.send(f"❌ **{user}**, ne možeš igrati sam/sama na svoju reč! Sačekaj drugog.")
        return


    if word in used_words:
        await message.add_reaction("🚫")
        await message.channel.send(f"🚫 **{user}**, reč **{word}** je već korišćena! Probaj drugu.")
        return

    if not word.startswith(last_word[-2:]):
        await message.add_reaction("❌")
        await message.channel.send(
            f"❌ **{user}**, moraš početi na **{last_word[-2:]}**, a ti si rekao/la **{word}**."
        )
        return


    if word == "kaladont":
        _add_score(user, win=True)
        await message.add_reaction("🏆")
        await message.channel.send(
            f"🎉 **{user}** je rekao/la **KALADONT** i pobedio/la!\n🏆 Dobija **2 poena**!\n📊 Pogledaj rezultate sa `!score`."
        )
        _end_game()
        return

    for dead_end in dead_end_pairs:
        if word.endswith(dead_end):
            _add_score(user, win=True)
            await message.add_reaction("🏆")
            await message.channel.send(
                f"🏆 **{user}** je rekao/la **{word}**, koje se završava na **{dead_end}** i nema nastavak!\n✅ **{user} POBEĐUJE i dobija 2 poena!**\n📊 Pogledaj rezultate sa `!score`."
            )
            _end_game()
            return

    _add_score(user, win=False)
    used_words.append(word)
    save_json_file(used_words_file, used_words)
    last_word = word
    last_player = user

    # dodaj reakciju ✅ jer je validna
    await message.add_reaction("✅")

    # nastavlja igru
    await message.channel.send(
        f"✅ **{user}** je uneo/la validnu reč **{word}**!\n"
        f"Sledeća mora početi na **{last_word[-2:]}**"
    )

# --- helper funkcije ---
def _add_score(user, win=False):
    """Dodaje poene igraču (2 za pobedu, 1 za običan potez)"""
    global scores
    if user not in scores:
        scores[user] = 0
    if win:
        scores[user] += 2  
    else:
        scores[user] += 1  
    save_json_file(scores_file, scores)

def _end_game():
    """Resetuje stanje igre"""
    global last_word, last_player, game_active, used_words
    last_word = None
    last_player = None
    game_active = False
    used_words = []
    save_json_file(used_words_file, used_words)

bot.run(TOKEN)
