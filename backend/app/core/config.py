from __future__ import annotations

import sys
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


REPO_ROOT = Path(__file__).resolve().parents[3]

# Default conda/mamba runner: use 'conda' on Windows, 'mamba' on other platforms.
_DEFAULT_RUNNER_EXECUTABLE: str = "conda" if sys.platform == "win32" else "mamba"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="AI4ML_",
        extra="ignore",
        env_file=str(REPO_ROOT / ".env"),
        env_file_encoding="utf-8",
    )

    app_name: str = "AI4ML Backend"
    api_prefix: str = "/api"
    repo_root: Path = REPO_ROOT
    storage_dir: Path = REPO_ROOT / "storage" / "tasks"
    run_output_dir: Path = REPO_ROOT / "storage" / "mlzero_runs"
    mlzero_runtime_dir: Path = REPO_ROOT / "storage" / "mlzero_runtime"

    # --- Cloud / Huawei MaaS defaults (used by default on Windows student setup) ---
    mlzero_config_path: Path = REPO_ROOT / "backend" / "config" / "mlzero-huawei-openai.yaml"
    mlzero_openai_base_url: str = "https://api.modelarts-maas.com/openai/v1"
    mlzero_openai_api_key: str = "local"
    mlzero_use_local_provider: bool = False
    mlzero_runner_executable: str = _DEFAULT_RUNNER_EXECUTABLE
    mlzero_env_name: str = "mlzero"
    mlzero_max_iterations: int = 2
    mlzero_hf_endpoint: str = "https://hf-mirror.com"

    # --- Local llama-cpp provider settings (Mac/dev only, not used when mlzero_use_local_provider=False) ---
    mlzero_model_path: Path = REPO_ROOT / "local" / "models" / "Qwen2.5-Coder-0.5B-Instruct-Q4_K_M.gguf"
    mlzero_mamba_executable: Path = Path.home() / ".local" / "miniforge3" / "bin" / "mamba"
    mlzero_server_host: str = "127.0.0.1"
    mlzero_server_port: int = 8001
    mlzero_model_alias: str = "gpt-4-local"
    mlzero_chat_format: str = "chatml"
    mlzero_context_size: int = 4096
    mlzero_server_threads: int = -1

    selected_project_base: str = "mlzero / autogluon-assistant"
    execution_runtime: str = "mlzero + Huawei MaaS openai-compatible"

    @property
    def mlzero_provider_base_url(self) -> str:
        """Base URL for the local llama-cpp server (used only when mlzero_use_local_provider=True)."""
        return f"http://{self.mlzero_server_host}:{self.mlzero_server_port}/v1"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.storage_dir.mkdir(parents=True, exist_ok=True)
    settings.run_output_dir.mkdir(parents=True, exist_ok=True)
    settings.mlzero_runtime_dir.mkdir(parents=True, exist_ok=True)
    return settings
