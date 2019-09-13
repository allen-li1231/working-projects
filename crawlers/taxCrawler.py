"""
@Author: Allen Lee     2018-01-24
"""
import re
from compile.my_class import MyPath
#from io import BytesIO
#import numpy as np
import pandas as pd
#import pytesseract
import requests
#import cv2
from PIL import Image#, ImageChops
from bs4 import BeautifulSoup as soup


def binarizeImg(img, threshold=120):
    gray_img = img.convert('L')
    bw = gray_img.point(lambda x: 0 if x < threshold else 255, '1')
    return bw


def train_set(amount=120):
    captcha_url = 'https://www.tax.sh.gov.cn/xbwz/servlet/GetshowimgSmall'
    s = requests.session()
    for i in range(amount):
        bPic = s.get(captcha_url).content
        img = Image.open(BytesIO(bPic))
        bw = binarizeImg(img)
        bw.save(r'C:\Users\super\Desktop\Captcha\c%d.png' % i, 'png')


def imgWordPartition(binarized_image, word_minwidth, threshold):
    pic_matrix = np.asarray(binarized_image)
    pic_row = pic_matrix.shape[0]
    pic_col = pic_matrix.shape[1]
    border = []
    start_col = 0

    while start_col < pic_col - 1:
        T = pic_row - threshold
        # 0=black and 1=white, so true threshold=row lenth-nominal threshold
        if sum(pic_matrix[:, start_col]) <= T:
            # This is where left border of a word emerges.
            word_flag = 0
            # This parameter is to count the width of a single word.
            for end_col in range(start_col, pic_col):
                word_flag += 1
                if sum(pic_matrix[:, end_col]) > T or end_col >= pic_col - 1:
                    # This is where right border of a word emerges,
                    # pay attention to the "endless" right border.
                    if word_flag < word_minwidth:
                        # word too short, thus abandoned.
                        start_col = end_col + 1
                        break
                    else:
                        border.append((start_col, end_col))
                        start_col = end_col + 1
                        break
        else:
            start_col += 1
    return border


# TODO: not a good solution...
def rotateAngle(binarized_image):
    pic_matrix = np.asarray(binarized_image)
    pic_matrix.flags.writeable = True
    d = np.uint8(pic_matrix)
    d[d == 0] = 255
    d[d == 1] = 0
    coords = np.column_stack(np.where(d > 0))
    return cv2.minAreaRect(coords)[-1]


def rotatePadding(binarized_image):
    angle = rotateAngle(binarized_image)
    img = ImageChops.invert(binarized_image)
    product = img.rotate(angle, expand=1)
    # fff = Image.new('1', product.size, 'white')
    # out = Image.blend(product, fff, 0.0)
    return ImageChops.invert(product)


def makeBlackBorder(image):
    pic_matrix = np.asarray(image, np.uint8)
    pic_matrix.flags.writeable = True
    pic_matrix[0, :] = 0
    pic_matrix[-1, :] = 0
    pic_matrix[:, 0] = 0
    pic_matrix[:, -1] = 0
    pic_matrix[pic_matrix == 1] = 255
    return Image.fromarray(pic_matrix, 'L').show()


def cropImg(binarized_image):
    border = imgWordPartition(binarized_image, 20, 2)
    # gray, i = Image.open(r'C:\Users\super\Desktop\Captcha\c99.png'), 99

    pic_row = binarized_image.size[1]
    vol = []
    for c in border:
        if c[1] - c[0] in range(50, 100):
            vol.append(
                binarized_image.crop([c[0], 0, int((c[1] + c[0]) / 2), pic_row])
            )
            vol.append(
                binarized_image.crop([int((c[1] + c[0]) / 2), 0, c[1], pic_row])
            )
        # elif c[1]-c[0] >= 100:
        #     gray.crop([c[0], 0, int((c[1]+2*c[0])/3), pic_row]).save(save_dir % (i, idx))
        #     gray.crop([int((c[1]+2*c[0])/3), 0, int((2*c[1]+c[0])/3), pic_row]).save(save_dir % (i, idx+4))
        #     gray.crop([int((2*c[1]+c[0])/3), 0, c[1], pic_row]).save(save_dir % (i, idx+8))
        else:
            vol.append(
                binarized_image.crop([c[0], 0, c[1], pic_row])
            )
    return vol


