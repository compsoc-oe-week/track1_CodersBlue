# Samantha — An AI Terminal Assistant for openEuler
> Hackathon: **OpenEuler Challenge Week** · Team size: 5 · Time: **1 day**

Samantha is a **Her-inspired**, empathetic **terminal assistant** for openEuler that turns natural-language requests into **safe, auditable shell actions**, with **advanced search**, **multi-step pipelines**, and **agentic behaviors** (self-correction, planning, and proactive suggestions).

This README doubles as our **roadmap**, **runbook**, and **judge-facing guide**.

---

## � Judging Criteria → Design Goals
1. **Tier 1**: "copy all PDFs from ~/Downloads to ~/docs" → preview → confirm → success.
2. **Tier 2**: "find logs >100MB last 7 days, compress and move to ~/backup/logs" → step checkpoints.
3. **Tier 3**: Search with a typo → Samantha suggests correction → retry works. Suggests cron job.
4. **openEuler**: "what kernel am I on?" + "install ripgrep and re-run OOM search".

Demo data lives in `demo_data/` for deterministic results.CLI
- Warm, empathetic conversational tone
- ANSI colors for commands/warnings/success
- ASCII visuals for directory trees, bar charts
- Built-in help system (`--help` or `?`)tural-language requests into **safe, auditable shell actions**, with **advanced search**, **multi-step pipelines**, and **agentic behaviors** (self-correction, planning, and proactive suggestions).

This README doubles as our **roadmap**, **runbook**, and **judge-facing guide**.

---

## 🧭 Judging Criteria → Design Goals
- **Functionality / Tier completion (40%)** → Deliver all Tiers 1–3 with crisp demo flows.
- **Technical sophistication (30%)** → JSON-bound model calls, safe execution, multi-step planning, recovery.
- **UX & Her-inspired feel (20%)** → Warm persona, ANSI-colored output, clear confirmations, ASCII visuals.
- **openEuler integration (10%)** → `dnf`/`yum`, kernel queries, rpm tooling, perf-minded search.

---

## ⚙️ Environment & Endpoints (Track 1)
We use two **OpenAI-compatible** vLLM instances:

- **Coder model**: `Qwen/Qwen3-Coder-480B-A35B-Instruct-FP8`  
  - Host: `eidf219-network-machine.os.eidf.epcc.ed.ac.uk:8000`
- **Visual model**: `Qwen/Qwen2.5-VL-32B-Instruct` (vision)  
  - Host: `eidf219-network-machine.vms.os.eidf.epcc.ed.ac.uk:8001`

### Quick test from VM
```bash
curl http://eidf219-network-machine.vms.os.eidf.epcc.ed.ac.uk:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen3-Coder-480B-A35B-Instruct-FP8",
    "messages": [{"role": "user", "content": "Give me a short introduction to large language models."}],
    "temperature": 0.6, "top_p": 0.95, "top_k": 20, "max_tokens": 32768
  }'
```

### SSH tunnel from local
```bash
# Coder
ssh -J <username>@eidf-gateway.epcc.ed.ac.uk -L 8000:YOUR_SERVER_IP:8000 -N <username>@<vm_ip>

# Vision
ssh -J <username>@eidf-gateway.epcc.ed.ac.uk -L 8001:YOUR_SERVER_IP:8001 -N <username>@<vm_ip>
```

Then call `http://localhost:8000/v1` or `http://localhost:8001/v1`.

**Docker note**: use `--network=host` (Linux) or `host.docker.internal:8000/8001`.

---

## 🗂 Project Structure & Role Assignments

We divide the project into clear modules so each role can own specific files without blocking others.

