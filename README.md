# 오픈소스 LLM 설치 및 실행 — Qwen2.5 1.5B

[Notion 실습 설명서](https://app.notion.com/p/4143a9f958b980c38daee3fd020c7af7) · [코드와 테스트 분석](REPORT.md)

Windows PC에 Ollama와 Qwen2.5 1.5B를 설치하고 Python 대화 프로그램으로 한국어 대화를 테스트하는 과제입니다. 테스트 원문과 실행 수치는 `results/test-results.json`, 상세 설명은 `REPORT.md`에 기록합니다.

## 구성

| 항목 | 내용 |
|---|---|
| 모델 | `qwen2.5:1.5b`, 약 1.54B 파라미터, Q4_K_M |
| 실행 도구 | Ollama v0.40.16 Windows 독립 실행 배포본 |
| 프로그램 | Python 3.9 이상, 표준 라이브러리만 사용 |
| 통신 | 로컬 `http://127.0.0.1:11434/api/chat` |
| 기능 | 한국어 대화, 대화 이력 유지, 초기화, 테스트 결과 저장 |

모델은 로컬 PC에서 실행합니다. 최초 설치와 모델 다운로드에는 인터넷이 필요합니다. 모델 파일과 실행 도구는 용량 때문에 GitHub에 포함하지 않습니다.

## 설치와 실행

Windows PowerShell에서 저장소 폴더를 연 뒤 실행합니다. Python은 별도 설치되어 있어야 합니다.

```powershell
powershell -ExecutionPolicy Bypass -File .\setup.ps1
powershell -ExecutionPolicy Bypass -File .\start.ps1
```

`setup.ps1`은 공식 GitHub 배포본을 `.runtime/ollama`에 설치합니다. `start.ps1`은 Ollama 서버를 시작하고 모델이 없으면 다운로드합니다. 실행 파일 약 1.6GB, 모델 약 1GB 외에 압축 해제 공간이 필요하므로 디스크 여유를 충분히 확보하세요.

대화창에서 질문을 입력합니다. `/reset`은 대화 초기화, `/exit`는 프로그램 종료입니다. 대화 프로그램을 종료해도 Ollama 서버는 백그라운드에서 계속 실행됩니다.

## 테스트 재현

```powershell
powershell -ExecutionPolicy Bypass -File .\start.ps1 -Test
```

한국어 인사, 개념 설명, 계산, 2회에 걸친 문맥 유지 테스트를 수행하고 `results/test-results.json`을 새 결과로 덮어씁니다. 실제 응답, 완료 사유, 생성 토큰 수, 시간, GPU 사용 정보를 저장합니다. 자동 실행 완료와 답변 내용의 정확성은 별도로 평가합니다.

대화 이력은 실행 중 메모리에만 유지되며 일반 대화는 파일로 저장하지 않습니다. 테스트 입력과 응답은 결과 파일에 저장됩니다. 테스트는 `temperature=0`, `seed=42`, `num_ctx=4096`, `num_predict=512`를 사용하며 환경이나 모델 버전에 따라 결과는 달라질 수 있습니다.

## 문제 해결

- 연결 오류: `start.ps1`을 먼저 실행하고 `logs/ollama-error.log`를 확인합니다.
- 모델 다운로드 실패: 인터넷 연결과 디스크 여유를 확인하고 `start.ps1`을 다시 실행합니다.
- 응답 지연 또는 메모리 부족: 다른 GPU 프로그램을 종료하거나 더 작은 모델을 검토합니다. 모델을 바꾸면 `chat.py`와 `start.ps1`의 이름을 함께 변경합니다.
- 포트 11434에서 다른 Ollama가 이미 실행 중이면 해당 서버를 사용합니다. 이 경우 모델 저장 경로와 서버 버전은 기존 서버 설정을 따릅니다.
- PowerShell 실행 정책 오류: 위 명령의 `-ExecutionPolicy Bypass`는 해당 실행에만 적용합니다.

## 라이선스와 출처

Qwen2.5 모델의 라이선스는 Apache 2.0, Ollama의 라이선스는 MIT입니다. 이 저장소는 해당 모델 가중치나 Ollama 실행 파일을 재배포하지 않습니다.

- [Ollama Windows 공식 문서](https://docs.ollama.com/windows)
- [Qwen2.5 1.5B Ollama 배포 정보](https://ollama.com/library/qwen2.5:1.5b)
- [Qwen2.5 1.5B 공식 모델 카드](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct)
- [Ollama Chat API](https://docs.ollama.com/api/chat)
- [Ollama 소스 및 라이선스](https://github.com/ollama/ollama)

GitHub에 올린 코드만으로 호스팅된 웹 대화 서비스가 생기지는 않습니다. 이 프로젝트는 PC에서 실행하는 대화 프로그램이며, 과제에는 Notion 보고서 또는 GitHub 저장소 URL을 활용할 수 있습니다.

