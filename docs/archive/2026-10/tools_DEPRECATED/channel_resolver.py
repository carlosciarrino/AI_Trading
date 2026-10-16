import subprocess, json, sys, logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

CHANNELS = {
    "simone_rizzo": "@simonerizzo",
    "aclas": "@aclasio",
    "riccardo_belli": "@riccardobellicontarini",
    "gabriele_aprile": "@GabrieleAprile",
    "guglielmo_vaccaro": "@guglielmo-vaccaro",
    "gianma_ai": "@Gianmaai.creator",
    "la_marketer": "@lamarketer.ai",
    "marco_builds": "@marcobuilds7",
    "dario_fontanel": "@dariofontanel",
    "teo_ai_finance": "@teo_aifinance",
    "somico85": "@somico85"
}

def resolve_channel_id(handle):
    """Usa yt-dlp per ottenere l'ID univoco del canale."""
    url = f"https://www.youtube.com/{handle}"
    try:
        result = subprocess.run(
            ["yt-dlp", "--print", "channel_id", "--playlist-items", "0", url],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            logger.error(f"Errore per {handle}: {result.stderr[:200]}")
            return None
    except Exception as e:
        logger.error(f"Eccezione per {handle}: {e}")
        return None

def main():
    resolved = {}
    for name, handle in CHANNELS.items():
        logger.info(f"Risoluzione {name} ({handle})...")
        channel_id = resolve_channel_id(handle)
        if channel_id:
            resolved[name] = {
                "handle": handle,
                "channel_id": channel_id,
                "rss_url": f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
            }
            logger.info(f"✅ {name}: {channel_id}")
        else:
            logger.warning(f"❌ {name}: impossibile risolvere")
    
    # Salva in config/youtube_channels.json
    import os
    os.makedirs("config", exist_ok=True)
    with open("config/youtube_channels.json", "w") as f:
        json.dump(resolved, f, indent=2)
    logger.info(f"✅ Salvati {len(resolved)} canali in config/youtube_channels.json")

if __name__ == "__main__":
    main()
