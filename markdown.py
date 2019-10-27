from markdown2 import markdown_path
from bs4 import BeautifulSoup

class Root: 

  def __init__(self):
    self.nodes = []

  def add_node(self, node):
    self.nodes.append(node)

  def show(self):
    
    print(1)
  

class Node:
  
  def __init__(self, children): 
    self.type = ""             # text, code, img
    self.size = ""             # 15, 16, ...
    self.bold = ""             # True, False
    self.text = children.text.strip().replace('  ', ' ')  
    self.children = children
    self.childrens = []        # [Node, Node, ...]
    
    self.name_parse()

  def add_childrens(self, children):
    self.childrens.append(children)

  def show(self):
    print("Type: %s \nSize: %s \nBold: %s \nText: %s \nChildren Length: %d"%(self.type, self.size, self.bold, self.text, len(self.childrens)))
    print()
    print()

  def name_parse(self):
    tag = self.children.name

    self.type = self.tag_type_map()
    self.text = self.get_tag_text()
    self.size = self.tag_size_map(tag)
    self.bold = self.tag_bold_map(tag)

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

  def get_tag_text(self):
    map = {
      "text": lambda : self.children.text,
      "code": lambda : self.children.text,
      "img": lambda: self.children.find('img').get('src')
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

    return map.get(tag, 'False')

def read(path):
  html = markdown_path(path)

  return _soup(html)

def _soup(contents):
  soup = BeautifulSoup(contents, 'lxml')
  return soup

def convert(soup):
  childrens = soup.find('body').children
  root = Root()

  for children in childrens: 
    if children.name !=None: 
      root.add_node(Node(children))

  return root

if __name__ == '__main__':
  soup = read('./data/test1.md')

  root = convert(soup)
  for node in root.nodes:
    node.show()
   
