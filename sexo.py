import re, os, asyncio, discord, shutil
from discord.ext import commands
from termcolor import colored

from config import token as cfgtoken
from config import chatid as cfgchat
from config import prefix as cfgprefix

# --- Limpeza automática do cache ---
if os.path.exists("__pycache__"):
    shutil.rmtree("__pycache__")
    print("🧹 __pycache__ removido")

# Configurações
prefixo = cfgprefix
token = cfgtoken
chat = cfgchat

pokeone = 473020399060385792
paused = False

client = commands.Bot(command_prefix=prefixo, help_command=None)

# --- Delay configurável por ação ---
ACTION_DELAYS = {
    "master": 2,  # delay para .master
    "1": 1,  # delay para enviar 1
    "quick": 1,  # delay para enviar quick
    "s": 5,  # delay para .s
}

# --- Listas de Pokémon ---
TARGET_POKEMON_CAPTURE = [
    "Pikachu",
    "Charmander",
    "Bulbasaur",
    "Ponyta",
    "Dodrio",
    "Sneasel",
]  # ajuste conforme necessário
TARGET_POKEMON_KILL = [
    "Zubat",
    "Rattata",
    "Pidgey",
    "Donphan",
    "Poliwhirl",
    "Poliwrath",
    "Politoed",
    "Magikarp",
    "Ursaring",
    "Poliwag",
    "Feebas",
    "Rapidash",
    "Heracross",
    "Tangela",
    "Aipom",
]


# --- Função segura para enviar mensagens ---
async def safe_send(channel, content, delay=0, retries=3):
    for attempt in range(retries):
        try:
            if delay > 0:
                await asyncio.sleep(delay)
            await channel.send(content)
            return
        except Exception as e:
            wait_time = (attempt + 1) * 3
            print(
                f"⚠ Tentativa de envio falhou '{content}' (tentativa {attempt + 1}/{retries}): {e}"
            )
            await asyncio.sleep(wait_time)
    print(f"❌ Falhou em enviar '{content}' após {retries} tentativas.")


# --- Evento de inicialização ---
@client.event
async def on_ready():
    print(colored(f"✅ Auto Spawn em execução em - {client.user.name}", "blue"))
    print(
        colored(f'iniciando autospawn com prefix: "{prefixo}"...', "black", "on_white")
    )


# --- Evento de mensagens ---
@client.event
async def on_message(message):
    global paused
    if paused or not message.channel or message.channel.id != int(chat):
        return

    if message.author.id != pokeone:
        if not message.author.bot:
            await client.process_commands(message)
        return

    # --- Mensagens com embeds ---
    if message.embeds:
        embed = message.embeds[0]

        description = embed.description or ""
        title = embed.title or ""
        footer_text = embed.footer.text if embed.footer else ""

        # Extrair nome do Pokémon da mensagem
        pokemon_match = re.search(r"\*\*(.+?)\*\*", description) or re.search(
            r"\*\*(.+?)\*\*", title
        )
        pokemon_name = pokemon_match.group(1) if pokemon_match else ""

        # --- Vitória de batalha ---
        if "You have won the Wild Battle!" in description:
            await safe_send(message.channel, f"{prefixo}s", ACTION_DELAYS["s"])

        # --- Captura de Shiny / Shiny Wild Pokémon ---
        elif "shiny" in description.lower() or "shiny" in title.lower():
            await safe_send(
                message.channel, f"{prefixo}master", ACTION_DELAYS["master"]
            )

        # --- Captura de Quick Ball ---
        elif pokemon_name in TARGET_POKEMON_CAPTURE:
            await safe_send(message.channel, f"{prefixo}quick", ACTION_DELAYS["quick"])

        # --- Captura normal (adicionado ao time ou enviado para Box) ---
        elif (
            "added to your team" in description
            or "Pokémon was sent to Box" in description
        ):
            await safe_send(message.channel, "1", ACTION_DELAYS["1"])

        # Já em batalha
        if "You're already in a battle." in description:
            await safe_send(message.channel, "1", ACTION_DELAYS["1"])

        # Footer Send 1
        if "Send 1" in footer_text:
            await safe_send(message.channel, "1", ACTION_DELAYS["1"])

    # Mensagens normais fora de embed
    elif "Keep the calm!" in message.content:
        # Reage apenas conforme evento
        pass

    # Processa comandos normalmente
    if not message.author.bot:
        await client.process_commands(message)


# --- Comandos para pausar/iniciar ---
@client.command(name="start")
async def start_cmd(ctx):
    global paused
    if ctx.channel.id == int(chat):
        if paused:
            paused = False
            await safe_send(ctx, "▶ Bot Iniciado")
        else:
            await safe_send(ctx, "⚠ Bot já está em execução.")


@client.command(name="stop")
async def stop_cmd(ctx):
    global paused
    if ctx.channel.id == int(chat):
        if not paused:
            paused = True
            await safe_send(ctx, "⏸ Bot pausado.")
        else:
            await safe_send(ctx, "⚠ Bot já está pausado.")


# --- Rodar bot ---
try:
    print(f"Versão discord.py: {discord.__version__}")
except:
    pass

client.run(token)
