from flask import Flask, request, jsonify
import feedparser
from urllib.parse import unquote  # ✅ 필수!
import os

app = Flask(__name__)

rss_feeds = {
    "IT": "https://www.inews24.com/rss/news_it.xml",
    "경제": "https://www.inews24.com/rss/news_economy.xml",
    "정치": "https://www.inews24.com/rss/news_politics.xml",
    "사회": "https://www.inews24.com/rss/news_society.xml",
    "문화": "https://www.inews24.com/rss/news_culture.xml",
    "연예": "https://www.inews24.com/rss/news_enter.xml",
    "스포츠": "https://www.inews24.com/rss/news_sports.xml"
}


@app.route("/rss/<category>", methods=["GET", "POST"])
def rss_by_category(category):
    from urllib.parse import unquote
    category = unquote(category)
    print(f"💬 요청받음: {category}")

    if category not in rss_feeds:
        return jsonify({
            "version": "2.0",
            "template": {
                "outputs": [{
                    "simpleText": {
                        "text": f"❗ [{category}] 분야의 뉴스는 지원하지 않습니다."
                    }
                }]
            }
        })

    return get_latest_news_card(category, rss_feeds[category])


def get_latest_news_card(category, feed_url):
    feed = feedparser.parse(feed_url)
    if not feed.entries:
        return jsonify({
            "version": "2.0",
            "template": {
                "outputs": [{
                    "simpleText": {
                        "text": "❗ 최신 뉴스를 불러올 수 없습니다."
                    }
                }]
            }
        })

    items = []
    for entry in feed.entries[:3]:
        items.append({
            "title": entry.title,
            "description": entry.get("published", "이뉴스24 제공"),
            "link": {
                "web": entry.link
            }
        })

    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [{
                "listCard": {
                    "header": {
                        "title": f"{category} 분야 최신 뉴스"
                    },
                    "items":
                    items,
                    "buttons": [{
                        "label": "다른 분야 뉴스 보기",
                        "action": "block",
                        "blockId":
                        "68345c25c5b310190b6dfa9f"  # ← 이 부분만 바꾸면 돼요!
                    }]
                }
            }]
        }
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render가 주는 포트 사용
    app.run(host="0.0.0.0", port=port)
