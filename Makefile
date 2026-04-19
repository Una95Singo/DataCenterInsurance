# Single entry point for the pipeline.
# `make all` runs every phase from a clean checkout.
# Targets are implemented incrementally as each phase lands.

.PHONY: all data fetch-raw scrape-dcm audit analysis interp paper lint test clean help

help:
	@echo "Targets:"
	@echo "  all       - run the full pipeline (data -> audit -> analysis -> interp -> paper)"
	@echo "  data      - phase 1: data collection"
	@echo "  fetch-raw - download active sources in scripts/raw_sources.yaml"
	@echo "  scrape-dcm - §1.1 datacentermap.com metro scrape (~490 GETs, ~16 min)"
	@echo "  audit     - phase 2: validation & bias audit"
	@echo "  analysis  - phase 3: spatial analysis"
	@echo "  interp    - phase 4: findings interpretation"
	@echo "  paper     - phase 5: render paper + substack"
	@echo "  lint      - ruff check"
	@echo "  test      - pytest"
	@echo "  clean     - remove processed data and generated figures"

all: data audit analysis interp paper

data:
	@echo "[phase 1] data collection — not yet implemented"

fetch-raw:
	python scripts/fetch_raw.py

scrape-dcm:
	python scripts/scrape_datacentermap.py

audit:
	@echo "[phase 2] validation & bias audit — not yet implemented"

analysis:
	@echo "[phase 3] spatial analysis — not yet implemented"

interp:
	@echo "[phase 4] findings interpretation — not yet implemented"

paper:
	@echo "[phase 5] paper render — not yet implemented"

lint:
	ruff check src tests

test:
	PYTHONPATH=src pytest -q

clean:
	rm -rf data/processed/* figures/*.png figures/*.caption.md
	@echo "cleaned data/processed and figures"
