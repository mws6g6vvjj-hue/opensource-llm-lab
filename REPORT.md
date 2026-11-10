# 오픈소스 LLM 설치 및 실행 — Qwen2.5

# 교수님용 프로그램 바로 실행

## [▶ 설치 없이 대화 프로그램 실행하기](https://mws6g6vvjj-hue.github.io/opensource-llm-lab/)

1. 위 실행 링크를 누른다.
2. **모델 불러오기**를 누르고 준비가 끝날 때까지 기다린다.
3. 질문을 입력하고 **보내기**를 누른다.

Python·Ollama 설치, 로그인, API 키 입력 없이 사용할 수 있다. 최신 PC용 Chrome 또는 Edge를 권장한다. 첫 실행에는 약 786MB의 모델 파일과 실행 도구를 인터넷으로 불러오므로 PC와 네트워크에 따라 수 분이 걸릴 수 있다. 모델이 브라우저 캐시에 남으면 다음 실행은 빨라질 수 있다.

**Notion 안에서 실행 화면 보기**

[웹 프로그램 열기](https://mws6g6vvjj-hue.github.io/opensource-llm-lab/)

임베드 화면이 표시되지 않거나 모델 준비가 멈추면 위 **프로그램 실행 링크로 새 창을 열어** 이용한다. GPU가 지원되지 않는 환경에는 호환 모드(CPU)를 제공한다.

| 구분 | 교수님용 웹 실습 | PC 설치 실습 |
| --- | --- | --- |
| 실행 위치 | 교수님 브라우저 | 설치한 Windows PC |
| 모델 | Qwen2.5 0.5B Instruct, ONNX | Qwen2.5 1.5B Instruct, Ollama |
| 실행 도구 | Transformers.js 3.8.1 | Ollama 0.40.16 + Python |
| 설치·로그인 | 필요 없음 | Python 및 Ollama 준비 |
| 입력 전달 | 브라우저 내부 모델 | PC의 로컬 API |
| 결과 | 직접 질문해 확인 | 아래에 기록한 실측 결과 |

아래 PC 실습의 1.5B 답변과 소요 시간을 웹의 0.5B 성능으로 해석하지 않는다. 웹 버전도 실제 언어 모델이 답변을 생성하며, 한국어 문장과 사실 설명에 오류가 있을 수 있다. 일반 대화는 페이지의 메모리에만 유지되고 대화 초기화 또는 새로고침 시 사라진다.

**웹 구현 출처:** [ONNX 모델](https://huggingface.co/onnx-community/Qwen2.5-0.5B-Instruct), [Qwen 원본 모델](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct), [Transformers.js 공식 문서](https://huggingface.co/docs/transformers.js), [양자화 실행 예제](https://huggingface.co/docs/transformers.js/guides/dtypes), [GitHub Pages 배포 문서](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

---

**파이썬 기반 오픈소스 LLM 대화 프로그램**

`chat.py` · `setup.ps1` · `start.ps1`

**선택 모델:** Qwen2.5-1.5B-Instruct / Ollama `qwen2.5:1.5b`

[공식 모델 배포 페이지](https://ollama.com/library/qwen2.5:1.5b)

[GitHub 저장소](https://github.com/mws6g6vvjj-hue/opensource-llm-lab) · [Notion 설명서](https://app.notion.com/p/4143a9f958b980c38daee3fd020c7af7)

아래 코드 분석과 실행 기록은 실제 프로그램 실행을 기준으로 작성하였다.

---

## <b>목차</b>

- 오픈소스 LLM과 Ollama의 정의
- 프로그램 코드 분석
- 오픈소스 LLM 설치 및 프로그램 사용법
- 대화 테스트 결과 및 해석
- Qwen2.5 한국어 대화 프로그램 실습
- 모델 실행 결과 비교 및 한계
- 참고자료 및 출처



---

# 오픈소스 LLM과 Ollama의 정의

LLM(Large Language Model)은 많은 텍스트를 학습하여 입력 문맥에 이어질 문장을 생성하는 대규모 언어 모델이다. 사용자의 질문과 이전 대화를 입력받아 설명, 번역, 글쓰기 등의 응답을 생성할 수 있다.

공개 모델을 사용할 때에는 모델 가중치, 실행 코드, 학습 데이터가 각각 어느 범위까지 공개되었는지와 라이선스가 허용하는 사용 범위를 구분해야 한다. 가중치를 내려받을 수 있다는 사실만으로 학습 데이터 전체가 공개되거나 모든 활용이 제한 없이 허용되는 것은 아니다.

본 과제는 Apache 2.0 라이선스로 제공되는 **Qwen2.5-1.5B-Instruct**를 선택하였다. Ollama 배포본은 약 1.54B 파라미터의 모델을 Q4_K_M 방식으로 양자화한 버전이다. 모델의 크기와 라이선스는 [Qwen 공식 모델 카드](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct) 및 [Ollama 모델 정보](https://ollama.com/library/qwen2.5:1.5b)를 확인하였다.

Ollama는 모델을 PC에서 실행하고 프로그램이 호출할 수 있는 로컬 API를 제공하는 실행 도구이다. 본 프로그램은 Python에서 로컬 서버에 요청을 보내고, 서버가 Qwen2.5 모델로 답변을 생성하도록 구성하였다. [출처: Ollama Windows 문서](https://docs.ollama.com/windows)

| 구분 | Qwen2.5 모델 | Ollama | Python 대화 프로그램 |
| --- | --- | --- | --- |
| 역할 | 문장을 생성하는 언어 모델 | 모델 실행과 API 제공 | 사용자 입력 및 답변 출력 |
| 주요 구성 | 학습된 가중치 | 로컬 서버와 실행 도구 | `chat.py` |
| 본 과제 설정 | `qwen2.5:1.5b` | 0.40.16 | Python 3.9.0 |
| 대화 기록 처리 | 전달받은 문맥을 이용 | 요청을 받아 추론 실행 | 이전 대화를 목록으로 유지 |

**전체 실행 흐름**

사용자 질문 → Python 대화 이력에 추가 → Ollama Chat API 호출 → Qwen2.5 답변 생성 → 대화 이력에 답변 저장 → 화면 출력



---

# 프로그램 코드 분석

## 1. 라이브러리 불러오기

```python
import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path
```

프로그램에 필요한 Python 표준 라이브러리를 불러오는 부분이다.

- **argparse:** 일반 대화 모드와 테스트 모드 구분.
- **json:** 요청과 응답 데이터를 JSON으로 변환.
- **urllib.request / urllib.error:** 로컬 서버 통신 및 연결 오류 처리.
- **time:** 실제 요청 소요 시간 측정.
- **datetime / pathlib:** 한국 시간 기록 및 결과 파일 저장.
- **sys:** 실행 실패 메시지와 종료 상태 처리.

별도의 Python 패키지를 설치하지 않고 표준 라이브러리로 구성하였다. HTTP 요청에 사용하는 기능은 [Python urllib.request 공식 문서](https://docs.python.org/3.9/library/urllib.request.html)를 참고하였다.



## 2. 모델과 서버 주소 설정

```python
BASE_URL = "http://127.0.0.1:11434"
MODEL = "qwen2.5:1.5b"
SYSTEM = "당신은 친절한 한국어 도우미입니다. 질문에 정확하고 간결한 한국어로 답하세요."
```

- `BASE_URL`: PC 내부에서 실행하는 Ollama 서버 주소.
- `MODEL`: 요청에 사용할 모델 이름.
- `SYSTEM`: 모델의 답변 언어와 응답 방식을 지정하는 지시문.

시스템 지시문을 작성해도 모든 답변의 정확성이나 형식 준수가 보장되지는 않는다. 실제 테스트에서 문장 수를 지키지 못하는 사례가 있었다.



## 3. API 요청 함수 구현

### 3-1. 요청 데이터 변환

```python
data = None if payload is None else json.dumps(
    payload, ensure_ascii=False
).encode("utf-8")
```

Python 객체를 JSON으로 바꾸고 UTF-8 바이트로 변환한다. `ensure_ascii=False`를 사용해 한국어를 그대로 표현한다.

### 3-2. 서버 요청과 응답 읽기

```python
req = urllib.request.Request(
    BASE_URL + path,
    data=data,
    headers={"Content-Type": "application/json"}
)
with urllib.request.urlopen(req, timeout=300) as response:
    return json.load(response)
```

요청 데이터와 JSON 형식의 헤더를 전달한다. 응답이 오면 JSON을 Python 객체로 읽는다. 최대 대기 시간은 300초로 설정하였다. [출처: Python urllib.request](https://docs.python.org/3.9/library/urllib.request.html)



## 4. 대화 요청과 생성 조건 설정

```python
def ask(messages):
    return api("/api/chat", {
        "model": MODEL,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0,
            "seed": 42,
            "num_ctx": 4096,
            "num_predict": 512
        }
    })
```

`messages` 배열에는 시스템 지시, 사용자 질문, 이전 모델 답변을 담는다. `stream=False`로 설정하여 응답이 완성되면 한 번에 받아 출력한다. Chat API의 요청과 응답 구조는 [Ollama 공식 Chat API 문서](https://docs.ollama.com/api/chat)를 참고하였다.

| 설정 | 본 과제 값 | 용도 |
| --- | --- | --- |
| `temperature` | 0 | 답변 생성의 무작위성 억제 |
| `seed` | 42 | 재현성을 위한 고정 시드 |
| `num_ctx` | 4096 | 요청에서 활용할 문맥 길이 설정 |
| `num_predict` | 512 | 최대 생성 토큰 수 제한 |
| `stream` | False | 완성된 응답을 한 번에 수신 |

같은 설정이라도 실행 환경과 모델 버전에 따라 결과가 달라질 수 있다.



## 5. 대화 이력과 답변 출력

```python
history = [{"role": "system", "content": SYSTEM}]
history.append({"role": "user", "content": prompt})
response = ask(history)
history.append(response["message"])
print("Qwen2.5:", response["message"]["content"])
```

사용자 질문을 대화 목록에 추가한 후, 목록 전체를 모델에 전달한다. 응답도 같은 목록에 추가하여 다음 질문에서 이전 대화를 참조할 수 있도록 한다.

이 방식은 프로그램이 이전 문장을 다시 전달하는 구조이며, 모델의 영구 기억이나 재학습을 뜻하지 않는다.



## 6. 대화 초기화와 종료

```python
if prompt == "/exit":
    return
if prompt == "/reset":
    history = history[:1]
    print("대화를 초기화했습니다.")
    continue
```

`/exit`는 대화 프로그램을 종료한다. `/reset`은 첫 시스템 지시문만 남기고 이전 사용자 질문과 모델 답변을 지운다.



## 7. 실행 시간과 결과 저장

```python
started = time.perf_counter()
response = ask(history)
elapsed = time.perf_counter() - started
seconds = response.get("eval_duration", 0) / 1e9
```

실제 요청 시간은 `time.perf_counter()`로 측정한다. 생성 속도는 응답에 포함된 생성 토큰 수와 생성 시간을 이용하여 계산한다.

$$
\text{생성 속도(token/s)} = \frac{\text{eval\_count}}{\text{eval\_duration}/10^9}
$$

`eval_duration`과 `eval_count`의 의미는 [Ollama Chat API의 응답 항목](https://docs.ollama.com/api/chat)에 따른다. 전체 응답 시간과 토큰 생성 시간은 서로 다른 수치이다.

```python
destination = Path(__file__).parent / "results" / "test-results.json"
destination.parent.mkdir(exist_ok=True)
destination.write_text(
    json.dumps(result, ensure_ascii=False, indent=2),
    encoding="utf-8"
)
```

실제 입력, 모델 응답, 실행 조건, 소요 시간, 모델 식별 정보를 결과 파일에 저장한다. 모델 답변의 내용이 맞는지는 별도로 검토한다.



---

# 오픈소스 LLM 설치 및 프로그램 사용법

## 실행 환경

| 항목 | 확인 결과 |
|---|---|
| 운영체제 | Windows 10 Pro, 10.0.19045 |
| CPU | Intel Core i7-10700F |
| 메모리 | 약 32GB |
| GPU | NVIDIA GeForce RTX 3070, 8GB |
| Python | 3.9.0 |
| Ollama | 0.40.16 |
| 모델 | qwen2.5:1.5b, 약 1.54B, Q4_K_M |
| 모델 다운로드 크기 | 986,061,892바이트 |
| 모델 라이선스 | Apache 2.0 |

모델 식별 digest: `65ec06548149b04c096a120e4a6da9d4017ea809c91734ea5631e89f96ddc57b`

실행일: 2026년 11월 10일 (한국 시간).

## 1. 실행 도구와 모델 설치

공식 Ollama 배포본을 다운로드하고 SHA-256을 확인한 뒤 과제 폴더에 설치하였다. 모델은 `.runtime/models`에 저장하고 서버는 `127.0.0.1:11434`에서 실행하였다. [출처: Ollama Windows 설치 문서](https://docs.ollama.com/windows)

```powershell
powershell -ExecutionPolicy Bypass -File .\setup.ps1
powershell -ExecutionPolicy Bypass -File .\start.ps1
```

- `setup.ps1`: 공식 배포본 다운로드, 해시 검증 및 압축 해제.
- `start.ps1`: 서버 시작, 모델이 없으면 다운로드, 대화 프로그램 실행.

설치 파일 SHA-256: `50fcf5ad54277f2fa5d173ebfc93bcb017adbc0c9ef2314daabc96ca9e6aa64e`

처음 실행할 때는 인터넷 연결과 설치 파일·모델을 저장할 공간이 필요하다. Python은 별도로 준비되어 있어야 한다. 모델 다운로드 명령은 다음과 같다. [출처: 모델 배포 페이지](https://ollama.com/library/qwen2.5:1.5b)

```powershell
ollama pull qwen2.5:1.5b
```

## 2. 프로그램 사용

Python 3.9 이상이 설치된 Windows에서 저장소 폴더를 연다.

```powershell
powershell -ExecutionPolicy Bypass -File .\setup.ps1
powershell -ExecutionPolicy Bypass -File .\start.ps1
```

질문을 입력하면 모델의 답변이 출력된다. `/reset`은 대화 이력 초기화, `/exit`는 대화 프로그램 종료이다. 대화 프로그램을 종료해도 Ollama 서버는 백그라운드에서 실행된다.

설치와 모델 다운로드에는 인터넷이 필요하다. 이후 대화는 로컬 서버에 전달된다. 별도 API 키는 사용하지 않는다. 일반 대화 이력은 프로그램 메모리에만 보관하며, 테스트 모드에서는 입력과 응답을 결과 파일로 저장한다.

## 3. 주요 파일

- `chat.py`: 로컬 API 호출, 대화 이력 유지, 초기화와 종료, 테스트 결과 저장.
- `setup.ps1`: 공식 배포본 다운로드, 해시 확인, 압축 해제.
- `start.ps1`: 서버 실행, 모델 다운로드, 대화 또는 테스트 시작.
- `environment.json`: 확인한 실행 환경.
- `results/test-results.json`: 최종 테스트의 요청, 응답, 수치 원본.
- `results/initial-results.json`: 최초 Qwen3 테스트 기록.
- `.gitignore`: 실행 파일, 모델, 임시 로그가 GitHub에 올라가지 않도록 제외.

API는 `POST http://127.0.0.1:11434/api/chat`이며 모델 이름과 role/content 형태의 대화 이력을 전달한다. Python의 urllib과 json을 사용해 추가 패키지 없이 동작한다. 실행 모델의 size_vram과 size가 동일하게 보고되어 GPU에 적재된 상태를 확인했다.



---

# 대화 테스트 결과 및 해석

## 테스트 조건 및 측정 결과

```powershell
powershell -ExecutionPolicy Bypass -File .\start.ps1 -Test
```

설정은 temperature=0, seed=42, num_ctx=4096, num_predict=512이다. 시나리오별 대화 이력을 분리하고, 문맥 테스트에서는 두 요청에 걸쳐 같은 대화 이력을 전달했다.

| 테스트 | 소요 시간 | 생성 속도 | 평가 |
|---|---:|---:|---|
| 한국어 인사 | 3.263초 | 142.39 token/s | 한국어 응답 성공, 두 문장 조건 불충족 |
| 개념 설명 | 0.862초 | 137.31 token/s | 부정확한 설명, 세 문장 조건 불충족 |
| 사과 계산 | 0.104초 | 129.05 token/s | 정답 5개 |
| 암호 전달 | 0.061초 | 186.65 token/s | 암호를 포함한 응답 |
| 암호 재질문 | 0.084초 | 86.31 token/s | 이전 암호 기억 성공 |

모든 요청은 stop 사유로 정상 완료됐다. 시간은 단일 실행 측정값으로 첫 요청에는 모델 로딩이 포함된다. 생성 속도는 API의 eval_count / eval_duration으로 계산하며 전체 응답 시간과 다르다. 짧은 답변의 token/s는 편차가 크므로 일반적인 성능 수치로 해석하지 않는다.

### 한국어 인사

입력: 안녕하세요! 당신이 할 수 있는 일을 한국어 두 문장으로 소개해 주세요.

실제 응답:
> 안녕하세요! 저는 친절하고 도움을 드릴 수 있는 한국어 도우미입니다. 질문에 대해 정확하고 간결하게 답변해 드리겠습니다.

평가: 한국어 대화는 가능했다. 인사말을 포함해 문장 종결이 세 번 있으므로 두 문장 지시를 엄밀히 충족하지 못했다.

### 개념 설명

입력: 오픈소스 LLM이 무엇인지 초보자에게 한국어 세 문장으로 설명해 주세요.

실제 응답:
> 오픈소스 LLM은 공개로 제공되는 모델입니다. 이 모델은 누구나 사용할 수 있으며, 특정 기능이나 특징을 제공하지 않습니다. 대신, 사용자는 모델을 개선하거나 향상시키는 데 필요한 정보를 제공해야 합니다. 오픈소스 LLM은 학습 데이터를 공개하고, 사용자들이 모델을 개선하는 데 필요한 정보를 제공합니다. 이는 모델 개발에 중요한 역할을 합니다.

평가: 부정확하다. ‘특정 기능이나 특징을 제공하지 않는다’는 설명은 적절하지 않으며, 모델이 공개되어 있다고 학습 데이터까지 항상 공개되는 것은 아니다. 요청한 세 문장도 지키지 못했다. 모델 응답을 사실로 그대로 사용하면 안 된다는 한계를 확인했다.

보완 설명: LLM은 대량의 텍스트를 학습해 문장을 생성하는 언어 모델이다. 공개 모델은 제공된 가중치와 코드 및 각 라이선스 조건에 따라 로컬 실행이나 활용이 가능하다. 가중치 공개, 학습 데이터 공개, 자유로운 재배포 허용 여부는 별도로 확인해야 한다.

### 간단한 계산

입력: 사과가 3개 있고 2개를 더 받았습니다. 사과는 모두 몇 개인가요? 한 문장으로 답하세요.

실제 응답:
> 사과는 5개입니다.

평가: 3+2=5로 정답이며 한 문장 지시도 충족했다.

### 대화 문맥 유지

첫 입력: 이번 대화에서 기억할 암호는 파란고래입니다. 암호를 기억했다고 짧게 답하세요.

첫 응답:
> 파란고래

후속 입력: 방금 내가 알려 준 암호는 무엇인가요? 암호만 답하세요.

후속 응답:
> 파란고래

평가: 이전 발화를 포함한 messages 배열을 다시 전달하자 암호를 정확히 재현했다. 프로그램이 대화 이력을 관리한 결과이며 영구 기억이나 모델 재학습을 의미하지 않는다.



---

# <b>Qwen2.5 한국어 대화 프로그램 실습</b>

**주요 기능**

1. 한국어 질문 입력과 답변 출력.
2. 이전 대화 이력을 활용한 후속 질문.
3. `/reset`으로 대화 초기화.
4. `/exit`로 대화 프로그램 종료.
5. 테스트 모드로 요청과 응답 원본 및 실행 수치 저장.
6. 서버 연결 오류 발생 시 안내 출력.

**프로그램 특징**

- Python 표준 라이브러리로 구현.
- Ollama를 통해 PC에서 모델 실행.
- 별도 유료 API 키 없이 실습.
- 일반 대화 이력은 실행 중 메모리에만 유지.
- 테스트 모드의 입력과 응답은 파일에 저장.
- PC용 터미널 프로그램과 별도로 설치 없이 이용하는 웹 대화 프로그램을 제공한다.

**활용 예시**

- 일상적인 한국어 질의응답.
- 간단한 계산과 문장 생성 실습.
- 대화 이력 전달 방식 학습.
- 모델 답변의 지시 준수 여부와 사실 정확성 비교.

**실습 순서**

1. **프로그램 준비:** Python을 확인한 후 설치와 실행 명령을 수행한다.
2. **첫 질문 입력:** 간단한 인사나 설명 질문을 입력한다.
3. **후속 질문 입력:** 이전 발화의 내용을 다시 물어 문맥 유지 여부를 확인한다.
4. **대화 초기화:** `/reset`을 입력해 이전 대화를 지운다.
5. **테스트 실행:** `start.ps1 -Test`를 실행하고 결과 파일을 확인한다.
6. **내용 평가:** 답변 출력 여부, 정답 여부, 한국어 표현, 문장 수 조건을 각각 확인한다.

실습 입력 예시는 앞 절의 실제 테스트 입력과 같다. ‘파란고래’는 기억 여부 확인용 예제 문자열이며 실제 비밀번호가 아니다.



---

# 모델 실행 결과 비교 및 한계

## Qwen3와 Qwen2.5의 실행 관찰 비교

| 항목 | 처음 시도한 Qwen3 4B | 최종 선택한 Qwen2.5 1.5B |
| --- | --- | --- |
| 모델 이름 | `qwen3:4b` | `qwen2.5:1.5b` |
| 본 환경의 관찰 | 추론 문장이 길게 섞이고 일부 응답이 길이 제한으로 종료 | 테스트 5회 모두 stop 사유로 완료 |
| 간단한 대화 실습 | 최종 답변만 간결하게 받는 데 문제 발생 | 한국어 응답·계산·문맥 유지 확인 |
| 결과 원본 | `results/initial-results.json` | `results/test-results.json` |
| 최종 프로그램 사용 | 사용하지 않음 | 사용함 |

처음에는 Qwen3의 think 설정과 프롬프트, 대화 템플릿을 점검했으나 이 환경에서 문제가 반복되어 Qwen2.5로 바꾸었다. 위 표는 동일 조건의 정식 성능 비교가 아니라 **실제 설치 과정에서 관찰한 실행 결과**이다. Qwen3 전체의 성능이 낮다고 일반화할 수 없다.

### 분석 결과

최종 모델은 한국어 응답을 생성했고, 3+2 계산과 이전 암호 재현에 성공하였다. 그러나 문장 수 조건을 엄밀히 따르지 못했고, 오픈소스 LLM 설명에서는 잘못된 정보를 생성하였다. 따라서 서버 실행과 대화 기능의 정상 동작을 답변 정확성 보장으로 해석해서는 안 된다.

### 문제 해결

연결 오류가 나면 `start.ps1`을 먼저 실행하고 `logs/ollama-error.log`를 확인한다. 모델 다운로드 실패 시 네트워크와 디스크 공간을 확인한다. 다른 Ollama 서버가 11434 포트에서 실행 중이면 기존 서버의 버전과 모델 저장 경로가 사용된다.

이 과제의 확인 범위는 간단한 대화 가능 여부다. 지식 정확성, 복잡한 추론, 모든 한국어 지시 준수까지 검증한 것은 아니다. GitHub Pages를 통해 docs 폴더의 웹 프로그램을 공개한다.

### 결론

Ollama와 Qwen2.5를 설치하고 Python 프로그램에서 한국어 대화를 실행하여 과제의 기본 목표를 확인하였다. 대화 이력을 전달하면 후속 질문에 이전 내용을 활용할 수 있었으며, 실제 응답 원문과 측정 수치를 저장하였다. 동시에 작은 언어 모델의 사실 정확성과 지시 준수 한계를 확인하였다.



---

# 참고자료 및 출처

## 모델과 실행 도구

| 번호 | 자료 | 본문에서 참고한 내용 |
| --- | --- | --- |
| 1 | [Qwen 공식 — Qwen2.5-1.5B-Instruct 모델 카드](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct) | 모델 식별, 파라미터 규모, 라이선스, 대화 모델 사용법 |
| 2 | [Ollama — qwen2.5:1.5b](https://ollama.com/library/qwen2.5:1.5b) | 실제 실행 태그, 배포 크기, 양자화, 실행 명령 |
| 3 | [Ollama — Windows 공식 문서](https://docs.ollama.com/windows) | Windows 설치, 모델 저장 위치, 로컬 API |
| 4 | [Ollama — Chat API](https://docs.ollama.com/api/chat) | model/messages/stream 요청 구조, 응답과 생성 시간 항목 |
| 5 | [Ollama — v0.40.16 공식 릴리스](https://github.com/ollama/ollama/releases/tag/v0.40.16) | 설치한 버전과 Windows 배포 파일 |
| 6 | [Ollama — 소스 및 MIT 라이선스](https://github.com/ollama/ollama/blob/main/LICENSE) | 실행 도구의 라이선스 확인 |

## 프로그램 구현

| 번호 | 자료 | 참고 내용 |
| --- | --- | --- |
| 7 | [Python 3.9 — urllib.request](https://docs.python.org/3.9/library/urllib.request.html) | Request, urlopen, timeout을 이용한 HTTP 요청 |

## 직접 생성한 실습 자료

- **최종 테스트 데이터:** `results/test-results.json`. 한국어 인사, 개념 설명, 계산, 문맥 유지 등 직접 작성한 입력을 실제 모델에 전달하여 생성하였다.
- **초기 실행 데이터:** `results/initial-results.json`. Qwen3 설치 후 처음 수행한 테스트의 원문이다.
- **실행 환경:** `environment.json`. 해당 PC에서 확인한 운영체제, CPU, 메모리, GPU, Python, Ollama 정보이다.
- **구현 코드:** `chat.py`, `setup.ps1`, `start.ps1`. 본 실습용으로 작성한 프로그램이다.

테스트 문장과 실행 결과는 외부 OPEN DATA를 가져온 것이 아니므로 공공데이터 출처를 임의로 기재하지 않았다. 표의 응답 시간과 답변은 직접 실행한 결과이며 공식 문서의 성능 수치를 인용한 것이 아니다.

**서식 참고:** [선형회귀 및 비선형회귀 프로그램](https://app.notion.com/p/3ec3a9f958b98085a11dc269f21eebab). 목차, 큰 제목, 단계별 코드 설명, 사용법, 결과 해석, 비교 표의 구성을 참고하였다.

자료 확인일: 2026년 11월 10일.

---

**제출 상태:** 설치·대화 테스트·Notion 설명서 작성 완료. GitHub 저장소에 코드와 실행 결과를 제공한다. 평가자에게 제출할 때에는 이 페이지의 열람 권한을 확인한다.

