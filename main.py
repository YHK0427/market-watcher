import os
import json
from dotenv import load_dotenv
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from notion_client import Client

# 방금 만든 에이전트들 가져오기
from nodes.agents import tech_agent, biz_agent, academic_agent, summarizer_node

# 1. 환경변수 로드
load_dotenv()

# 2. 상태(State) 정의 - 에이전트끼리 주고받을 데이터 주머니
class AgentState(TypedDict):
    tech_data: str      # 기술 에이전트가 조사한 내용
    biz_data: str       # 비즈니스 에이전트가 조사한 내용
    paper_data: str     # 학술 에이전트가 조사한 내용
    final_report: str   # 최종 요약된 JSON 데이터

# 3. 노션 적재 함수
def push_to_notion(state):
    print("💾 [Notion] 데이터베이스 적재 시작...")
    notion = Client(auth=os.getenv("NOTION_TOKEN"))
    db_id = os.getenv("NOTION_DB_ID")
    
    try:
        # 문자열로 된 리포트를 실제 리스트로 변환
        report_list = json.loads(state["final_report"])
        
        for item in report_list:
            notion.pages.create(
                parent={"database_id": db_id},
                properties={
                    "제목": {"title": [{"text": {"content": item["title"]}}]}, # 아까 찾은 '이름' 컬럼!
                    "카테고리": {"select": {"name": item["category"]}},
                    "요약": {"rich_text": [{"text": {"content": item["summary"]}}]},
                    "중요도": {"select": {"name": item["importance"]}},
                    "URL": {"url": item["link"]}
                }
            )
            print(f"   ✅ 업로드 완료: {item['title']}")
            
    except Exception as e:
        print(f"❌ 노션 업로드 실패: {e}")
        # 실패시 원본 데이터를 보여줌 (디버깅용)
        print("Raw Data:", state["final_report"])

# 4. LangGraph 그래프 건설 🏗️
workflow = StateGraph(AgentState)

# 노드 등록
workflow.add_node("tech", tech_agent)
workflow.add_node("biz", biz_agent)
workflow.add_node("academic", academic_agent)
workflow.add_node("summary", summarizer_node)
workflow.add_node("publish", push_to_notion)

# 엣지 연결 (흐름 정의)
# 시작하자마자 3명이 동시에(Parallel) 달려나갑니다
workflow.set_entry_point("tech") 
workflow.set_entry_point("biz")
workflow.set_entry_point("academic")

# 3명이 일이 끝나면 무조건 summary(팀장)에게 보고합니다
workflow.add_edge("tech", "summary")
workflow.add_edge("biz", "summary")
workflow.add_edge("academic", "summary")

# 팀장이 요약하면 publish(노션)로 넘깁니다
workflow.add_edge("summary", "publish")
workflow.add_edge("publish", END)

# 그래프 컴파일
app = workflow.compile()

# 5. 실행!
if __name__ == "__main__":
    print("🤖 CLOVA Market Watcher 가동!")
    # 빈 주머니(State)를 던져주면 알아서 채워옵니다
    app.invoke({"tech_data": "", "biz_data": "", "paper_data": ""})
    print("✨ 모든 작업이 완료되었습니다.")