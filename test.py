
import os

hosts = os.environ.get('SSH_HOSTS')#.split(',')
user = os.environ.get('SSH_USER')
key = os.environ.get('SSH_KEY')

print(hosts)
print(user)
print(key)