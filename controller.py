# import parser
# print(parser.markdown)
import naver 
from parser import markdown
from config import NAVER_ID, NAVER_PASSWORD
from utils.progress_bar import progress_bar as pb

class Post():
  def __init__(self, path, id, password, **kwargs):
    if kwargs.get('debug', False):
      self.naver = naver.Naver(id, password)

    soup = markdown.read(path)
    self.root = markdown.convert(soup)

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

if __name__ == "__main__":
  post = Post('./data/test2.md', NAVER_ID, NAVER_PASSWORD, debug=True)
  post()