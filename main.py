# Flask 서버와 외부 요청 처리를 위한 모듈 import
from flask import Flask, request, jsonify

# RSS 파싱을 위한 라이브러리
import feedparser

# 테스트용 딜레이를 위한 시간 모듈
import time

# Flask 앱 초기화
app = Flask(__name__)

# 카테고리별 RSS 피드 주소 정의 (이뉴스24 기준)
rss_feeds = {
    "IT": "https://www.inews24.com/rss/news_it.xml",
    "경제": "https://www.inews24.com/rss/news_economy.xml",
    "정치": "https://www.inews24.com/rss/news_politics.xml",
    "사회": "https://www.inews24.com/rss/news_society.xml",
    "문화": "https://www.inews24.com/rss/news_culture.xml",
    "생활": "https://www.inews24.com/rss/news_life.xml",
    "연예": "https://www.inews24.com/rss/news_enter.xml",
    "스포츠": "https://www.inews24.com/rss/news_sports.xml"
}


# 카카오 챗봇에서 POST 요청이 들어올 경로 설정
@app.route("/webhook", methods=["POST"])
def kakao_webhook():
    # 요청 본문(JSON) 가져오기
    req = request.get_json()
    print("💬 요청 받음:", req)  # 디버깅용 콘솔 출력

    # 사용자가 입력한 말 추출
    user_msg = req['userRequest']['utterance']

    # 만약 사용자가 입력한 분야가 rss_feeds에 있다면
    if user_msg in rss_feeds:
        feed_url = rss_feeds[user_msg]  # 해당 분야의 RSS 주소 가져오기
        news_text = get_latest_news(feed_url)  # 최신 뉴스 3개 불러오기

        # 카카오 챗봇으로 보낼 JSON 응답
        return jsonify({
            "version": "2.0",
            "template": {
                "outputs": [{
                    "simpleText": {
                        "text": news_text  # 불러온 뉴스 내용 전송
                    }
                }]
            }
        })

    # 입력한 분야가 없는 경우 안내 메시지 응답
    else:
        return jsonify({
            "version": "2.0",
            "template": {
                "outputs": [{
                    "simpleText": {
                        "text": "❗ 해당 분야의 뉴스를 찾을 수 없어요. 예) 정치, 경제, 연예 등"
                    }
                }]
            }
        })


# RSS 피드에서 뉴스 3개 불러오는 함수
def get_latest_news(feed_url):
    feed = feedparser.parse(feed_url)  # RSS 주소 파싱
    if feed.entries:  # 뉴스가 하나라도 있으면
        messages = []
        for entry in feed.entries[:3]:  # 최신 뉴스 3개까지만
            title = entry.title  # 뉴스 제목
            link = entry.link  # 뉴스 링크
            messages.append(f"📌 {title}\n🔗 {link}")  # 출력 형식 설정
        return "\n\n".join(messages)  # 뉴스 3개를 하나의 문자열로 반환
    else:
        return "❗ 최신 뉴스를 불러올 수 없습니다."


# 서버 실행 (로컬 테스트용)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
