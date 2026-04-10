# AI4ML

AI4ML is a course project for a low-code / no-code machine learning community platform. The current repository state targets the Week 2 milestone in the project plan dated 2026-04-01: finalize the long-term base platform, validate that base locally on the current machine, record the environment honestly, and scaffold the frontend/backend repository structure around the chosen runtime.

## Week 2 deliverables

- Finalized the long-term upstream base as `MLZero / AutoGluon Assistant`.
- Validated the selected MLZero base locally with `llama-cpp-python` and a local GGUF model.
- Pulled the main GitHub candidate repositories into `external/` for architecture and selection review.
- Verified a direct MLZero executor run and a full API-backed task flow on the current machine.
- Added an initial monorepo structure for `frontend`, `backend`, `docs`, `scripts`, `data`, `local`, and `storage`.
- Defined the first-round API boundaries for task creation, CSV upload, MLZero execution, and run inspection.

## Latest local validation

- Direct executor validation succeeded with `validation_score = 0.9` at `storage/mlzero_runs/irismlz_fastpath6/20260401T021635Z`.
- API integration validation succeeded with task `f2032269` and `validation_score = 0.9` at `storage/mlzero_runs/f2032269/20260401T021837Z`.
- `GET /api/health` currently reports `execution_runtime = mlzero + Huawei MaaS openai-compatible`.

## Repository layout

```text
AI4ML/
├── backend/                  # FastAPI service, MLZero executor, and local provider runtime
├── data/                     # Sample datasets and local fixtures
├── docs/                     # Week 2 architecture / selection / environment records
├── external/                 # Upstream repos; MLZero is installed editable from here
├── frontend/                 # Vite + React task prototype
├── local/                    # Local GGUF model files and other machine-local assets
├── scripts/                  # Reproducible helper scripts
├── storage/                  # Local task uploads, MLZero outputs, and runtime logs
├── .env.example              # Template for secrets – copy to .env and fill in
├── weekly_report_template.md
└── 1."智算"AI4ML 社区.docx
```

## Quick start

### 1. One-time: create your `.env` file (Windows + Huawei MaaS)

```powershell
# At repository root (D:\Project\gitProject\AI4ML)
Copy-Item .env.example .env
```

Open `.env` and replace the placeholder with your real Huawei MaaS API key:

```
AI4ML_MLZERO_OPENAI_API_KEY=your-actual-maas-key
```

The backend loads `.env` automatically on startup – no per-run environment variables needed.

### 2. Create and activate the `mlzero` conda environment

```powershell
conda create -n mlzero python=3.11 -y
conda activate mlzero
pip install -e external/autogluon-assistant
```

### 3. Backend

```powershell
conda activate mlzero
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload --port 8000
```

Quick health check:

```powershell
curl http://127.0.0.1:8000/api/health
```

### 4. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` after the backend is running on `http://localhost:8000`.

---

## Switching back to local llama-cpp (Mac / dev setup)

If you want to use a local `llama-cpp-python` server instead of Huawei MaaS, add the following overrides to your `.env` (or set them as environment variables before starting the backend):

```dotenv
AI4ML_MLZERO_USE_LOCAL_PROVIDER=true
AI4ML_MLZERO_CONFIG_PATH=backend/config/mlzero-local-openai.yaml
AI4ML_MLZERO_RUNNER_EXECUTABLE=mamba
```

The local model file must be present at `local/models/Qwen2.5-Coder-0.5B-Instruct-Q4_K_M.gguf`.

---

## Week 2 documents

- `docs/week2-tech-selection.md`
- `docs/week2-architecture.md`
- `docs/week2-environment-validation.md`
- `docs/repository-guidelines.md`
- `docs/current-memory.md`

## Current decision

The selected project base is `MLZero / AutoGluon Assistant`. This base is also the active local execution path in this repo.

`AIDE ML` and `AutoML-Agent` remain architecture references:

- `AIDE ML` for experiment-tree and progress visualization ideas
- `AutoML-Agent` for role decomposition and multi-agent module boundaries

`AutoGluon Tabular 1.1.0` is no longer the active runtime path. It only remains as historical context from earlier Week 2 exploration.

The default configuration targets Windows students using Huawei MaaS (`deepseek-v3.2`) with a `conda` runner and the `mlzero-huawei-openai.yaml` config. Local llama-cpp remains available via the overrides described above.
