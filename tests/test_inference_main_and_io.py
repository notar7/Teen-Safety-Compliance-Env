import importlib
import json



def _load_inference_module(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "updated-key-123")
    mod = importlib.import_module("inference")
    return importlib.reload(mod)


def test_fallback_action_shape(monkeypatch):
    inf = _load_inference_module(monkeypatch)
    action = inf._fallback_action("x")
    assert action["decision"] == "escalate"
    assert action["confidence"] == 0.5
    assert "reason" in action


def test_safe_action_valid_round_trip(monkeypatch):
    inf = _load_inference_module(monkeypatch)
    action = inf._safe_action(
        {
            "decision": "restrict",
            "confidence": 0.72,
            "reason": "Potential policy risk for minors.",
            "additional_action": "add_warning_label",
        }
    )
    assert action.decision == "restrict"
    assert action.confidence == 0.72
    assert action.additional_action == "add_warning_label"


def test_get_agent_action_passes_chat_parameters(monkeypatch):
    inf = _load_inference_module(monkeypatch)

    captured = {}

    class DummyResponse:
        def __init__(self):
            msg = type("Msg", (), {"content": '{"decision":"allow","confidence":0.6,"reason":"ok reason","additional_action":null}'})
            choice = type("Choice", (), {"message": msg})
            self.choices = [choice]

    class DummyClient:
        def __init__(self):
            self.chat = type("Chat", (), {"completions": self})

        def create(self, **kwargs):  # noqa: ANN003
            captured.update(kwargs)
            return DummyResponse()

    monkeypatch.setattr(inf, "client", DummyClient())

    obs = {
        "case_id": "T1_001",
        "task_id": "task1_easy",
        "instructions": "review",
        "content": {"text": "x"},
        "user_profile": {"declared_age": 15},
        "platform_context": "instagram",
        "previous_actions": [],
        "step_number": 0,
    }

    out = inf.get_agent_action(obs)
    assert out["decision"] == "allow"
    assert captured["model"] == inf.MODEL_NAME
    assert captured["temperature"] == 0.1
    assert captured["max_tokens"] == 512


def test_main_writes_results_file_and_returns_payload(monkeypatch, tmp_path):
    inf = _load_inference_module(monkeypatch)

    calls = []

    def fake_run_task(_env, task_id, num_episodes=3):  # noqa: ANN001
        calls.append((task_id, num_episodes))
        base = {"task1_easy": 0.9, "task2_medium": 0.7, "task3_hard": 0.5}[task_id]
        return {"task_id": task_id, "avg_score": base, "episode_scores": [base, base, base]}

    monkeypatch.setattr(inf, "run_task", fake_run_task)

    times = iter([1000.0, 1010.0])
    monkeypatch.setattr(inf.time, "time", lambda: next(times))

    monkeypatch.chdir(tmp_path)
    result = inf.main()

    assert calls == [
        ("task1_easy", 3),
        ("task2_medium", 3),
        ("task3_hard", 3),
    ]
    assert result["overall_avg"] == 0.7
    assert result["runtime_secs"] == 10.0

    output_file = tmp_path / "baseline_results.json"
    assert output_file.exists()
    data = json.loads(output_file.read_text(encoding="utf-8"))
    assert data["overall_avg"] == 0.7
    assert data["tasks"]["task1_easy"]["avg_score"] == 0.9


def test_main_result_shape(monkeypatch, tmp_path):
    inf = _load_inference_module(monkeypatch)

    monkeypatch.setattr(
        inf,
        "run_task",
        lambda _env, task_id, num_episodes=3: {
            "task_id": task_id,
            "avg_score": 0.6,
            "episode_scores": [0.6] * num_episodes,
        },
    )
    monkeypatch.setattr(inf.time, "time", lambda: 1000.0)
    monkeypatch.chdir(tmp_path)

    out = inf.main()
    assert "model" in out
    assert "api_base" in out
    assert "tasks" in out and set(out["tasks"].keys()) == {"task1_easy", "task2_medium", "task3_hard"}
    assert isinstance(out["overall_avg"], float)
