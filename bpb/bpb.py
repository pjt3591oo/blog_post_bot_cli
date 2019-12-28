#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function

__author__ = "JeongTae Park"
__copyright__ = "Copyright 2019, First Last"
__version__ = "1.0.0"
__maintainer__ = "JeongTae Park"
__email__ = "pjt3591oo@gmail.com"
__status__ = "development"

from logzero import logger
import time, json, random, sys, os, argparse, platform

from markdown2 import markdown_path
from bs4 import BeautifulSoup, NavigableString, Tag

from selenium import webdriver

from selenium.webdriver.common import keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.file_detector import UselessFileDetector


class Root: 

  def __init__(self):
    self.contents = []

  def add_contents(self, content):
    self.contents.append(content)

  def show(self):
    print(1)
  
class Children:

  def __init__(self, **kwargs):
    self.origin = kwargs.get('origin')
    self.type = kwargs.get('type', 'text')
    self.size = kwargs.get('size', 15)
    self.bold = kwargs.get('bold', False)
    self.text = kwargs.get('text', '')
    self.color = kwargs.get('color', '#000')

class Content:
  
  def __init__(self, children, resource_dir): 
    self.type = ""             # text, code, img
    self.size = ""             # 15, 16, ...
    self.bold = False          # True, False
    self.text = children.text.strip().replace('  ', ' ')  
    self.children = children
    self.childrens = []        # [Node, Node, ...]
    
    self.name_parse(resource_dir)
    self.content_parse()
    
  def add_childrens(self, children):
    self.childrens.append(children)

  def show(self):
    print("Type: %s \nSize: %s \nBold: %s \nText: %s \nChildren Length: %d"%(self.type, self.size, self.bold, self.text, len(self.childrens)))
    print([{"type": children.type, "size": children.size, "bold": children.bold, "text": children.text, "color": children.color } for children in self.childrens])
    print()

  def name_parse(self, resource_dir):
    tag = self.children.name

    self.type = self.tag_type_map()
    self.text = self.get_tag_text(resource_dir)
    self.size = self.tag_size_map(tag)
    self.bold = self.tag_bold_map(tag)

  def content_parse(self):
    
    childrens = [children for children in self.children.contents if (type(children) == NavigableString and children.string.strip()) or type(children) == Tag]
    for idx, children in enumerate(childrens):
      c = {}
      is_last_text_enter = False

      if self.type == 'text':
        text = children.string.strip().replace('\n', '')
        bold = (children.name == 'code' or children.name == 'strong') and True or False
        c = Children(origin=children, type=self.type, size=self.size, bold=bold, text=text )
        if idx == (len(childrens) - 1) :
          is_last_text_enter = self.is_last_text_enter()

      else: 
        c = Children(origin=children, type=self.type, size=self.size, bold=self.bold, text=self.text )

      self.childrens.append(c)
     
      if is_last_text_enter:
        self.childrens.append(Children(origin="enter", type="text", size="15", bold=False, text="\n"))
      

  def is_last_text_enter(self):
    return self.type == 'text' and self.size == '15'

  def tag_size_map(self, tag):
    map = {
      'h1': '24',
      'h2': '19',
      'h3': '16',
      'h4': '15',
      'h5': '13',
      'h6': '11',

      'p': '15',
      'code': '15',
      'a': '15',
    }

    return map.get(tag, '15')

  def get_tag_text(self, resource_dir):
    map = {
      "text": lambda : self.children.text,
      "code": lambda : self.children.text,
      "img": lambda: os.path.join(resource_dir, self.children.find('img').get('src').split('/')[-1])
    }
    
    return map[self.type]()

  def tag_type_map(self):

    is_code = self.children.find('code')
    
    node_type = 'text'

    if is_code != None:
      node_type = self.children.text == self.children.find('code').text and 'code' or 'text' 
    elif self.children.find('img') != None:
      node_type = 'img'

    return node_type

  def tag_bold_map(self, tag):
    map = {
      'b': True
    }

    return map.get(tag, False)

  def get_children(self):
    return self.childrens

  def add_children(self, children):
    self.childrens.append(children)


def read(path):
  html = markdown_path(path)

  return _soup(html)

def _soup(contents):
  soup = BeautifulSoup(contents, 'lxml')
  return soup

def convert(soup, resource_dir):
  childrens = soup.find('body').children
  root = Root()

  for children in childrens: 
    if children.name !=None: 
      content = Content(children, resource_dir)
      root.add_contents(content)

  return root

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

def display(res_time, value, endvalue, bar_length=20):
        percent = float(value) / endvalue
        arrow = '-' * int(round(percent * bar_length)-1) + '>'
        spaces = ' ' * (bar_length - len(arrow))

        sys.stdout.write("\rPercent: [{0}] {1}% ({2} seconds)".format(arrow + spaces, int(round(percent * 100)), res_time))
        sys.stdout.flush()

def progress_bar(max_sleep_time = 5):
  res_time = random.randrange(1, max_sleep_time + 1)
  
  for i in range(0, res_time):
    display(res_time, (max_sleep_time/res_time) * (i + 1), max_sleep_time)
    time.sleep(1)

  sys.stdout.write('\n\n\n')


