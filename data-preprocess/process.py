# -*- coding: utf-8 -*-

import os
import json
import shutil

train_val_ratio = 4


def parse_json(file_path):
    with open(file_path, encoding='utf-8') as f:
        obj = json.load(f)
    f.close()
    return obj


def parse_category(root):
    #     load category information
    category_file = os.path.join(root, "categories.json")

    image2categories = parse_json(category_file)

    category_set = set()
    for image_name, category in image2categories.items():
        if category not in category_set:
            category_set.add(category)
    return image2categories, category_set


def make_corresponding_folder(root, category_set):
    train_folder = os.path.join(root, "classification_train")
    val_folder = os.path.join(root, "classification_val")

    if not os.path.exists(train_folder):
        os.mkdir(train_folder)
    if not os.path.exists(val_folder):
        os.mkdir(val_folder)

    # 创建类对应的文件夹
    for category in category_set:
        train_category_folder = os.path.join(train_folder, category)
        val_category_folder = os.path.join(val_folder, category)
        if not os.path.exists(train_category_folder):
            os.mkdir(train_category_folder)
        if not os.path.exists(val_category_folder):
            os.mkdir(val_category_folder)


def split_images(root, image2categories):
    """
    处理AI2D中的图像，把图像分成训练测试集，并划分到不同文件夹中
    :return:
    """
    train_folder = os.path.join(root, "classification_train")
    val_folder = os.path.join(root, "classification_val")
    images_path = os.path.join(root, 'images')

    for image_name, category in image2categories.items():
        src = os.path.join(images_path, image_name)
        dst = os.path.join(train_folder, category)
        shutil.copy(src, dst)

    # 移动图片到测试集中
    sub_folders = os.listdir(train_folder)
    for sub_folder in sub_folders:
        source_path = os.path.join(train_folder, sub_folder)
        dst_path = os.path.join(val_folder, sub_folder)
        image_names = os.listdir(source_path)
        mv_num = len(image_names) // (1 + train_val_ratio)
        for i in range(mv_num):
            src = os.path.join(source_path, image_names[i])
            dst = os.path.join(dst_path, image_names[i])
            shutil.move(src, dst)


def split_images2(root, image2categories):
    """
    处理AI2D中的图像，把图像分成训练测试集，并划分到不同文件夹中
    :return:
    """
    train_folder = os.path.join(root, "classification_train")
    val_folder = os.path.join(root, "classification_val")
    images_path = os.path.join(root, 'images')

    image_names = os.listdir(images_path)
    train_num = len(image_names) * 4 // 5

    i = 0
    for image_name, category in image2categories.items:
        if i < train_num:
            src = os.path.join(images_path, image_name)
            dst = os.path.join(train_folder, category)
            shutil.copy(src, dst)
        else:
            src = os.path.join(images_path, image_name)
            dst = os.path.join(val_folder, category)
            shutil.copy(src, dst)
        i += 1


def main():
    root = "/home/yangkuan/data/ai2d/"
    image2categories, categories = parse_category(root)
    make_corresponding_folder(root, categories)
    split_images2(root, image2categories)


if __name__ == '__main__':
    main()
