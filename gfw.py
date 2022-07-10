# -*- coding: UTF-8 -*-
# By: 陈暗魔
# Time: 2022-06-11 17:06

import httpx
import os

# ikuai cookie
cookie = ''
# ikuai ip
ipadd = ''

# ikuai 分流指定外网口
wan = ''


def findAllFile():
    dict1 = {}
    for root, ds, fs in os.walk('./gfw_list/'):
        for filename in fs:
            ids = filename.split('-')
            ids = ids[0]
            dict1[ids] = [root, filename]
    for id in range(1, len(dict1) + 1):
        f = dict1.get(str(id))
        fullname = os.path.join(f[0], f[1])
        yield fullname


def get_gfw(filename):
    for flie in filename:
        data = ""
        i = 0
        f = open(flie, 'r', encoding='utf-8')
        for gfw in f.read().splitlines():
            gfw = gfw.split(' ')
            if i == 0:
                data = gfw[0]
                i = i + 1
            else:
                data = data + f',{gfw[0]}'
        f.close()
        yield data


def main(gfw, id):
    url = f"http://{ipadd}/Action/call"

    payload = "{\"func_name\":\"stream_domain\"," \
              "\"action\":\"add\"," \
              "\"param\":{\"interface\":\"" \
              f"{wan}\",\"src_addr\":\"\",\"domain\":" \
              f"\"{gfw}\"" \
              ",\"comment\":" \
              f"\"gfw_list{id}\"" \
              ",\"week\":\"1234567\",\"time\":\"00:00-23:59\",\"enabled\":\"yes\"}}"
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.39',
        'Content-Type': 'application/json;charset=UTF-8',
        'Cookie': f'username=admin; login=1; sess_key={cookie}'
    }

    response = httpx.post(url, headers=headers, data=payload, timeout=10000)

    print(response.text)


if __name__ == "__main__":
    n = 1
    for ip in get_gfw(findAllFile()):
        # if n == 3:
        #     break
        main(ip, n)
        n += 1
