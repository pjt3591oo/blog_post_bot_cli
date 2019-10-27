import markdown 
import naver 
from config import NAVER_ID, NAVER_PASSWORD

class Convert():
  def __init__(self, path, id, password):
    self.naver = naver.Naver(id, password)

    soup = markdown.read(path)
    self.root = markdown.convert(soup)


  def text_setting(self, node):
    self.naver.input_text('')
    self.naver.set_font_size(node.size)
    if node.bold : self.naver.set_bold()

  def code_setting(self, node):
    self.naver.set_code(node.text)

  def img_setting(self, node):
    self.naver.input_img(node.text)

  def __call__(self):
    
    for node in self.root.nodes:
      node.show()
      
      if node.type == 'text':
        self.text_setting(node)
        self.naver.input_text(node.text + '\n')

      elif node.type =='code':
        self.code_setting(node)
         
      elif node.type == 'img':
        self.img_setting(node)

if __name__ == "__main__":
  c = Convert('./data/test.md', NAVER_ID, NAVER_PASSWORD)
  c()