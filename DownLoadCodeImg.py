import requests
import random
import os


def download_codeimg(count):
    if not os.path.exists('./CodeImg/Source/'):
        os.makedirs('./CodeImg/Source/')

    for index, i in enumerate(range(1, count)):
        url = "https://perbank.abchina.com/EbankSite/LogonImageCodeAct.do?r={0}".format(random.random())
        print url
        response = requests.get(url)
        img = response.content
        with open('./CodeImg/Source/' + str(index) + '.jpg', 'wb') as f:
            f.write(img)


if __name__ == "__main__":
    download_codeimg(100)
