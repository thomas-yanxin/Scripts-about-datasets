import glob
import os
from PIL import Image
import math


def get_all_subfolders(path=None):
    if path:
        return [f.path for f in os.scandir(path) if f.is_dir()]
    return None


def resize_images(source, target_dimensions, destination, fruit_name):
    """
    Resizes with white padding and commutes an entire fruit directory to the specified dimensions
    The target destination must have the {width}x{height} directory already created
    :param source: path to the fruit in the raw dataset
    :param target_dimensions: an array containing all desired dimensions for the fruit
    :param destination: path to the resulted resized fruit
    :param fruit_name: name for the resulted fruit dir
    """
    images = glob.glob(source)
    for image in images:
        # Get Image Data
        img = Image.open(image)
        # Calculate ratios and differences between image dims
        dim_to_max = 1 * (img.size[1] / 16 > img.size[0] / 13)
        ratios = [img.size[1] / img.size[0], img.size[0] / img.size[1]]
        for dim in target_dimensions:
            img_copy = img.copy()
            # The image is definitely smaller than the target
            if img.size[0] < dim[0] and img.size[1] < dim[1]:
                new_sizes = [0, 0]
                new_sizes[dim_to_max] = dim[dim_to_max]
                new_sizes[(dim_to_max + 1) % 2] = math.floor(ratios[dim_to_max] * dim[dim_to_max])
                img_copy = img_copy.resize(tuple(new_sizes), Image.ANTIALIAS)
            # The image has at least one dimension bigger than the target
            else:
                img_copy.thumbnail(tuple(dim), Image.ANTIALIAS)
            # Create new blank image for resized image insertion
            new_img = Image.new("RGB", (dim[0], dim[1]), (255, 255, 255))
            new_img.paste(img_copy, ((dim[0] - img_copy.size[0]) // 2, (dim[1] - img_copy.size[1]) // 2))
            new_img.save(os.path.join(destination, f"{dim[0]}x{dim[1]}", fruit_name, os.path.basename(image)), "JPEG")


def mass_resize(directories, target_dimensions, destination):
    """
    Resizes multiple fruits on multiple dimensions and commutes the results to the destination
    :param directories: paths to all fruit directiories
    :param target_dimensions: array of multiple tuples of width x height dimensions
    :param destination: path for storing the output ( must have a directory named {width}x{height} for each dim pair
    """
    for dim in target_dimensions:
        os.makedirs(os.path.join(destination, f"{dim[0]}x{dim[1]}"))
        for directory in directories:
            os.makedirs(os.path.join(destination, f"{dim[0]}x{dim[1]}", os.path.basename(directory)))
    for directory in directories:
        print(os.path.basename(directory))
        resize_images(directory + "/*jpg", target_dimensions, destination, os.path.basename(directory))


if __name__ == '__main__':
    # Example for resizing on 224x224
    fruit_dirs = get_all_subfolders("./Fruit-262") # 原数据集地址
    mass_resize(fruit_dirs, [(224, 224)], "./ResizedDataset") # 处理后的数据集地址
