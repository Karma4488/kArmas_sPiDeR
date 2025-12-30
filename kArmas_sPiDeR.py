#!/usr/bin/env python3
# kArmas_sPiDeR — Intelligent Spider
# Made in l0v3
# Author: Karmasec

import asyncio, aiohttp, aiosqlite
import hashlib, random, time, sys, shutil, os, re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import tldextract
import urllib.robotparser as robotparser
from math import log2

# ================== CONFIG ==================

USER_AGENT = "kArmas_sPiDeR/1.0 (ethical-research)"
MAX_DEPTH = 4
MAX_CONCURRENCY = 10
CRAWL_DELAY = (0.7, 2.0)
DB_FILE = "kArmas_sPiDeR.db"

KEYWORDS = ["admin","login","dashboard","api","auth","token","secret","config"]

GREEN = "\033[1;32m"
DARK  = "\033[0;32m"
GLOW  = "\033[92m"
RESET = "\033[0m"
BOLD  = "\033[1m"

# ================== FX BANNER ==================

def karma_banner():
    os.system("clear")
    chars = "01アイウエオカキクケコサシスセソ"
    for _ in range(20):
        print(DARK + "".join(random.choice(chars) for _ in range(70)) + RESET)
        time.sleep(0.03)
    os.system("clear")

    banner = f"""{GREEN}{BOLD}
 ███▄ ▄███▓ ▄▄▄     ▄▄▄       ██▀███   ███▄ ▄███▓ ▄▄▄
▓██▒▀█▀ ██▒▒████▄  ▒████▄    ▓██ ▒ ██▒▓██▒▀█▀ ██▒▒████▄
▓██    ▓██░▒██  ▀█▄▒██  ▀█▄  ▓██ ░▄█ ▒▓██    ▓██░▒██  ▀█▄
▒██    ▒██ ░██▄▄▄▄██░██▄▄▄▄██ ▒██▀▀█▄  ▒██    ▒██ ░██▄▄▄▄██

        k A r m a s _ s P i D e R
   We are Anonymous. We are Legion.
   Knowledge is Power.
{RESET}"""
    for line in banner.splitlines():
        print(GLOW + line + RESET)
        time.sleep(0.04)

# ================== FX: MATRIX RAIN ==================

async def matrix_rain(stop):
    chars = "01アイウエオカキクケコサシスセソ"
    width = shutil.get_terminal_size((80, 20)).columns
    while not stop.is_set():
        flicker = random.choice([GREEN, DARK, GLOW])
        sys.stdout.write(flicker + "".join(random.choice(chars) for _ in range(width)) + RESET + "\n")
        sys.stdout.flush()
        await asyncio.sleep(0.06)

# ================== FX: SPIDER ==================

SPIDER = ["\\_oo_/", "/_.._\\", "\\ oo /", "/____\\"]

async def spider_walk(stop):
    width = shutil.get_terminal_size((80, 20)).columns
    x = 0
    f = 0
    while not stop.is_set():
        glow = random.choice([GREEN, GLOW])
        sys.stdout.write("\033[s\033[H")
        sys.stdout.write(" " * x + glow + SPIDER[f % len(SPIDER)] + RESET)
        sys.stdout.write("\033[u")
        sys.stdout.flush()
        x = (x + 2) % max(1, width - 8)
        f += 1
        await asyncio.sleep(0.15)

# ================== UTILS ==================

def sha256(b): return hashlib.sha256(b).hexdigest()

def entropy(text):
    freq = {}
    for c in text:
        freq[c] = freq.get(c, 0) + 1
    e = 0
    for c in freq:
        p = freq[c] / len(text)
        e -= p * log2(p)
    return round(e, 2)

def keyword_score(text):
    return sum(5 for k in KEYWORDS if k in text.lower())

# ================== DB ==================

async def init_db():
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS pages(
            url TEXT PRIMARY KEY,
            depth INT,
            status INT,
            hash TEXT,
            entropy REAL,
            score INT,
            ts REAL)
        """)
        await db.commit()

# ================== SPIDER CORE ==================

visited = set()
seen = set()
queue = asyncio.PriorityQueue()

async def fetch(session, url):
    try:
        async with session.get(url, headers={"User-Agent": USER_AGENT}, timeout=20) as r:
            return r.status, r.headers.get("content-type",""), await r.read()
    except:
        return None, None, None

def links(base, html):
    soup = BeautifulSoup(html, "lxml")
    for a in soup.find_all("a", href=True):
        u = urljoin(base, a["href"]).split("#")[0]
        if u.startswith("http"): yield u

async def worker(session, db, rp, domain):
    while True:
        prio, (url, depth) = await queue.get()
        if depth > MAX_DEPTH or url in seen or not rp.can_fetch(USER_AGENT, url):
            queue.task_done(); continue
        seen.add(url)
        await asyncio.sleep(random.uniform(*CRAWL_DELAY))

        status, ctype, data = await fetch(session, url)
        if not data: queue.task_done(); continue

        h = sha256(data)
        if h in visited: queue.task_done(); continue
        visited.add(h)

        text = data.decode(errors="ignore")
        ent = entropy(text[:4000])
        score = keyword_score(text)

        await db.execute(
            "INSERT OR REPLACE INTO pages VALUES (?,?,?,?,?,?,?)",
            (url, depth, status, h, ent, score, time.time()))
        await db.commit()

        sys.stdout.write(GLOW + f"[+] {url} | score={score} | entropy={ent}\n" + RESET)

        if "text/html" in ctype:
            for l in links(url, text):
                if tldextract.extract(l).domain == domain:
                    await queue.put((-(score+random.randint(0,5)), (l, depth+1)))
        queue.task_done()

# ================== MAIN ==================

async def main(target):
    ext = tldextract.extract(target)
    rp = robotparser.RobotFileParser()
    rp.set_url(urljoin(target, "/robots.txt"))
    try: rp.read()
    except: pass

    await init_db()
    await queue.put((0, (target, 0)))

    stop_fx = asyncio.Event()
    fx1 = asyncio.create_task(matrix_rain(stop_fx))
    fx2 = asyncio.create_task(spider_walk(stop_fx))

    async with aiohttp.ClientSession() as session:
        async with aiosqlite.connect(DB_FILE) as db:
            workers = [asyncio.create_task(worker(session, db, rp, ext.domain))
                       for _ in range(MAX_CONCURRENCY)]
            await queue.join()
            stop_fx.set()
            for w in workers: w.cancel()
            fx1.cancel(); fx2.cancel()

# ================== ENTRY ==================

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python kArmas_sPiDeR.py https://target.com")
        sys.exit(1)

    karma_banner()
    asyncio.run(main(sys.argv[1]))
