import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from tavily import TavilyClient

from dotenv import load_dotenv  # <--- [추가] 1. 이걸 추가하고
load_dotenv()                   # <--- [추가] 2. 바로 실행해서 키부터 읽게 해야 합니다!

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from tavily import TavilyClient


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0) 
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# ... (밑에 있는 search_tavily 함수부터는 그대로 두시면 됩니다)
# 1. 도구 초기화
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0) # 무료 모델 중 성능 최강
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# 2. 검색 함수 (Tavily)
def search_tavily(query, topic):
    print(f"   [{topic}] 검색 중: {query}...")
    # Tavily의 고급 검색 기능 활용 (답변 품질 향상)
    results = tavily.search(
        query=query, 
        topic="news", 
        days=1,       # 지난 24시간 뉴스만
        search_depth="advanced",
        max_results=3 # 상위 3개만
    )
    # 검색 결과에서 제목과 내용, URL만 뽑기
    context = []
    for r in results['results']:
        context.append(f"- 제목: {r['title']}\n- 내용: {r['content']}\n- 링크: {r['url']}")
    
    return "\n\n".join(context)

# 3. 에이전트 노드 정의

def tech_agent(state):
    print("🚀 [Tech Agent] 기술 동향 조사 시작...")
    query = "latest AI technology trends LLM detailed tech crunch"
    search_result = search_tavily(query, "Tech")
    return {"tech_data": search_result}

def biz_agent(state):
    print("💼 [Biz Agent] 비즈니스 사례 조사 시작...")
    # ★핵심: 단순 뉴스 제외, 실제 도입 사례 위주 검색
    query = "Generative AI enterprise use cases success stories ROI efficiency"
    search_result = search_tavily(query, "Business")
    return {"biz_data": search_result}

def academic_agent(state):
    print("🎓 [Academic Agent] 최신 논문 조사 시작...")
    query = "top trending AI research papers arxiv huggingface daily"
    search_result = search_tavily(query, "Academic")
    return {"paper_data": search_result}

def summarizer_node(state):
    print("📝 [Supervisor] 정보 취합 및 최종 요약 중...")
    
    # 3명의 에이전트가 가져온 데이터를 하나로 합침
    tech = state.get("tech_data", "")
    biz = state.get("biz_data", "")
    paper = state.get("paper_data", "")

    # Gemini에게 최종 리포트 작성을 요청
    prompt = f"""
    당신은 'CLOVA Market Watcher'의 수석 분석가입니다.
    아래 수집된 정보를 바탕으로 노션에 적재할 수 있는 깔끔한 리포트를 작성해주세요.
    
    [수집된 정보]
    1. 기술 동향: {tech}
    2. 비즈니스 사례: {biz}
    3. 학술 연구: {paper}

    [작성 규칙]
    - 각 분야별로 가장 중요한 뉴스 1개씩만 선정하세요 (총 3개).
    - 한국어로 작성하세요.
    - 내용은 '3줄 요약' 형태로 핵심만 간결하게 쓰세요.
    - 결과는 반드시 아래와 같은 Python List[Dict] 형식의 JSON 문자열로만 출력하세요. (마크다운 없이)
    
    [
      {{
        "category": "기술동향",
        "title": "뉴스 제목",
        "summary": "3줄 핵심 요약 내용...",
        "link": "원본 기사 링크",
        "importance": "★★★"
      }},
      ... (비즈니스, 학술 포함 총 3개)
    ]
    """
    
    response = llm.invoke(prompt)
    
    # JSON 문자열만 깔끔하게 추출 (전처리)
    content = response.content.replace("```json", "").replace("```", "").strip()
    return {"final_report": content}