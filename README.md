# Barnacle Scraper (retired)

Barnacle Scraper is a Python-based automation tool designed to analyze the Steam Community Market for long-term investment potential. It builds and maintains a local SQLite database, collects market data in staged passes, applies heuristics to reduce redundant work, and scores items based on liquidity and price trends. The system is designed to be idempotent, resilient to interruption, and capable of resuming from its last known state.

---

## Overview

Barnacle Scraper’s goal is to create a complete, local snapshot of the Steam Community Market and evaluate items for investment viability. It operates in multiple phases:

- **Phase 1 — Preliminary Data Collection:**  
  Creates a local snapshot of the market, gathering basic item attributes (price, quality, etc.).

- **Phase 2 — Targeted Data Collection:**  
  Applies heuristics to narrow the item pool and fetches detailed history only for items that meet update criteria.

- **Phase 3 — Investment Scoring:**  
  Evaluates items using recent price trends, liquidity indicators, and other heuristics.

The system is built to safely resume after interruption. State is cached to the database after each completed step, allowing the scraper to continue from the last processed page or item.

---

## Key Features

- Local SQLite database with automatic setup and maintenance  
- Idempotent design — one run completes all stages end-to-end  
- Rolling-window heuristics to avoid redundant scraping  
- Multi-stage pipeline for efficient data collection  
- Network-call minimization through batching when ever possible 
- Graceful resume behavior after interruption  
- Cooldown, jitter, and backoff strategy to reduce automation detection  
- Dependency-free implementation (Python standard library only)

---

## Tech Stack

- **Python 3.12.7**  
- **SQLite** (via Python’s built-in `sqlite3`)  
- **No external dependencies** — all HTML parsing and logic implemented using standard library modules

---

## How to Run

1. Ensure your Python environment is active (Python 3.12.7+).  
2. Navigate to the project directory.  
3. Run:

```bash
python main.py
```
The program will automatically initialize the database and begin the scraping pipeline.

---

## Project Structure

```text
barnacle_scraper/
├── data/
├── resources/
├── src/
│   ├── application/
│   ├── config/
│   ├── domain/
│   ├── infrastructure/
│   └── main.py
└── README.md
```
---

## Current Status & Limitations

This project was undergoing a refactor and is currently retired. It is not recommended for real‑world use in its current form due to strict automation detection and is better suited for deployment over cloud infrastructure.

- Even with cooldowns, jitter, and backoff strategies, the scraper eventually triggered automation flags.
- Long continuous runs (~48 hours projected for full market coverage) increased the likelihood of soft IP throttling.
- A cloud‑based deployment with fan out approach would be more appropriate for future iterations.
- Use of unofficial APIs mean that calls can break or the data returned could be structured differently.

Despite these limitations, Barnacle Scraper demonstrates:

- Practical experience with automation pipelines
- Heuristic‑based optimization
- Database‑backed state management
- Resilience and idempotent design

---

## Future Improvements
- Console‑based progress visualization
- Rolling‑window performance logging system
- Distributed or cloud‑based execution

---

## Disclaimer
This project is for educational and experimental purposes only.
It is not intended for production use or large‑scale scraping of the Steam Community Market.