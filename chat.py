"""Qwen2.5 local chat: Python standard library only, no API key required."""
import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

BASE_URL = "http://127.0.0.1:11434"
MODEL = "qwen2.5:1.5b"
SYSTEM = "당신은 친절한 한국어 도우미입니다. 질문에 정확하고 간결한 한국어로 답하세요."


def api(path, payload=None):
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(BASE_URL + path, data=data,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as response:
        return json.load(response)


def ask(messages):
    return api("/api/chat", {"model": MODEL, "messages": messages,
               "stream": False,
               "options": {"temperature": 0, "seed": 42, "num_ctx": 4096, "num_predict": 512}})


def run_tests():
    """Record real outputs; semantic correctness is reviewed separately."""
    scenarios = [
        ("한국어 인사", ["안녕하세요! 당신이 할 수 있는 일을 한국어 두 문장으로 소개해 주세요."]),
        ("개념 설명", ["오픈소스 LLM이 무엇인지 초보자에게 한국어 세 문장으로 설명해 주세요."]),
        ("계산", ["사과가 3개 있고 2개를 더 받았습니다. 사과는 모두 몇 개인가요? 한 문장으로 답하세요."]),
        ("대화 문맥", ["이번 대화에서 기억할 암호는 파란고래입니다. 암호를 기억했다고 짧게 답하세요.",
                     "방금 내가 알려 준 암호는 무엇인가요? 암호만 답하세요."]),
    ]
    records = []
    for name, prompts in scenarios:
        history = [{"role": "system", "content": SYSTEM}]
        for prompt in prompts:
            history.append({"role": "user", "content": prompt})
            started = time.perf_counter()
            response = ask(history)
            elapsed = time.perf_counter() - started
            history.append(response["message"])
            seconds = response.get("eval_duration", 0) / 1e9
            record = {"test": name, "prompt": prompt, "response": response,
                      "wall_seconds": round(elapsed, 3),
                      "tokens_per_second": round(response.get("eval_count", 0) / seconds, 2) if seconds else None}
            records.append(record)
            print(name, "|", response["message"]["content"], flush=True)
    result = {"tested_at": datetime.now(timezone(timedelta(hours=9))).isoformat(),
              "version": api("/api/version"), "model": MODEL,
              "models": api("/api/tags"), "running_models": api("/api/ps"),
              "settings": {"temperature": 0, "seed": 42,
                           "num_ctx": 4096, "num_predict": 512}, "tests": records}
    destination = Path(__file__).parent / "results" / "test-results.json"
    destination.parent.mkdir(exist_ok=True)
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Saved:", destination)


def main():
    parser = argparse.ArgumentParser(description="Qwen2.5 한국어 로컬 대화")
    parser.add_argument("--test", action="store_true", help="실제 대화 테스트 결과 저장")
    args = parser.parse_args()
    if args.test:
        run_tests()
        return
    history = [{"role": "system", "content": SYSTEM}]
    print("Qwen2.5 1.5B 로컬 대화 | /exit 종료 | /reset 대화 초기화")
    while True:
        try:
            prompt = input("\n나: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n종료합니다.")
            return
        if prompt == "/exit":
            return
        if prompt == "/reset":
            history = history[:1]
            print("대화를 초기화했습니다.")
            continue
        if not prompt:
            continue
        history.append({"role": "user", "content": prompt})
        try:
            response = ask(history)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            history.pop()
            print("연결 오류: start.ps1로 Ollama를 먼저 실행하세요.", exc)
            continue
        history.append(response["message"])
        print("Qwen2.5:", response["message"]["content"])


if __name__ == "__main__":
    try:
        main()
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        print("실행 실패: start.ps1로 서버와 모델을 준비하세요.", exc, file=sys.stderr)
        sys.exit(1)
