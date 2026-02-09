# CLOVA Market Watcher

## 🚀 프로젝트 개요 (Project Overview)
CLOVA Market Watcher는 LangChain과 Google Gemini를 활용하여 시장 트렌드를 자동으로 분석하고, 그 결과를 Notion 데이터베이스에 정리해주는 AI 에이전트 기반 프로젝트입니다. 기술, 비즈니스, 학술 분야의 최신 정보를 병렬적으로 수집 및 요약하여 효율적인 시장 인사이트를 제공합니다.

## ✨ 주요 기능 (Key Features)
- **AI 기반 시장 트렌드 분석**: Google Gemini 모델을 활용하여 다양한 시장 데이터를 분석합니다.
- **병렬 데이터 수집**: 기술, 비즈니스, 학술 분야별 전문 에이전트가 동시에 정보를 탐색합니다.
- **웹 검색 통합**: Tavily API를 통해 최신 웹 정보를 효과적으로 검색합니다.
- **자동 요약 및 보고**: 수집된 정보를 정형화된 JSON 형식으로 요약하고 보고서를 생성합니다.
- **Notion 연동**: 분석된 보고서를 사용자가 지정한 Notion 데이터베이스에 자동으로 적재하여 관리 편의성을 높입니다.

## ⚙️ 기술 스택 (Tech Stack)
- **Python**: 프로젝트의 주 개발 언어.
- **LangChain / LangGraph**: LLM 기반 애플리케이션 개발 프레임워크 및 에이전트 워크플로우 관리.
- **Google Gemini (via `langchain-google-genai`)**: 핵심 LLM으로 정보 분석 및 요약에 사용.
- **Tavily API**: 실시간 웹 검색 및 정보 수집.
- **Notion API (via `notion-client`)**: Notion 데이터베이스 연동.
- **`python-dotenv`**: 환경 변수 관리.

## 📦 설치 (Installation)

### 1. 저장소 복제 (Clone Repository)
```bash
git clone https://github.com/your-username/clova-market-watcher.git # 실제 저장소 URL로 변경하세요.
cd clova-market-watcher
```

### 2. 가상 환경 설정 (Setup Virtual Environment)
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. 의존성 설치 (Install Dependencies)
```bash
pip install -r requirements.txt
```

## 🔑 환경 변수 설정 (Environment Variables)
프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 다음 환경 변수들을 설정해야 합니다.

```dotenv
GOOGLE_API_KEY="YOUR_GOOGLE_GEMINI_API_KEY"
TAVILY_API_KEY="YOUR_TAVILY_API_KEY"
NOTION_TOKEN="YOUR_NOTION_INTEGRATION_TOKEN"
NOTION_DB_ID="YOUR_NOTION_DATABASE_ID"
```

- **`GOOGLE_API_KEY`**: Google AI Studio 또는 Google Cloud Platform에서 발급받을 수 있는 Gemini API 키.
- **`TAVILY_API_KEY`**: Tavily 웹사이트에서 발급받을 수 있는 API 키.
- **`NOTION_TOKEN`**: Notion 통합(Integration)을 생성하여 발급받을 수 있는 토큰. Notion 통합 생성 시 해당 데이터베이스에 접근 권한을 부여해야 합니다.
- **`NOTION_DB_ID`**: 데이터를 적재할 Notion 데이터베이스의 ID. 데이터베이스 URL에서 확인할 수 있습니다 (`https://www.notion.so/{YOUR_WORKSPACE}/{DATABASE_ID}?v=...`).

## ▶️ 실행 방법 (How to Run)
모든 설치 및 환경 변수 설정이 완료되었다면, 다음 명령어를 사용하여 프로젝트를 실행할 수 있습니다.

```bash
python main.py
```

실행이 완료되면, 설정된 Notion 데이터베이스에 분석된 시장 보고서가 자동으로 적재됩니다.

## 📝 Notion 데이터베이스 설정 (Notion Database Setup)
`CLOVA Market Watcher`가 정상적으로 데이터를 적재하려면, Notion 데이터베이스에 다음 속성(Property)들이 정확히 설정되어 있어야 합니다.

| 속성 이름 | 타입 (Type) | 설명 |
| :------- | :----------- | :--- |
| `제목`     | `Title`      | 보고서의 제목이 들어갑니다. (필수) |
| `카테고리` | `Select`     | 보고서의 카테고리 (예: `기술동향`, `비즈니스`, `학술`). |
| `요약`     | `Rich text`  | 3줄 요약된 핵심 내용이 들어갑니다. |
| `중요도`   | `Select`     | 보고서의 중요도 (예: `★★★`, `★★`, `★`). |
| `URL`      | `URL`        | 원본 기사나 자료의 링크가 들어갑니다. |

`카테고리`와 `중요도` 속성의 `Select` 옵션들은 스크립트에서 예상하는 값들과 일치하도록 미리 설정해두는 것이 좋습니다. (예: `카테고리`에 "기술동향", "비즈니스", "학술" 옵션 추가, `중요도`에 "★★★", "★★", "★" 옵션 추가).
<img width="1150" height="273" alt="image" src="https://github.com/user-attachments/assets/d23e896c-4eb5-4215-b1c3-26c1e51849a0" />

