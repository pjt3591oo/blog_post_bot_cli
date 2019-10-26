import markdown 
import naver 
from config import NAVER_ID, NAVER_PASSWORD

class Convert():
  def __init__(self, path, id, password):
    self.naver = naver.Naver(id, password)

    soup = markdown.read(path)
    self.root = markdown.convert(soup)


  def text_setting(self, node):
    self.naver.inputText('')
    self.naver.setFontSize(node.size)
    if node.bold : self.naver.setBold()

  def code_setting(self, node):
    self.naver.setCode(node.text)

  def __call__(self):
    
    for node in self.root.nodes:
      node.show()
      
      if node.type == 'text':
        self.text_setting(node)
        self.naver.inputText(node.text + '\n')

      elif node.type =='code':
        self.code_setting(node)
         

if __name__ == "__main__":
  c = Convert('./data/text.md', NAVER_ID, NAVER_PASSWORD)
  c()