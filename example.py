from bpb.lib.controller import Controller

if __name__ == "__main__":
  account_set_path = '/Users/bagjeongtae/Desktop/blog_post_bot_cli/config.json'
  web_driver = '/Users/bagjeongtae/Desktop/blog_post_bot_cli/driver/chromedriver'
  resource_dir = '/Users/bagjeongtae/Desktop/blog_post_bot_cli/data/'
  target = '/Users/bagjeongtae/Desktop/blog_post_bot_cli/data/test.md'
    
  controller = Controller(target, account_set_path,web_driver, resource_dir, debug=True)
  controller()