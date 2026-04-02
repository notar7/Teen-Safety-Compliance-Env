import importlib

from env.environment import TeenSafetyEnvironment


class _DummyResponse:
    def __init__(self, content: str):
        msg = type("Msg", (), {"content": content})
        choice = type("Choice", (), {"message": msg})
        self.choices = [choice]


class _DummyClient:
    def __init__(self, content: str = '{"decision":"restrict","confidence":0.7,"reason":"ok","additional_action":null}', exc: Exception | None = None):
        self._content = content
        self._exc = exc
        self.chat = type("Chat", (), {"completions": self})

    def create(self, **kwargs):  # noqa: ANN003
        if self._exc:
            raise self._exc
        return _DummyResponse(self._content)


def _load_inference_module():
    mod = importlib.import_module("inference")
    return importlib.reload(mod)


def test_inference_reads_updated_api_key(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "updated-key-123")
    inf = _load_inference_module()
    assert inf.OPENAI_API_KEY == "updated-key-123"


def test_safe_action_coercion():
    inf = _load_inference_module()
    action = inf._safe_action(
        {
            "decision": "BAD_DECISION",
            "confidence": "2.0",
            "reason": "",
            "additional_action": "unknown",
        }
    )
    assert action.decision == "escalate"
    assert action.confidence == 1.0
    assert action.reason == "No reason provided."
    assert action.additional_action is None


def test_get_agent_action_json_and_fallback_paths(monkeypatch):
    inf = _load_inference_module()
    env = TeenSafetyEnvironment(rng_seed=42)
    obs = env.reset("task1_easy").model_dump()

    monkeypatch.setattr(inf, "client", _DummyClient('{"decision":"allow","confidence":0.6,"reason":"ok reason","additional_action":null}'))
    parsed = inf.get_agent_action(obs)
    assert parsed["decision"] == "allow"

    monkeypatch.setattr(inf, "client", _DummyClient("text before {\"decision\":\"restrict\",\"confidence\":0.6,\"reason\":\"reason\",\"additional_action\":null} text"))
    extracted = inf.get_agent_action(obs)
    assert extracted["decision"] == "restrict"

    monkeypatch.setattr(inf, "client", _DummyClient("not json"))
    fallback = inf.get_agent_action(obs)
    assert fallback["decision"] == "escalate"

    monkeypatch.setattr(inf, "client", _DummyClient(exc=RuntimeError("api fail")))
    fallback2 = inf.get_agent_action(obs)
    assert fallback2["decision"] == "escalate"


def test_run_task_smoke(monkeypatch):
    inf = _load_inference_module()
    monkeypatch.setattr(inf, "get_agent_action", lambda _obs: {
        "decision": "restrict",
        "confidence": 0.7,
        "reason": "Potentially harmful for minors due to policy risk.",
        "additional_action": "add_warning_label",
    })
    monkeypatch.setattr(inf.time, "sleep", lambda _x: None)

    env = TeenSafetyEnvironment(rng_seed=42)
    result = inf.run_task(env, "task1_easy", num_episodes=1)
    assert result["task_id"] == "task1_easy"
    assert len(result["episode_scores"]) == 1
