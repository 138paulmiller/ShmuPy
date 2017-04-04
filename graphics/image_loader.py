import os
import graphics


def load_image_file(img_file):
    return graphics.pygame.image.load(os.path.realpath(img_file)).convert_alpha()


def load_images(root_dir):
    images = {}
    if root_dir:
        for dir_name, subdir_list, file_list in os.walk(os.path.realpath(root_dir),topdown=False):  # do not travers . and ..
            for subdir in subdir_list:
                images.update(load_images(subdir))
            for file_name in file_list:
                images[file_name] = load_image_file('{}/{}'.format(dir_name, file_name))
    return images

