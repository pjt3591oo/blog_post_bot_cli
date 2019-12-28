from markdown2 import markdown_path
from bs4 import BeautifulSoup, NavigableString, Tag
import os 


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

if __name__ == '__main__':
  resource_dir = '/Users/bagjeongtae/Desktop/markdown_to_convert/data'
  soup = read('./data/test2.md')

  root = convert(soup, resource_dir)
  for content in root.contents:
    content.show()
   
