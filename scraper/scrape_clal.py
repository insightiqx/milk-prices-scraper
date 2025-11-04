"""
CLAL (section=demi) – Captura de red (JSON) + evidencia
- Intercepta TODAS las respuestas y guarda:
  * JSON (application/json) o URLs que contengan 'json'
  * CSV (text/csv)
- Hace screenshot y guarda HTML
- Esto nos dice EXACTAMENTE de dónde vienen los datos del gráfico
"""

import asyncio, os, re, uuid
from pathlib import Path
from playwright.async_api import async_playwright

URL = "https://www.clal.it/en/index.php?section=demi"

SAVE_DIR = Path("data/raw/net")
SAVE_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

def should_save_response(resp):
    url = resp.url.lower()
    ctype = (resp.headers.get("content-type") or "").lower()
    # guarda JSON/CSV o cosas que parezcan series
    if "application/json" in ctype or "text/csv" in ctype:
        return True
    if any(k in url for k in ["json", "series", "data", "chart", "ajax", "get", "api"]):
        return True
    return False

async def run():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        ctx = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36",
            locale="en-US",
            timezone_id="Europe/Paris",
            viewport={"width": 1440, "height": 900}
        )

        # hook para guardar respuestas útiles
        async def on_response(resp):
            try:
                if not should_save_response(resp):
                    return
                url = resp.url
                ctype = (resp.headers.get("content-type") or "").split(";")[0]
                ext = ".json" if "json" in (ctype or "").lower() or "json" in url.lower() else (".csv" if "csv" in (ctype or "").lower() else ".bin")
                safe = re.sub(r"[^a-z0-9]+", "_", url.lower())
                fname = SAVE_DIR / f"{safe[:140]}_{uuid.uuid4().hex[:6]}{ext}"
                body = await resp.body()
                fname.write_bytes(body)
                print(f"💾 Guardado: {fname.name}")
            except Exception:
                pass

        ctx.on("response", on_response)
        page = await ctx.new_page()

        # Ir a la página
        await page.goto(URL, wait_until="networkidle")

        # Aceptar cookies si aparecen
        for sel in [
            "#onetrust-accept-btn-handler",
            "button:has-text('Accept')",
            "button:has-text('I agree')",
            "text=Accept"
        ]:
            try:
                await page.click(sel, timeout=1000)
                break
            except Exception:
                pass

        # Desplazar un poco para disparar cargas perezosas
        for _ in range(4):
            await page.mouse.wheel(0, 900)
            await page.wait_for_timeout(600)

        # Guarda evidencia visual/HTML
        (RAW_DIR / "demi.html").write_text(await page.content(), encoding="utf-8")
        await page.screenshot(path=str(RAW_DIR / "demi.png"), full_page=True)

        # Espera un poco extra para que cierren todas las peticiones tardías
        await page.wait_for_timeout(2000)

        await browser.close()
        print(f"✅ He terminado. Revisa los archivos en {SAVE_DIR}")

if __name__ == "__main__":
    asyncio.run(run())