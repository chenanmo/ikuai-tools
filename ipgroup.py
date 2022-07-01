# -*- coding: UTF-8 -*-
# By: 陈暗魔
# Time: 2022-06-11 13:35
import httpx
import os

cookie = '03d909ce0e910249bdc6a40249480334'
ipadd = '127.0.0.1'


def findAllFile():
    dict1 = {}
    for root, ds, fs in os.walk('./china_ip/'):
        for filename in fs:
            ids = filename.split('-')
            ids = ids[0]
            dict1[ids] = [root, filename]
    for id in range(1, len(dict1) + 1):
        f = dict1.get(str(id))
        fullname = os.path.join(f[0], f[1])
        yield fullname


def get_ip(filename):
    for flie in filename:
        data = ""
        i = 0
        f = open(flie, 'r', encoding='utf-8')
        for ip in f.read().splitlines():
            ip = ip.split(' ')
            if i == 0:
                data = ip[0]
                i = i + 1
            else:
                data = data + f',{ip[0]}'
        f.close()
        yield data


def main(ip, id):
    url = f"http://{ipadd}/Action/call"
    payload = "{\"func_name\":\"ipgroup\"," \
              "\"action\":\"add\"," \
              "\"param\":{\"group_name\":" \
              f"\"china_ip_{id}\"," \
              "\"addr_pool\":" \
              f"\"{ip}\"," \
              "\"newRow\":true," \
              "\"comment\":\",\"}}"
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.39',
        'Content-Type': 'application/json;charset=UTF-8',
        'Accept-Encoding': 'gzip, deflate',
        f'Cookie': f'username=admin; login=1; sess_key={cookie}'
    }
    response = httpx.post(url, headers=headers, data=payload, timeout=10000)

    print(response.text)


if __name__ == '__main__':
    n = 1
    for ip in get_ip(findAllFile()):
        main(ip, n)
        n += 1
