from PIL import Image
import requests
import base64


def conv_d(data):
    d = []

    for c in data:
        d.append(format(ord(c), '08b'))

    return d


def mod_p(p, data):
    d = conv_d(data)
    len_d = len(d)
    im_data = iter(p)

    for i in range(len_d):
        p = [v for v in im_data.__next__()[:3] + im_data.__next__()[:3] +
             im_data.__next__()[:3]]

        for j in range(0, 8):
            if d[i][j] == '0' and p[j] % 2 != 0:
                p[j] -= 1
            elif d[i][j] == '1' and p[j] % 2 == 0:
                if p[j] != 0:
                    p[j] -= 1
                else:
                    p[j] += 1

        if i == len_d - 1:
            if p[-1] % 2 == 0:
                if p[-1] != 0:
                    p[-1] -= 1
                else:
                    p[-1] += 1
        else:
            if p[-1] % 2 != 0:
                p[-1] -= 1

        p = tuple(p)
        yield p[0:3]
        yield p[3:6]
        yield p[6:9]


def encode():
    img = Image.open('image.png', 'r')

    data = 'hostname'

    new_img = img.copy()

    w = new_img.size[0]
    (x, y) = (0, 0)

    for p in mod_p(new_img.getdata(), data):
        new_img.putpixel((x, y), p)

        if x == w - 1:
            x = 0
            y += 1
        else:
            x += 1

    new_img.save('image-steg.png', 'PNG')

    with open('image-steg.png', 'rb') as img:
        return base64.b64encode(img.read())



def main():
    im_b64 = encode().decode('utf-8')

    headers = {'Authorization': 'Client-ID 7a93b181f27546c'}
    data = {'image': im_b64, 'type': 'base64', 'name': 'image.png'}

    response = requests.post('https://api.imgur.com/3/upload', data=data, headers=headers)

    print(f'Imgur link: {response.json()["data"]["link"]}')
    

if __name__ == '__main__':
    main()