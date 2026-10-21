"""P1.7 (côté modèle) · Une génération abandonnée par le client doit s'arrêter dans vLLM.

Pour chaque mode (réponse en flux, réponse d'un bloc) : on lance 8 générations longues (2 000 tokens
demandés), on coupe la connexion au bout de 1 s, puis on lit /metrics de vLLM : le nombre de requêtes
en cours doit retomber à 0 en moins de 2 s. Sinon, des générations orphelines occupent la carte pour rien.
Témoin : les mêmes requêtes non coupées sont bien en cours au moment de la coupure.

Usage : python outils/annulation_vllm.py [--url http://127.0.0.1:8000]
"""
import argparse
import asyncio
import re
import time

import httpx

MODELE = "mistralai/Mistral-Small-3.2-24B-Instruct-2506"
DEMANDE = {"model": MODELE, "max_tokens": 2000, "temperature": 0.7, "ignore_eos": True,
           "messages": [{"role": "user", "content": "Écris un très long rapport détaillé sur l'histoire des banques en Europe."}]}


async def en_cours(client: httpx.AsyncClient, url: str) -> float:
    texte = (await client.get(f"{url}/metrics")).text
    m = re.search(r"^vllm:num_requests_running\{[^}]*\} ([0-9.e+]+)", texte, re.M)
    return float(m.group(1)) if m else -1.0


async def generation(url: str, flux: bool) -> None:
    async with httpx.AsyncClient(timeout=None) as c:
        if flux:
            async with c.stream("POST", f"{url}/v1/chat/completions", json={**DEMANDE, "stream": True}) as r:
                async for _ in r.aiter_bytes():
                    pass
        else:
            await c.post(f"{url}/v1/chat/completions", json=DEMANDE)


async def essai(url: str, flux: bool) -> dict:
    async with httpx.AsyncClient(timeout=10) as c:
        taches = [asyncio.create_task(generation(url, flux)) for _ in range(8)]
        await asyncio.sleep(1.0)
        avant = await en_cours(c, url)
        for t in taches:
            t.cancel()  # coupe la connexion HTTP, comme un client qui abandonne
        await asyncio.gather(*taches, return_exceptions=True)
        coupe = time.monotonic()
        while True:
            n = await en_cours(c, url)
            if n == 0 or time.monotonic() - coupe > 10:
                break
            await asyncio.sleep(0.05)
        return {"mode": "flux" if flux else "bloc", "en_cours_avant": avant, "en_cours_apres": n,
                "delai_s": round(time.monotonic() - coupe, 2)}


async def principal(url: str) -> None:
    ok = True
    for flux in (True, False):
        r = await essai(url, flux)
        reussi = r["en_cours_avant"] >= 8 and r["en_cours_apres"] == 0 and r["delai_s"] < 2
        ok &= reussi
        print(f"{r['mode']} : {r['en_cours_avant']:.0f} générations en cours à la coupure, "
              f"{r['en_cours_apres']:.0f} après {r['delai_s']} s → {'arrêtées' if reussi else 'ORPHELINES'}")
        await asyncio.sleep(2)
    print("RÉSULTAT :", "réussi" if ok else "ÉCHEC")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--url", default="http://127.0.0.1:8000")
    asyncio.run(principal(p.parse_args().url))
