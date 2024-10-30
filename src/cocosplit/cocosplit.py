import json

import funcy
import numpy as np
from sklearn.model_selection import train_test_split
from skmultilearn.model_selection import iterative_train_test_split


def save_coco(
    file_path, info, licenses, images, annotations, categories
):  # pylint: disable=missing-function-docstring
    with open(file_path, "wt", encoding="UTF-8") as coco:
        json.dump(
            {
                "info": info,
                "licenses": licenses,
                "images": images,
                "annotations": annotations,
                "categories": categories,
            },
            coco,
            indent=2,
            sort_keys=True,
        )


def filter_annotations(
    annotations, images
):  # pylint: disable=missing-function-docstring
    image_ids = funcy.lmap(lambda i: int(i["id"]), images)
    return funcy.lfilter(lambda a: int(a["image_id"]) in image_ids, annotations)


def filter_images(images, annotations):  # pylint: disable=missing-function-docstring

    annotation_ids = funcy.lmap(lambda i: int(i["image_id"]), annotations)

    return funcy.lfilter(lambda a: int(a["id"]) in annotation_ids, images)


def split_coco_json(
    source_coco_json_path: str,
    output_train_coco_json_path: str,
    output_test_coco_json_path: str,
    split_size: float = 0.8,
    is_stratified: bool = True,
):  # pylint: disable=missing-function-docstring

    with open(source_coco_json_path, "rt", encoding="UTF-8") as annotations:
        coco = json.load(annotations)
        info = coco["info"]
        licenses = coco["licenses"]
        images = coco["images"]
        annotations = coco["annotations"]
        categories = coco["categories"]

        if is_stratified:

            annotation_categories = funcy.lmap(
                lambda a: int(a["category_id"]), annotations
            )

            # bottle neck 1
            # remove classes that has only one sample, because it can't be split into the training and testing sets
            annotation_categories = funcy.lremove(
                lambda i: annotation_categories.count(i) <= 1, annotation_categories
            )

            annotations = funcy.lremove(
                lambda i: i["category_id"] not in annotation_categories, annotations
            )

            x_train, _, x_test, _ = iterative_train_test_split(
                np.array([annotations]).T,
                np.array([annotation_categories]).T,
                test_size=1 - split_size,
            )

            save_coco(
                output_train_coco_json_path,
                info,
                licenses,
                filter_images(images, x_train.reshape(-1)),
                x_train.reshape(-1).tolist(),
                categories,
            )
            save_coco(
                output_test_coco_json_path,
                info,
                licenses,
                filter_images(images, x_test.reshape(-1)),
                x_test.reshape(-1).tolist(),
                categories,
            )

            print(
                f"Saved {len(x_train)} entries in {output_train_coco_json_path} and {len(x_test)} in {output_test_coco_json_path}"
            )

        else:

            x_train, x_test = train_test_split(images, train_size=split_size)

            anns_train = filter_annotations(annotations, x_train)
            anns_test = filter_annotations(annotations, x_test)

            save_coco(
                output_train_coco_json_path,
                info,
                licenses,
                x_train,
                anns_train,
                categories,
            )
            save_coco(
                output_test_coco_json_path,
                info,
                licenses,
                x_test,
                anns_test,
                categories,
            )

            print(
                f"Saved {len(anns_train)} entries in {output_train_coco_json_path} and {len(anns_test)} in {output_test_coco_json_path}"
            )
