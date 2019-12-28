import json, time

from bpb.utils.progress_bar import progress_bar as pb
from bpb.parser import markdown
from bpb.lib.naver import Naver

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
    
    soup = markdown.read(path)
    self.root = markdown.convert(soup, resource_dir)

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
    pb(3)

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

if __name__ == "__main__":

  NAVER_ID = ''
  NAVER_PASSWORD = ''
  
  account_set_path = './config.json'
  web_driver = './driver/chromedriver'
  resource_dir = './data/'
    
  controller = Controller('./data/test2.md', account_set_path,web_driver, resource_dir, debug=True)
  controller()