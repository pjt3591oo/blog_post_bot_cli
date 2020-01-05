# NBAPB (Blog Auto Posting Bot)

* 데모영상

  [데모영상 바로가기](https://blog.naver.com/pjt3591oo/221722855748)


## 설치, 셋팅

* 설치

  ```bash
  $ pip install bpb
  ```

* 네이버 계정 설정

  **file**: `config.json`

  ```json
  {
    "NAVER_ID": "",
    "NAVER_PASSWORD": ""
  }

  ```

* chromedriver 설치

  [chromedriver download](https://sites.google.com/a/chromium.org/chromedriver/downloads)

  chromedriver는 크롬 버전에 맞춰 설치


## 구동

* **CLI 모드**

  ```bash
  bpb -a [계정정보 json 파일] -f [마크다운 파일 경로] -w [웹 드라이버 파일 경로] -r [-f 인자로 전달한 파일에서 사용하는 리소스 파일 경로] start
  ```

  경로는 **`절대경로`** 입력 권장합니다.

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

* **Code**

  ```py
  from bpb.lib.controller import Controller

  if __name__ == "__main__":
    account_set_path = '/Users/bagjeongtae/Desktop/blog_post_bot_cli/config.json'
    web_driver = '/Users/bagjeongtae/Desktop/blog_post_bot_cli/driver/chromedriver'
    resource_dir = '/Users/bagjeongtae/Desktop/blog_post_bot_cli/data/'
    target = '/Users/bagjeongtae/Desktop/blog_post_bot_cli/data/test.md'
      
    controller = Controller(target, account_set_path,web_driver, resource_dir, debug=True)
    controller()
  ```

### issue

* 실행환경

  mac에서만 테스트함.

* 이미지 경로문제

  윈도우의 경우 다음과 같이 경로를 작성

  ```
  ![](C:\\Users\\user\\Desktop\\blog_post_bot_cli\\data\\img.png)
  ```

* 비동기처리
  
  코드에서 실행할 경우 비동기로 처리하도록 한다.