import os
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

def find_correct_column_name():
    token = os.getenv("NOTION_TOKEN")
    database_id = os.getenv("NOTION_DB_ID")
    notion = Client(auth=token)

    # 가장 흔한 컬럼 이름 후보 4가지
    candidates = ["이름", "Name", "Title", "제목"]

    print(f"🔍 다음 ID로 접속 시도 중: {database_id}")
    print("------------------------------------------------")

    for col_name in candidates:
        print(f"👉 컬럼 이름이 '{col_name}' 인지 확인 중...", end=" ")
        try:
            notion.pages.create(
                parent={"database_id": database_id},
                properties={
                    col_name: { 
                        "title": [{"text": {"content": f"✅ 찾았다! 정답은 {col_name}"}}]
                    }
                }
            )
            print("🎉 성공!!")
            print("------------------------------------------------")
            print(f"✅ 당신의 노션 제목 컬럼 이름은 [ {col_name} ] 입니다.")
            print("이제 코드에서 '제목' 대신 이 이름을 쓰시면 됩니다.")
            return # 성공했으니 종료
            
        except Exception as e:
            # 실패하면 조용히 넘어감
            if "property that exists" in str(e):
                print("❌ 아님")
            else:
                print(f"\n⚠️ 다른 에러 발생: {e}")

if __name__ == "__main__":
    find_correct_column_name()