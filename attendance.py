from flask import Flask, request, render_template_string
from datetime import datetime
import csv
import os

app = Flask(__name__)

CSV_FILE = "attendance.csv"

# 회원명단
MEMBERS = [
    "전일주", "곰트림", "엘펜하임", "젊은총", "지리산",
    "산그리메", "카라", "유화", "봉우리", "쇼콜라",
    "부메랑", "안젤리나", "제이미", "수경", "와송",
    "복이언니", "영남", "여우비"
]

# 출석부 생성
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["이름", "출석시간"])

HOME_HTML = """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>해밀산악회 출석체크</title>
</head>
<body>

<h2>해밀산악회 QR 출석체크</h2>

<form action="/checkin" method="post">

<select name="name">
{% for member in members %}
<option value="{{member}}">
{{member}}
</option>
{% endfor %}
</select>

<input type="submit" value="출석하기">

</form>

<br>
<a href="/list">출석현황 보기</a>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(
        HOME_HTML,
        members=MEMBERS
    )

@app.route("/checkin", methods=["POST"])
def checkin():

    name = request.form["name"]

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    already = False

    with open(CSV_FILE, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        next(reader, None)

        for row in reader:
            if row and row[0] == name:
                already = True
                break

    if already:
        return f"""
        <h2>{name}님</h2>
        <h3 style='color:red'>
        이미 출석하셨습니다.
        </h3>

        <a href='/'>돌아가기</a>
        """

    with open(CSV_FILE, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([name, now])

    return f"""
    <h2>{name}님</h2>

    <h3 style='color:blue'>
    출석 완료!
    </h3>

    <p>{now}</p>

    <a href='/'>돌아가기</a>
    """

@app.route("/list")
def attendance_list():

    html = """
    <html>
    <head>
    <meta charset="utf-8">
    <title>출석현황</title>
    </head>
    <body>

    <h2>출석현황</h2>

    <table border="1" cellpadding="5">
    <tr>
        <th>번호</th>
        <th>이름</th>
        <th>출석시간</th>
    </tr>
    """

    count = 0

    with open(CSV_FILE, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        next(reader, None)

        for row in reader:
            count += 1

            html += f"""
            <tr>
                <td>{count}</td>
                <td>{row[0]}</td>
                <td>{row[1]}</td>
            </tr>
            """

    html += f"""
    </table>

    <br>
    총 출석인원 : {count}명

    <br><br>

    <a href="/">출석페이지</a>

    </body>
    </html>
    """

    return html

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )