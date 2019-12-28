from selenium import webdriver
import time, json
from selenium.webdriver.common import keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.file_detector import UselessFileDetector

import platform

class Naver:
  
  def __init__(self, ID, PASSWORD,  webdriver_path):
    self.driver = self._get_chromedriver(webdriver_path)
    self.id = "'%s'"%(ID)
    self.password = "'%s'"%(PASSWORD)
    
    self.login()

  @staticmethod
  def _get_chromedriver(webdriver_path):
    return webdriver.Chrome(webdriver_path)

  def login(self):
    self.driver.get('https://nid.naver.com/nidlogin.login')
    self.driver.execute_script("document.getElementsByName('id')[0].value=" + self.id )
    self.driver.execute_script("document.getElementsByName('pw')[0].value=" + self.password )

    self.driver.find_element_by_id('label_ip_on').click()
    self.driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
    time.sleep(7)

    self.move_blog_editor()
    print('>>> login complete <<<')

  def set_bold(self):
    # self.last_text_line_focus()
    selector = "se-toolbar-button-bold"
    s = "document.getElementsByClassName('%s')[0].click()"%(selector)
    time.sleep(0.4)
    self.driver.execute_script(s)
    time.sleep(1.5)

  def set_font_size(self, size):
    # self.last_text_line_focus()
    selector = "se-toolbar-button-font-size-code"
    size = str(size)

    s = {
      "11": "se-font-size-code-fs11",
      "13": "se-font-size-code-fs13",
      "15": "se-font-size-code-fs15",
      "16": "se-font-size-code-fs16",
      "19": "se-font-size-code-fs19",
      "24": "se-font-size-code-fs24",
      "28": "se-font-size-code-fs28",
      "30": "se-font-size-code-fs30",
      "34": "se-font-size-code-fs34",
      "38": "se-font-size-code-fs38"
    }

    query = "document.getElementsByClassName('%s')[0].click()"%(selector)
    self.driver.execute_script(query)
    time.sleep(1.0)

    query = "document.getElementsByClassName('%s')[0].click()"%(s[size])

    self.driver.execute_script(query)
    time.sleep(1.0)

  def set_code(self,  text): 
    # 소스코드 추가
    selector = "se-toolbar-button-code" 
    query = "document.getElementsByClassName('%s')[0].click()"%(selector)
    self.driver.execute_script(query)
    time.sleep(0.5)

    # # 추가된 소스코드 클릭
    # code_editors = self.driver.find_elements_by_css_selector('.%s'%(selector))
    # code_editors[-1].click()

    # 포커스 잡힌 부분에 데이터 입력
    actions = ActionChains(self.driver)
    actions.send_keys(text)
    actions.perform()
    time.sleep(1.5)

  def input_img_btn_click(self):
    # 사진 버튼을 눌러야 input창이 발생
    time.sleep(0.5)
    selector = '.se-toolbar-item-image'
    img_tag = self.driver.find_element_by_css_selector('%s'%(selector))
    time.sleep(0.5)
    img_tag.click()
    time.sleep(0.5)
    webdriver.ActionChains(self.driver).send_keys(keys.Keys.ESCAPE).perform()
    time.sleep(0.5)

  def input_img(self, path):
    print(path)
    self.input_img_btn_click()

    x_path = '/html/body/input[1]'
    img_tag = self.driver.find_element_by_xpath(x_path)

    img_tag.send_keys(path)
    time.sleep(0.5)

  def input_text(self, text):
    # self.last_text_line_focus()
  
    actions = ActionChains(self.driver)
    actions.send_keys(text)
    actions.perform()
    time.sleep(0.7)

  def move_blog_editor(self):
    self.driver.get('https://blog.naver.com/%s/postwrite'%(self.id.replace("'", '')))
    time.sleep(2)

    self.already_write_popup_close()
    self.helper_close()
    
  # 블로그 접속하면 우측에 뜨는 도움말 닫기
  # 해당 도움말 때문에 .se-component-content 마지막 클릭시 clickable에러 발생
  def helper_close(self):
    query = '.se-help-panel-close-button'
    try:
      helper_dom = self.driver.find_element_by_css_selector(query)
      helper_dom.click()
    except:
      print('우측에 helper가 없음.')

    time.sleep(0.5)

  # "작성 중인 글이 있습니다." 팝업
  def already_write_popup_close(self):
    query = '.se-popup-button-cancel'

    try:
      already_wirte = self.driver.find_element_by_css_selector(query)
      already_wirte.click()
    except:
      print('작성 중인 글이 있습니다. 팝업이 없음')

    time.sleep(0.5)

  def last_text_line_focus(self):
    selector = '.se-text-paragraph'  #  .se-component-content
    # query = "var componentCnt = document.getElementsByClassName('%s').length; document.getElementsByClassName('%s')[componentCnt - 1].click()"%(selector, selector)
    components = self.driver.find_elements_by_css_selector(selector)
    # self.driver.execute_script(query)
    time.sleep(0.3)
    print(components[-1])
    components[-1].click()
    time.sleep(0.5)

if __name__ == "__main__":

  NAVER_ID = ''
  NAVER_PASSWORD = ''
  
  account_set_path = './config.json'
  webdriver_path = ''

  with open(account_set_path) as json_file:
    f = json.loads(json_file)

    NAVER_ID = f['id']
    NAVER_PASSWORD = f['password']

  # 아이디/비밀번호를 입력해준다.
  naver = Naver(NAVER_ID, NAVER_PASSWORD, webdriver_path)

  naver.set_bold()

  naver.set_font_size(13)

  code1 = 'let a = 10;'
  code2 = '''function test() {
  console.log('hello world');
}'''

  naver.set_code(code1)
  naver.set_code(code2)

  # naver.set_bold()
  # naver.input_text('안녕하세요\n')
  
  # naver.set_bold()
  # naver.set_font_size(13)
  # naver.input_text('안녕하세요1\n')

  # naver.set_font_size(15)
  # naver.input_text('안녕하세요2\n')

  # naver.set_font_size(16)
  # naver.input_text('안녕하세요3 ')

  # naver.set_bold()
  # naver.input_text(' 안녕하세요4')