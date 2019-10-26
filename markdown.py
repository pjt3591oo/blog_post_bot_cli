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
    self.type = ""             # text, code
    self.size = ""             # 15, 16, ...
    self.bold = ""             # True, False
    self.text = children.text.strip().replace('  ', ' ')  # hello world
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
      'a': '15'
    }

    return map.get(tag, '15')


  def tag_type_map(self):

    c = self.children.find('code')

    if c != None:
      return self.children.text == self.children.find('code').text and 'code' or 'text' 

    return 'text'

  def tag_bold_map(self, tag):
    map = {
      'b': True
    }

    return map.get(tag, 'False')

def read(path):
  html = markdown_path('test.md')

  # a = open('index.html', 'w')
  # a.write(html)
  # a.close()

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
  soup = read('.test.md')

  root = convert(soup)
  for node in root.nodes:
    node.show()
   
