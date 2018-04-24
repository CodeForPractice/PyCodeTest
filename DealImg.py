# coding=utf-8
from PIL import Image
import os


def get_gray_binary_img(imgpath, threshold=140):
    image = Image.open(imgpath)
    imggray = image.convert('L')
    binary_table = get_binary_table(threshold=threshold)
    return imggray.point(binary_table, '1')


def get_binary_table(threshold=140):
    """
    获取灰度转二值的映射table
    :param threshold:
    :return:
    """

    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    return table


def clear_dot_point(gray_binary_img):
    for h in range(0, gray_binary_img.height):
        for w in range(0, gray_binary_img.width):
            if not (gray_binary_img.getpixel((w, h)) == 0):
                continue
            round_point = 0;
            min_h = h - 1
            if min_h < 0:
                min_h = 0
            max_h = h + 1
            if max_h > gray_binary_img.height - 1:
                max_h = gray_binary_img.height - 1
            min_w = w - 1
            if min_w < 0:
                min_w = 0
            max_w = w + 1
            if max_w > gray_binary_img.width - 1:
                max_w = gray_binary_img.width - 1
            for i in range(min_h, max_h + 1):
                for j in range(min_w, max_w + 1):
                    round_point += gray_binary_img.getpixel((j, i))
            if round_point == 8:
                gray_binary_img.putpixel((w, h), 1)

    return gray_binary_img


def split_img(gray_binary_img, img_list=[]):
    gray_binary_img_new = gray_binary_img
    round_point = None
    is_have = False
    for w in range(0, gray_binary_img_new.width):
        for h in range(0, gray_binary_img_new.height):
            if gray_binary_img_new.getpixel((w, h)) == 0:
                round_point = find_left_bound(gray_binary_img_new, w, h)
                is_have = True
                if check_point_avliable(gray_binary_img, round_point):
                    gray_binary_img_new_cut = gray_binary_img.crop((round_point[0], round_point[1], round_point[2] + 1, round_point[3] + 1))
                    img_list.append(gray_binary_img_new_cut)
                break
        if is_have:
            break
        # if is_have:

    if round_point is not None:
        gray_binary_img_fixed = fix_white(gray_binary_img_new, round_point)
        split_img(gray_binary_img_fixed, img_list=img_list)
    return img_list


def check_point_avliable(gray_binary_img, round_point):
    count_value = 0;
    for i in range(round_point[1], round_point[3] + 1):
        for j in range(round_point[0], round_point[2] + 1):
            count_value += gray_binary_img.getpixel((j, i))
    return (round_point[3] + 1 - round_point[1]) * (round_point[2] + 1 - round_point[0]) - count_value > 10


def fix_white(img, round_point):
    gray_binary_img = img
    for i in range(round_point[1], round_point[3] + 1):
        for j in range(round_point[0], round_point[2] + 1):
            gray_binary_img.putpixel((j, i), 1)
    return gray_binary_img


def find_left_bound(gray_binary_img, start_w, start_h, have_found_point_list=[]):
    next_node_top = start_h - 2
    next_node_left = start_w - 2
    # 左上右下
    result = [start_w, start_h, start_w + 1, start_h]
    have_found_point_list.append({start_w, start_h})
    for w in range(next_node_left, start_w + 3):
        for h in range(next_node_top, start_h + 3):
            if w >= 0 and h >= 0 and w < gray_binary_img.width and h < gray_binary_img.height:
                if start_w == w and start_h == h:
                    continue
                if {w, h} in have_found_point_list:
                    continue
                point_value = gray_binary_img.getpixel((w, h))
                if point_value == 0:
                    result_new = find_left_bound(gray_binary_img, w, h, have_found_point_list=have_found_point_list)
                    if result[0] > result_new[0]:
                        result[0] = result_new[0]
                    if result[1] > result_new[1]:
                        result[1] = result_new[1]
                    if result[2] < result_new[2]:
                        result[2] = result_new[2]
                    if result[3] < result_new[3]:
                        result[3] = result_new[3]
                    if result[0] > w:
                        result[0] = w
                    if result[1] > h:
                        result[1] = h
                    if result[2] < w:
                        result[2] = w
                    if result[3] < h:
                        result[3] = h
    return result


def print_point(gray_binary_img):
    for i in range(0, gray_binary_img.height):
        code = []
        for j in range(0, gray_binary_img.width):
            code.append(str(gray_binary_img.getpixel((j, i))))
        print "".join(code)


def deal_img(file_path, name):
    gray_binary_img = get_gray_binary_img(file_path)
    gray_binary_img_new = clear_dot_point(gray_binary_img)
    split_img_list = split_img(gray_binary_img_new, img_list=[])
    for index, split_img_info in enumerate(split_img_list):
        dir_path = './CodeImg/Split/' + name.replace(".jpg", "")
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        split_img_info.save(dir_path + "/" + str(index) + ".jpg")


if __name__ == "__main__":
    for root, dirs, files in os.walk('./CodeImg/Source'):
        # for file in files:
        #     print file.name
        for filename in files:
            if filename == '4.jpg':
                file_path = './CodeImg/Source/' + filename
                deal_img(file_path, filename)

        # print(root)  # 当前目录路径
        # print(dirs)  # 当前路径下所有子目录
        # print(files)  # 当前路径下所有非目录子文件
    # gray_binary_img = get_gray_binary_img('./CodeImg/Source/1.jpg')
    # gray_binary_img_new = clear_dot_point(gray_binary_img)
    # split_img_list = split_img(gray_binary_img_new)
    # for split_img in split_img_list:
    #     print_point(split_img)
    #     print '========================='

    # gray_binary_img_new.save('./CodeImg/New/1.jpg')
