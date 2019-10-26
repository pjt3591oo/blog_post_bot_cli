# NBAPB (Blog Auto Posting Bot)

* 네이버 계정 설정

file: `config.py`

```py
NAVER_ID = ''
NAVER_PASSWORD = ''
```

* chromedriver 설치

[chromedriver download](https://sites.google.com/a/chromium.org/chromedriver/downloads)

chromedriver는 77.x 버전을 사용하도록 하자. 78.x 버전은 정상적으로 동작하지 않음

* 의존성 모듈 설치

```bash
pip install -r requirements.txt
```

* 구동

```bash
$ python controller.py
```

* release