```
.
├── src/
│   ├── cli/
│   │   └── samantha.py         # CLI entrypoint (glue everything) → Lead
│   ├── core/
│   │   ├── nl2cmd.py           # NL → JSON plan (prompts, parsing) → NL & Model
│   │   ├── executor.py         # Execute commands, dry-run, undo log → Terminal
│   │   ├── safety.py           # Path validation, denylist, confirmations → Terminal
│   │   ├── search.py           # find/grep/rg, filters, fuzzy → Search & Agent
│   │   ├── planner.py          # Multi-step pipelines, checkpoints → Search & Agent
│   │   ├── memory.py           # Session state, context, pronouns → Search & Agent
│   │   └── utils.py            # Shared helpers → Lead
│   ├── osint/
│   │   └── openeuler.py        # openEuler integration (dnf, kernel info) → Lead
│   ├── vision/
│   │   └── ascii_art.py        # Optional ASCII/diagram helpers → UX & Persona
│   └── ui/
│       ├── colors.py           # ANSI styling → UX & Persona
│       └── persona.py          # "Her"-style tone, system prompts → UX & Persona
├── notebooks/
│   └── experiments.ipynb       # Quick prompt/model spikes → NL & Model
├── tests/
│   ├── test_nl2cmd.py          # Unit tests for parsing → NL & Model
│   ├── test_executor.py        # Unit tests for safety/execution → Terminal
│   ├── test_search.py          # Unit tests for filters/fuzzy → Search & Agent
│   └── test_persona.py         # Persona tone/UX tests → UX & Persona
├── demo_data/                  # Seed files for predictable demo
│   ├── logs/                   # Large log files
│   └── docs/                   # PDFs, text samples
├── requirements.txt
├── Makefile
└── README.md
```

---

## 🗂 Project Structure & Role Assignments

We divide the project into clear modules so each role can own specific files without blocking others.

```
.
├── src/
│   ├── cli/
│   │   └── samantha.py         # CLI entrypoint (glue everything) → Lead
│   ├── core/
│   │   ├── nl2cmd.py           # NL → JSON plan (prompts, parsing) → NL & Model
│   │   ├── executor.py         # Execute commands, dry-run, undo log → Terminal
│   │   ├── safety.py           # Path validation, denylist, confirmations → Terminal
│   │   ├── search.py           # find/grep/rg, filters, fuzzy → Search & Agent
│   │   ├── planner.py          # Multi-step pipelines, checkpoints → Search & Agent
│   │   ├── memory.py           # Session state, context, pronouns → Search & Agent
│   │   └── utils.py            # Shared helpers → Lead
│   ├── osint/
│   │   └── openeuler.py        # openEuler integration (dnf, kernel info) → Lead
│   ├── vision/
│   │   └── ascii_art.py        # Optional ASCII/diagram helpers → UX & Persona
│   └── ui/
│       ├── colors.py           # ANSI styling → UX & Persona
│       └── persona.py          # “Her”-style tone, system prompts → UX & Persona
├── notebooks/
│   └── experiments.ipynb       # Quick prompt/model spikes → NL & Model
├── tests/
│   ├── test_nl2cmd.py          # Unit tests for parsing → NL & Model
│   ├── test_executor.py        # Unit tests for safety/execution → Terminal
│   ├── test_search.py          # Unit tests for filters/fuzzy → Search & Agent
│   └── test_persona.py         # Persona tone/UX tests → UX & Persona
├── demo_data/                  # Seed files for predictable demo
│   ├── logs/                   # Large log files
│   └── docs/                   # PDFs, text samples
├── requirements.txt
├── Makefile
└── README.md
### 📌 Role-to-File Mapping

1. **Team lead & architect**
   - `src/cli/samantha.py`, `src/core/utils.py`, `src/osint/openeuler.py`
   - Oversees merges + demo script

2. **NL & model integration**
   - `src/core/nl2cmd.py`, `notebooks/experiments.ipynb`, `tests/test_nl2cmd.py`

3. **Terminal integration**
   - `src/core/executor.py`, `src/core/safety.py`, `tests/test_executor.py`

4. **Search & agentic behaviour**
   - `src/core/search.py`, `src/core/planner.py`, `src/core/memory.py`, `tests/test_search.py`

5. **UX & persona**
   - `src/ui/colors.py`, `src/ui/persona.py`, `src/vision/ascii_art.py`, `tests/test_persona.py`

---

## 🚀 Install & Run

### Requirements
- openEuler Docker/VM provided by organisers
- Python 3.10+ (system Python ok)
- Optional: ripgrep for fast content search

### Installation
```bash
# Install deps
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Env vars
export OPENAI_API_KEY=EMPTY
export CODER_BASE_URL=http://localhost:8000/v1
export VISION_BASE_URL=http://localhost:8001/v1

# Smoke run
# Smoke run
python -m src.cli.samantha "copy all PDFs from downloads to docs"
```

---

## ✅ Tier-by-Tier Plan

### Tier 1 — Basic Operations
- NL → JSON command plan
- File ops (cp, mv, rm, ls) with preview & confirmation
- Safety checks (denylist, dry-run, undo log)
- Basic search (find, grep), fuzzy matching

### Tier 2 — Advanced Search & Multi-Step
- Context memory for pronouns & follow-ups
- Multi-step pipelines with checkpoints
- Advanced filters: size, date, owner, patterns

### Tier 3 — Agentic Capabilities
- Self-correction ("Did you mean…?")
- Planning with feedback (recover from errors)
- Proactive suggestions (cron jobs for repeated tasks)
```
✅ Tier-by-Tier Plan
Tier 1 — Basic Operations
NL → JSON command plan

File ops (cp, mv, rm, ls) with preview & confirmation

Safety checks (denylist, dry-run, undo log)

Basic search (find, grep), fuzzy matching

Tier 2 — Advanced Search & Multi-Step
Context memory for pronouns & follow-ups

Multi-step pipelines with checkpoints

Advanced filters: size, date, owner, patterns

Tier 3 — Agentic Capabilities
Self-correction (“Did you mean…?”)

Planning with feedback (recover from errors)

Proactive suggestions (cron jobs for repeated tasks)

🎨 UX: “Her”-Inspired CLI
Warm, empathetic conversational tone

ANSI colors for commands/warnings/success

ASCII visuals for directory trees, bar charts

Built-in help system (--help or ?)

---

## 🐧 openEuler Integration
- `dnf search <pkg>`, `dnf info <pkg>`, `dnf install <pkg>`
- `uname -r`, `cat /etc/os-release`
- Prefer ripgrep if available for performance

🧵 Demo Script (5–7 minutes)
Tier 1: “copy all PDFs from ~/Downloads to ~/docs” → preview → confirm → success.

Tier 2: “find logs >100MB last 7 days, compress and move to ~/backup/logs” → step checkpoints.

Tier 3: Search with a typo → Samantha suggests correction → retry works. Suggests cron job.

openEuler: “what kernel am I on?” + “install ripgrep and re-run OOM search”.

Demo data lives in demo_data/ for deterministic results.

---

## ⏱ One-Day Execution Plan (hour-by-hour)
- **T+0:00–1:00** — Setup: Repo, env vars, test API, scaffold core modules.
- **T+1:00–3:00** — Tier 1: Commands, safety, undo, search.
- **T+3:00–6:00** — Tier 2: Memory, pipelines, filters.
- **T+6:00–8:00** — Tier 3: Self-correction, replanning, proactive suggestions.
- **T+8:00–9:00** — openEuler integration: dnf, kernel queries, perf optimisations.
- **T+9:00–10:00** — Polish: UX tone, colors, help, demo rehearsal.

---

## 🔒 Safety Rules
- Always preview before execution
- Double confirmation for destructive ops
- Denylist sensitive paths
- Maintain undo log for recovery

---

## 🧱 Minimal CLI Skeleton
```python
# src/cli/samantha.py
import argparse
from src.core import nl2cmd, executor, memory, safety

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt", nargs="+")
    args = ap.parse_args()
    user_intent = " ".join(args.prompt)

    plan = nl2cmd.make_plan(user_intent)
    plan = safety.sanitize_plan(plan)
    executor.preview(plan)
    if executor.confirm(plan):
        results = executor.run(plan)
        memory.update(results=results, plan=plan)
        executor.summarize(results)

if __name__ == "__main__":
    main()
```

---

## 📝 Deliverables Checklist
- [ ] Tier 1–3 implemented
- [ ] openEuler commands working
- [ ] Safety features enforced
- [ ] Demo script rehearsed
- [ ] README + Makefile complete

---

## 👥 Team Roles
- **Team lead & architect** – stand-ups, module integration, progress tracking
- **NL & model integration** – prompts, chat model calls, output parsing
- **Terminal integration** – file ops, safety checks, core commands
- **Search & agentic behaviour** – advanced search, pipelines, self-correction
- **UX & persona** – conversational tone, ANSI UI, CLI polish

---

## 🙌 Credits
Built by a five-member team during OpenEuler Challenge Week.

---

**Would you like me to also generate stub `.py` files with TODOs** so you can `git clone` + `touch` everything and start coding immediately without wasting time on scaffolding?






