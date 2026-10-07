"""Configuración centralizada del sistema.

Todos los parámetros de servicios de terceros (GitHub, LLM/OpenAI/OpenRouter,
Langfuse) se leen desde variables de entorno para evitar valores "hardcodeados"
en el código.

Se puede usar un archivo ``.env`` que será cargado
automáticamente mediante ``python-dotenv`` si está presente.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Optional

try:  # pragma: no cover - carga opcional de .env
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # pragma: no cover
    pass


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    return os.getenv(name, default)


def _env_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    try:
        return float(value)
    except ValueError:
        return default


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    try:
        return int(value)
    except ValueError:
        return default


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass
class MCPConfig:
    """Configuración de acceso al servidor MCP."""

    base_url: str = field(
        default_factory=lambda: _env("MCP_BASE_URL", "https://7680-fast-mcp-server.fastmcp.app/mcp")
    )
    api_key: Optional[str] = field(default_factory=lambda: _env("MCP_API_KEY"))

@dataclass
class LLMConfig:
    """Configuración del proveedor de LLM: OpenAI u OpenRouter (capa gratuita)."""

    provider: str = field(
        default_factory=lambda: _env("LLM_PROVIDER", "openrouter").lower()
    )
    api_key: Optional[str] = field(
        default_factory=lambda: _env("LLM_API_KEY")
        or _env("OPENROUTER_API_KEY")
        or _env("OPENAI_API_KEY")
    )
    base_url: Optional[str] = field(
        default_factory=lambda: _env(
            "LLM_BASE_URL",
            None,
        )
    )
    model: str = field(
        default_factory=lambda: _env(
            "LLM_MODEL", "meta-llama/llama-3.1-8b-instruct:free"
        )
    )
    temperature: float = field(default_factory=lambda: _env_float("LLM_TEMPERATURE", 0.2))
    max_tokens: int = field(default_factory=lambda: _env_int("LLM_MAX_TOKENS", 600))
    request_timeout: int = field(default_factory=lambda: _env_int("LLM_TIMEOUT", 60))

    def resolved_base_url(self) -> Optional[str]:
        if self.base_url:
            return self.base_url
        if self.provider == "openrouter":
            return "https://openrouter.ai/api/v1"
        return None  # usa el default de OpenAI


@dataclass
class LangfuseConfig:
    """Configuración de observabilidad con Langfuse."""

    public_key: Optional[str] = field(default_factory=lambda: _env("LANGFUSE_PUBLIC_KEY"))
    secret_key: Optional[str] = field(default_factory=lambda: _env("LANGFUSE_SECRET_KEY"))
    host: str = field(
        default_factory=lambda: _env("LANGFUSE_HOST", "https://cloud.langfuse.com")
    )
    enabled: bool = field(default_factory=lambda: _env_bool("LANGFUSE_ENABLED", True))

    @property
    def is_configured(self) -> bool:
        return self.enabled and bool(self.public_key) and bool(self.secret_key)


@dataclass
class AppConfig:
    """Configuración raíz que agrupa toda la configuración de la aplicación."""

    llm: LLMConfig = field(default_factory=LLMConfig)
    mcp: MCPConfig = field(default_factory=MCPConfig)
    langfuse: LangfuseConfig = field(default_factory=LangfuseConfig)

    @classmethod
    def from_env(cls) -> "AppConfig":
        return cls()


def get_config() -> AppConfig:
    """Punto de entrada único para obtener la configuración de la aplicación."""

    return AppConfig.from_env()
