# NBAPB (Blog Auto Posting Bot)

* 설치

  ```bash
  $ pip install bpb
  ```

* 네이버 계정 설정

  file: `config.json`

  ```json
  {
    "NAVER_ID": "",
    "NAVER_PASSWORD": ""
  }

  ```

* chromedriver 설치

  [chromedriver download](https://sites.google.com/a/chromium.org/chromedriver/downloads)

  chromedriver는 크롬 버전에 맞춰 설치


* 구동

  ```bash
  bpb -a [계정정보 json 파일] -f [마크다운 파일 경로] -w [웹 드라이버 파일 경로] -r [-f 인자로 전달한 파일에서 사용하는 리소스 파일 경로] start
  ```

  경로는 **`절대경로`** 입력을 권장합니다.

  마크다운에서 사용하는 리소스(이미지)는 상대경로로 경로를 표현할 수 있으므로 마크다운에서 사용되는 이미지 파일을 따로 디렉터리로 관리하여 **`-r`** 옵션으로 전달

  ```bash
  bpb -a ./config.json -f ./data/test2.md -w ./driver/chromedriver -r ./data/ start
  ```

  계정정보 ./config.json
  마크다운 파일경로 ./data/test2.md
  웹드라이버파일경로 .driver/chromedriver
  마크다운에서 사용하는 리소스 파일 경로 ./data/

  ```bash
  bpb -a /Users/bagjeongtae/Desktop/markdown_to_convert/config.json -f /Users/bagjeongtae/Desktop/markdown_to_convert/data/test1.md -w /Users/bagjeongtae/Desktop/markdown_to_convert/driver/chromedriver -r /Users/bagjeongtae/Desktop/markdown_to_convert/data/ start
  ```



### issue

* 실행환경

현재는 mac에서만 테스트함.

* 이미지 경로문제

윈도우의 경우 다음과 같이 경로를 작성

```
![](C:\\Users\\user\\Desktop\\blog_post_bot_cli\\data\\img.png)
```