class Controller():
  def __init__(self, path, account_set_path, webdriver_path, resource_dir, **kwargs):
    '''
      params
        path: 마크다운 파일 경로
        account_set_path: 네이버 계정정보 파일 경로

    '''
    # if kwargs.get('debug', False):
    with open(account_set_path, 'r') as json_file:
      f = json.loads(json_file.read())
      self.naver = Naver(f['NAVER_ID'], f['NAVER_PASSWORD'], webdriver_path)
    
    soup = read(path)
    self.root = convert(soup, resource_dir)

  def text_bold_setting(self, content):
    if content.bold : 
      self.naver.set_bold()

  def text_fontsize_setting(self, content):
    self.naver.input_text('')
    self.naver.set_font_size(content.size)

  def code_setting(self, node):
    self.naver.set_code(node.text)

  def img_setting(self, node):
    self.naver.input_img(node.text)

  def __call__(self):
    progress_bar(3)

    for content in self.root.contents:
      content.show()
      print('>>>>>>>>>>>>>>> content start %s, %s <<<<<<<<<<<<<<'%(content.type, content.size))
      if content.type == 'text':
        self.text_fontsize_setting(content)
        
        for children in content.childrens:
          print('****************** ', children.type, children.size, children.bold, children.text , ' ******************')
          
          self.text_bold_setting(children)
          self.naver.input_text(children.text+ ' ')
          self.text_bold_setting(children)
        
        self.naver.input_text('\n')

      elif content.type =='code':
        self.code_setting(content)
        
      elif content.type == 'img':
        self.img_setting(content)

    print('\n\n%s posting complete %s'%('*'*25, '*'*25))
    print('60초 후 브라우저가 꺼집니다 그 전에 저장하세요.')
    time.sleep(60)

class bpb():
    def post(self, args):
        msg = "arg=%s, file_path=%s, account_set=%s, resource_dir=%s, verbose=%s, web_driver=%s"%(
            args.arg,
            args.file_path,
            args.account_set,
            args.resource_dir,
            args.verbose,
            args.web_driver
        )
        logger.info(msg)
        
        controller = Controller(args.file_path, args.account_set, args.web_driver, args.resource_dir, debug=True)
        controller()

    def execute(self):
        PARSER = argparse.ArgumentParser()

        PARSER.add_argument("arg", help="Required positional argument")

        PARSER.add_argument("-a", "--account-set", action="store")   # 계정정보 파일

        PARSER.add_argument("-w", "--web-driver", action="store")    # 크롬 드라이버 경로
        PARSER.add_argument("-f", "--file-path", action="store")     # 파일 경로
        PARSER.add_argument("-r", "--resource-dir", action="store") # 리소스 파일 경로

        PARSER.add_argument(
            "-v",
            "--verbose",
            action="count",
            default=0,
            help="Verbosity (-v, -vv, etc)")

        PARSER.add_argument(
            "--version",
            action="version",
            version="{prog} (version {version})".format(prog="BLOG POSTING BOT", version=__version__))

        kwargs = PARSER.parse_args()

        self.post(kwargs)

    def test(self):
        print("hello world")

def execute():
  PARSER = argparse.ArgumentParser()

  PARSER.add_argument("arg", help="Required positional argument")

  PARSER.add_argument("-a", "--account-set", action="store")   # 계정정보 파일

  PARSER.add_argument("-w", "--web-driver", action="store")    # 크롬 드라이버 경로
  PARSER.add_argument("-f", "--file-path", action="store")     # 파일 경로
  PARSER.add_argument("-r", "--resource-dir", action="store") # 리소스 파일 경로

  PARSER.add_argument(
      "-v",
      "--verbose",
      action="count",
      default=0,
      help="Verbosity (-v, -vv, etc)")

  PARSER.add_argument(
      "--version",
      action="version",
      version="{prog} (version {version})".format(prog="BLOG POSTING BOT", version=__version__))

  kwargs = PARSER.parse_args()

  controller = Controller(kwargs.file_path, kwargs.account_set, kwargs.web_driver, kwargs.resource_dir, debug=True)
  controller()
  
if __name__ == "__main__":
    print('test')
#     PARSER = argparse.ArgumentParser()

#     PARSER.add_argument("arg", help="Required positional argument")

#     PARSER.add_argument("-a", "--account-set", action="store")   # 계정정보 파일

#     PARSER.add_argument("-w", "--web-driver", action="store")    # 크롬 드라이버 경로
#     PARSER.add_argument("-f", "--file-path", action="store")     # 파일 경로
#     PARSER.add_argument("-r", "--resource-dir", action="store") # 리소스 파일 경로

#     PARSER.add_argument(
#         "-v",
#         "--verbose",
#         action="count",
#         default=0,
#         help="Verbosity (-v, -vv, etc)")

#     PARSER.add_argument(
#         "--version",
#         action="version",
#         version="{prog} (version {version})".format(prog="BLOG POSTING BOT", version=__version__))

#     kwargs = PARSER.parse_args()

#     post(kwargs)