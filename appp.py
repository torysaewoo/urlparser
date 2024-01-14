from flask import Flask, request, render_template_string
from urllib.parse import urlparse, parse_qs, unquote

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    url_analysis = ""
    if request.method == 'POST':
        url = request.form.get('url')
        url_analysis = analyze_url(url)
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>마케팅해커 URL Analyzer</title>
        </head>
        <body>
            <h2>마케팅해커 URL 분석기</h2>
            <form method="post">
                URL: <input type="text" name="url">
                <input type="submit" value="분석">
            </form>
            <pre>{{ url_analysis }}</pre>
        </body>
        </html>
    ''', url_analysis=url_analysis)

def analyze_url(url):
    parsed_url = urlparse(url)
    analysis = "기본 URL: " + parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path + "\n"

    # 쿼리 파라미터 추출 및 분석
    query_params = parse_qs(parsed_url.query, encoding="euc-kr",)
    for key, value in query_params.items():
        if key == 'iframe_url':
            analysis += "\niframe 내부 URL:\n"
            iframe_url = unquote(value[0], encoding='euc-kr')  # URL 디코딩 with EUC-KR
            iframe_parsed = urlparse(iframe_url)
            analysis += "  iframe 경로: " + iframe_parsed.path + "\n"
            iframe_query_params = parse_qs(iframe_parsed.query)
            for iframe_key, iframe_value in iframe_query_params.items():
                analysis += f"  {iframe_key}: {unquote(iframe_value[0], encoding='euc-kr')}\n"
                
        else:
            analysis += f"{key}: {unquote(value[0], encoding='euc-kr')}\n"  # URL 디코딩 with EUC-KR

    return analysis

if __name__ == '__main__':
    app.run(debug=True)
