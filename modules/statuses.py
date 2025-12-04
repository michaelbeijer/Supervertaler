"""Centralized status vocabulary for Supervertaler segments."""

from dataclasses import dataclass
from typing import Dict, Optional
import re


@dataclass(frozen=True)
class StatusDefinition:
    key: str
    label: str
    icon: str
    color: str
    memoq_label: str
    memoQ_equivalents: tuple[str, ...]
    match_symbol: str = ""


STATUSES: Dict[str, StatusDefinition] = {
    "not_started": StatusDefinition(
        key="not_started",
        label="Not started",
        icon="❌",  # Red X - clear "not done" indicator (matches memoQ style)
        color="#ffe6e6",
        memoq_label="Not started",
        memoQ_equivalents=("not started", "not translated"),
    ),
    "pretranslated": StatusDefinition(
        key="pretranslated",
        label="Pre-translated",
        icon="🤖",  # Robot - indicates automatic/machine pre-translation
        color="#e8f2ff",
        memoq_label="Pre-translated",
        memoQ_equivalents=("pre-translated", "pretranslated"),
        match_symbol="⚡",
    ),
    "translated": StatusDefinition(
        key="translated",
        label="Translated",
        icon="✏️",  # Pencil - indicates manual translation work (matches Trados style)
        color="#e6ffe6",
        memoq_label="Translated",
        memoQ_equivalents=("translated",),
        match_symbol="✍️",
    ),
    "confirmed": StatusDefinition(
        key="confirmed",
        label="Confirmed",
        icon="✔",  # Checkmark - will be styled green via CSS
        color="#d1ffd6",
        memoq_label="Confirmed",
        memoQ_equivalents=("confirmed",),
        match_symbol="🛡️",
    ),
    "tr_confirmed": StatusDefinition(
        key="tr_confirmed",
        label="TR confirmed",
        icon="🌟",
        color="#d9f0ff",
        memoq_label="TR confirmed",
        memoQ_equivalents=("tr confirmed", "translation review confirmed"),
        match_symbol="🌐",
    ),
    "proofread": StatusDefinition(
        key="proofread",
        label="Proofread",
        icon="🟪",
        color="#efe0ff",
        memoq_label="Proofread",
        memoQ_equivalents=("proofread",),
        match_symbol="📘",
    ),
    "rejected": StatusDefinition(
        key="rejected",
        label="Rejected",
        icon="🚫",
        color="#ffe0e0",
        memoq_label="Rejected",
        memoQ_equivalents=("rejected",),
        match_symbol="⛔",
    ),
    "approved": StatusDefinition(
        key="approved",
        label="Approved",
        icon="⭐",
        color="#e6f3ff",
        memoq_label="Approved",
        memoQ_equivalents=("approved", "final", "proofread confirmed"),
        match_symbol="🏁",
    ),
    "cm": StatusDefinition(
        key="cm",
        label="CM (101%)",
        icon="💎",  # Diamond - highest quality match (context match)
        color="#c3e6cb",  # Darker green - very high confidence
        memoq_label="Pre-translated (101%)",
        memoQ_equivalents=("pre-translated (101%)", "context match", "cm", "101%"),
        match_symbol="💎",
    ),
    "tm_100": StatusDefinition(
        key="tm_100",
        label="TM 100%",
        icon="✅",  # Checkmark - exact match
        color="#d4edda",  # Light green - high confidence
        memoq_label="Pre-translated (100%)",
        memoQ_equivalents=("pre-translated (100%)", "100%", "exact match"),
        match_symbol="✅",
    ),
    "tm_fuzzy": StatusDefinition(
        key="tm_fuzzy",
        label="TM Fuzzy",
        icon="🔶",  # Orange diamond - partial match
        color="#fff3cd",  # Light yellow/orange - needs review
        memoq_label="Pre-translated (fuzzy)",
        memoQ_equivalents=("fuzzy", "fuzzy match"),
        match_symbol="🔶",
    ),
    "repetition": StatusDefinition(
        key="repetition",
        label="Repetition",
        icon="🔁",  # Repeat icon - internal repetition
        color="#e2e3e5",  # Light gray - auto-propagated
        memoq_label="Repetition",
        memoQ_equivalents=("repetition", "rep", "auto-propagated"),
        match_symbol="🔁",
    ),
    "machine_translated": StatusDefinition(
        key="machine_translated",
        label="MT",
        icon="🤖",  # Robot - machine translation
        color="#ffeaa7",  # Light orange/yellow - needs review
        memoq_label="Machine Translated",
        memoQ_equivalents=("machine translated", "mt", "nmt", "auto-translated"),
        match_symbol="🤖",
    ),
}

DEFAULT_STATUS = STATUSES["not_started"]


def get_status(key: str) -> StatusDefinition:
    """Return status definition for key, falling back to default."""
    return STATUSES.get(key, DEFAULT_STATUS)


def match_memoq_status(status_text: str) -> tuple[StatusDefinition, Optional[int]]:
    """Map memoQ status string to a StatusDefinition plus optional match percent."""
    status_clean = (status_text or "").strip()
    percent: Optional[int] = None

    if status_clean:
        match = re.search(r"(\d+)\s*%", status_clean)
        if match:
            try:
                percent = int(match.group(1))
            except ValueError:
                percent = None

    lower = status_clean.lower()

    for definition in STATUSES.values():
        if any(eq in lower for eq in definition.memoQ_equivalents):
            return definition, percent

    if "proofread" in lower and "confirm" in lower:
        return STATUSES["approved"], percent
    if "confirm" in lower and "tr" in lower:
        return STATUSES["tr_confirmed"], percent
    if "confirm" in lower:
        return STATUSES["confirmed"], percent
    if "lock" in lower:
        return STATUSES["not_started"], percent
    if "reject" in lower:
        return STATUSES["rejected"], percent
    if "proof" in lower:
        return STATUSES["proofread"], percent
    if "translate" in lower:
        return STATUSES["translated"], percent

    return DEFAULT_STATUS, percent


def compose_memoq_status(
    status_key: str,
    match_percent: Optional[int] = None,
    existing: Optional[str] = None,
) -> str:
    """Compose a memoQ status string, preserving existing text when provided."""
    if existing and existing.strip():
        return existing.strip()

    status_def = get_status(status_key)
    base = status_def.memoq_label
    if match_percent is not None:
        return f"{base} ({match_percent}%)"
    return base


