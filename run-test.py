import json
import os
import subprocess as sp
import time

import requests
from selenium import webdriver

subprocess.Popen(["Xvfb", ":99"])
os.environ['DISPLAY'] = ':99'

sp.check_call(["docker", "run", "-d",
               "--name", "blog", "multistage-blog"])
sp.check_call(["docker", "exec", "blog",
               "mkdir", "/mnt/db"])
sp.check_call(["docker", "exec", "blog",
               "/appenv/bin/python",
               "-c", "from blog import storage;"
                     "storage.create_all("
                     "storage.get_engine())"])

details = sp.check_output(["docker", "inspect", "blog"])
t = json.loads(details)
address = t[0]["NetworkSettings"]["IPAddress"]

time.sleep(10)

requests.post(f'http://{address}:8080/posts',
              json=dict(author='foo',
                        content='hello there friend'))

d = webdriver.Firefox()
d.get(f"http://{address}:8080/")
content = d.find_element_by_tag_name("ul")

innerHTML = content.get_attribute('innerHTML')
if 'hello there friend' not in innerHTML:
     raise ValueError('no friend', innerHTML)

print("Success!", innerHTML)

sp.check_call(["docker",
               "rm", "-f", "blog"])