def saveCroppedImg():
    save_dir = r'C:\Users\super\Desktop\Captcha\cropped\pic_%d_%d.png'
    img_dir = r'C:\Users\super\Desktop\Captcha\c%d.png'
    for i in range(120):
        gray = Image.open(img_dir % i)
        border = imgWordPartition(gray, 20, 2)
        # gray, i = Image.open(r'C:\Users\super\Desktop\Captcha\c99.png'), 99
        pic_matrix = np.asarray(gray)
        pic_row = pic_matrix.shape[0]

        for idx, c in enumerate(border):
            if c[1]-c[0] in range(50, 100):
                gray.crop([c[0], 0, int((c[1]+c[0])/2), pic_row]).save(save_dir % (i, idx))
                gray.crop([int((c[1]+c[0])/2), 0, c[1], pic_row]).save(save_dir % (i, idx+4))
            # elif c[1]-c[0] >= 100:
            #     gray.crop([c[0], 0, int((c[1]+2*c[0])/3), pic_row]).save(save_dir % (i, idx))
            #     gray.crop([int((c[1]+2*c[0])/3), 0, int((2*c[1]+c[0])/3), pic_row]).save(save_dir % (i, idx+4))
            #     gray.crop([int((2*c[1]+c[0])/3), 0, c[1], pic_row]).save(save_dir % (i, idx+8))
            else:
                cropped_img = gray.crop([c[0], 0, c[1], pic_row])
                cropped_img.save(save_dir % (i, idx))

                # gray.filter(ImageFilter.FIND_EDGES).show()
    test_img = Image.open(r'C:\Users\super\Desktop\Captcha\cropped\pic_57_2.png')


def ocr(binarized_image):
    container = cropImg(binarized_image)
    word = ''
    for w in container:
        word + pytesseract.image_to_string(
            rotatePadding(w)
                                           ).lower()
    return word


def saveRotatedImg():
    img_dir = r'C:\Users\super\Desktop\Captcha\cropped'
    save_dir = r'C:\Users\super\Desktop\Captcha\rotated\r%d.png'
    for idx, filename in enumerate(os.listdir(img_dir)):
        if 'pic' in filename:
            img = Image.open(img_dir+r'\%s' % filename)
            c = rotatePadding(img)
            c.save(save_dir % idx)

def showTaxCaptcha():
    path = MyPath().scriptpath
    captcha_url = 'https://www.tax.sh.gov.cn/xbwz/servlet/GetshowimgSmall'
    s = requests.session()
    bPic = s.get(captcha_url).content
    with open(file=path+r'\captcha.jpeg', mode='wb') as pic:
        pic.write(bPic)
        pic.close()
    Image.open(path+r'\captcha.jpeg').show()
    return s


def taxLogin(name):
    inspect_url1 = 'https://www.tax.sh.gov.cn/xbwz/wzfw/YhscxCtrl-yhsCx.pfv'
    header = {
        'Connection': 'keep-alive',
        'Content-Length': '41',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Host': 'www.tax.sh.gov.cn',
        'Origin': 'https://www.tax.sh.gov.cn',
        'Referer': 'https://www.tax.sh.gov.cn/xbwz/wzfw/YhscxCtrl-yhsCx.pfv',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like\
    Gecko) Chrome/63.0.3239.132 Safari/537.36 OPR/50.0.2762.67',
        'Cookies': 'JSESSIONID=lxSewBmKaJcAlyA6_6wXBY5UwM1sEJJM8id8wUz8co_ObA1uxwIs!-675922001; _gscu_1774520468=40261816gudqzy88; _gscbrs_1774520468=1; yfx_c_g_u_id_10003703=_ck18102310301614559554367015522; yfx_f_l_v_t_10003703=f_t_1540261816443__r_t_1540261816443__v_t_1540261816443__r_c_0; _gscs_1774520468=40261816hiy08b88|pv:2'
    }

    s = showTaxCaptcha()
    valid_code = input('Please set valid code: ')
    payload = {'shhtym': name, 'yzm': valid_code}
    content = s.post(inspect_url1, data=payload, headers=header).text
    login_status = '验证码' in content
    try_count = 1

    while login_status and try_count <= 2:
        s = showTaxCaptcha()
        valid_code = input('Please try again: ')
        payload = {'shhtym': name, 'yzm': valid_code}
        content = s.post(inspect_url1, data=payload, headers=header).text
        login_status = '验证码' in content
        try_count += 1
    return s, content


