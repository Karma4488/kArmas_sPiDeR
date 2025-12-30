# kArmas_sPiDeR

SPIDER_FRAMES = [
    r"/\oo/\ ",
    r"\_.._/ ",
    r"/ oo \ ",
    r"\____/ "

🕷️ kArmas_sPiDeR
Intelligent Web Spider
“Knowledge is power. Information wants to be free 

📌 Overview
kArmas_sPiDeR is a high-performance, intelligent, ethical web spider built for authorized security research, OSINT, reconnaissance, and asset discovery.
Designed to run flawlessly on Termux (Android 16) and standard Linux environments, it combines a modern async crawling engine with a visually distinctive Matrix-style terminal interface.
This is not a toy crawler — it is engineered for professionals who value speed, intelligence, traceability, and 

🧠 Core Capabilities
🔍 Intelligent Crawling
Async engine (asyncio + aiohttp)
Priority-based crawl frontier
Smart depth control
Duplicate content detection (SHA-256)
Domain-restricted crawling
Sitemap & HTML link discovery

🧬 Content Intelligence
Keyword-based page scoring
Entropy analysis (detects obfuscation / randomness)
Automatic identification of potentially sensitive pages
Structured data persistence
🗄️ Persistence & Auditability
SQLite database storage
Timestamped crawl records
Ideal for reporting, auditing, and post-analysis
🤖 Ethical by Design
robots.txt enforced
Rate-limited (human-like delays)

🎭 Visual Interface (Terminal FX)
Live Matrix rain (non-blocking)
Animated ASCII spider crawling across the terminal
Green glow & flicker effects
Clean, readable crawl output
Termux-safe ANSI rendering (no curses)
Visuals run in parallel and do not affect crawl performance.

🧰 Requirements
Platform
Termux 118.3 (Android 16)
Linux / WSL also supported
Dependencies
pkg install python -y
pip install aiohttp aiosqlite beautifulsoup4 lxml tldextract

🚀 Usage

python kArmas_sPiDeR.py https://target.com

📂 Output
SQLite Database
kArmas_sPiDeR.db
Field
Description
url
Crawled URL
depth
Crawl depth
status
HTTP status code
hash
SHA-256 content hash
entropy
Entropy score (obfuscation indicator)
score
Keyword intelligence score
ts
Timestamp
This structure is ideal for:
Security reports
Asset inventories
Recon pipelines
OSINT correlation


🧩 Design Philosophy
Professional over noisy
Intelligence over brute force
Visibility over stealth

Roadmap (Optional Extensions)
Live crawl statistics HUD
Export to JSON / CSV
API-only crawling mode
Visual crawl graph generation
Tor-routed mode (opt-in)

We are Anonymous.
We are Legion.
We do not forgive.
We do not forget.
Its now to late to expect US

Made in l0v3 bY kArmasec



