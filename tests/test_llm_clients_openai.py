"""Guard the OpenAI model list and how its models are called (modules/llm_clients.py).

Michael's rule (2026-10-07): the OpenAI list holds the best and latest three -
most expensive, middle, cheapest, in that order - and the middle one is the
default. The same three are in Supervertaler for Trados and for memoQ
(OpenAiModelTests in the plugins' shared core). All three reason on every
request, so they must be sent no temperature: an explicit one is refused.
"""

from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.llm_clients import LLMClient
from modules.llm_pricing import estimate_cost

THE_THREE = ["gpt-6-astra", "gpt-6.1-sol", "gpt-6-luna"]


def test_the_list_is_astra_sol_luna_most_capable_first():
    assert list(LLMClient.OPENAI_MODELS) == THE_THREE


def test_the_default_is_the_middle_pick_not_the_first():
    assert LLMClient.DEFAULT_MODELS["openai"] == "gpt-6.1-sol"
    assert LLMClient(api_key="x", provider="openai").model == "gpt-6.1-sol"


def test_openrouter_offers_the_same_three_and_no_gpt_5_4():
    ids = [m for m in LLMClient.OPENROUTER_MODELS if m.startswith("openai/")]
    assert ids == ["openai/" + m for m in THE_THREE]


@pytest.mark.parametrize("provider, model", [
    *[("openai", m) for m in THE_THREE],
    *[("openrouter", "openai/" + m) for m in THE_THREE],
    ("openai", "gpt-6-sol"),        # typed in: still a reasoning model
    ("openai", "gpt-5.6-terra"),    # a saved GPT-5.6 keeps working
])
def test_reasoning_models_are_sent_no_temperature(provider, model):
    client = LLMClient(api_key="x", provider=provider, model=model)
    assert client.temperature is None, f"{model} would be sent a temperature"


def test_a_non_reasoning_model_keeps_its_temperature():
    client = LLMClient(api_key="x", provider="mistral", model="mistral-large-latest")
    assert client.temperature == 0.3


@pytest.mark.parametrize("model", THE_THREE + ["gpt-5.5", "gpt-5.4-mini"])
def test_listed_and_saved_openai_models_take_images(model):
    assert LLMClient.model_supports_vision("openai", model)


@pytest.mark.parametrize("model", THE_THREE + ["openai/" + m for m in THE_THREE])
def test_every_listed_openai_model_has_a_price(model):
    provider = "openrouter" if model.startswith("openai/") else "openai"
    assert estimate_cost(provider, model, 1_000_000, 0), f"{model} has no price"