def taxInspect(name):
    session, content = taxLogin(name)
    inspect_url2 = 'https://www.tax.sh.gov.cn/xbwz/wzfw/YhscxCtrl-yhscxXx.pfv'
    info1 = soup(content, 'html.parser')
    try:
        label = str(info1.find_all('label'))
        label = re.findall("<label>(.*?)：*</label>", label)
        stat = str(info1.find_all('span')[3:13])
        stat = re.findall("<span>(.*?) *</span>", stat)

        reg_num = str(info1.find_all('div', attrs={'class': "moreDesc"}))
        reg_num = re.findall('value="(\d*)"', reg_num)[0]
        content = session.get(inspect_url2, params={'djxh': reg_num}).text

        label2 = re.findall("<label>(.*?)：</label>", content)
        stat2 = re.findall("<label>.*?：</label><span>(.*?)</span>", content)
        return label, stat, label2, stat2
    except:
        return -1, -1, -1, -1


def main():
    path = MyPath().scriptpath
    exl_path = input('Please set input excel path.\nMake sure columns 企业名称 and 税务证 are in the excel:\n')
    corp = pd.read_excel(exl_path).loc[:, ['企业名称', '税务证']]
    n = corp.shape[0]
    progress = 0
    # corp = corp.iloc[1249:]
    with open(path+r'\Inspect.csv', mode='a', encoding='utf-8') as csv_file:
        for i, row in corp.iterrows():
            num = row.loc['税务证']
            label, stat, label2, stat2 = taxInspect(num)

            if label != -1:
                name = stat[2]
                recog_num = stat[0]
                status = stat[4]
                tax_authority_idx = label2.index('主管税务机关')
                tax_admin_idx = label2.index('税务管理员')
                tax_authority = stat2[tax_authority_idx]
                tax_admin = stat2[tax_admin_idx]
            else:
                name = row.loc['企业名称']
                recog_num = row.loc['税务证']
                status = ''
                tax_authority = ''
                tax_admin = ''

            try:
                int(stat[0])
                csv_file.write("%s,'%s,%s,%s,%s\n" % (name, recog_num, status, tax_authority, tax_admin))
            except:
                csv_file.write("%s,%s,%s,%s,%s\n" % (name, recog_num, status, tax_authority, tax_admin))
            progress += 1
            print('\rProgress: %d/%d Total (%.2f%%). ' % (progress, n, 100*progress/n), end='')
    f = input('\nRecheck with company name? (y/n)\n')
    while f not in ['y', 'n']:
        f = input('Wrong input, please type y or n:')
    if f == 'y':
        print('Now rechecking...')
        recheck = pd.read_csv(path+r'\Inspect.csv')
        for i, row in recheck.iterrows():
            if pd.notnull(row[0]) and pd.isnull(row[2]):
                label, stat, label2, stat2 = taxInspect(row[0])
                if label != -1:
                    tax_authority_idx = label2.index('主管税务机关')
                    tax_admin_idx = label2.index('税务管理员')
                    tax_authority = stat2[tax_authority_idx]
                    tax_admin = stat2[tax_admin_idx]

                    recheck.iloc[i, 1] = stat[0]
                    recheck.iloc[i, 2] = stat[4]
                    recheck.iloc[i, 3] = tax_authority
                    recheck.iloc[i, 4] = tax_admin
                else:
                    pass
            else:
                pass

        recheck.columns = ['Corp_Name', 'Soci_Num', 'Status', 'Tax_Authority', 'Tax_Admin']
        recheck.to_excel(path+r'\Inspect-rechecked.xlsx', index=False)


if __name__ == '__main__':
    main()
