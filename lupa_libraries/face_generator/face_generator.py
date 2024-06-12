"""
Module to create faces using the resources from the Kenney modular characters library.

Source of the assets : https://kenney.nl/assets/modular-characters
"""

##############
### Import ###
##############

### Python imports ###

import os
import sys
from typing import Literal
from functools import partial
from random import random, randrange
from math import sin, cos, pi

### Pillow imports ###

from PIL import Image, ImageOps

### Local imports ###

sys.path.append("./")
from image import get_image_size

#################
### Constants ###
#################

__version__ = "1.0.0"

### Paths ###

CURRENT_FOLDER = os.path.dirname(__file__)
RESOURCES_FOLDER = os.path.join(CURRENT_FOLDER, "resources")


### Image size ###

WIDTH = 250
HEIGHT = 250
IMAGE_SIZE = (WIDTH, HEIGHT)


### Skin ###

SKIN_FOLDER = os.path.join(RESOURCES_FOLDER, "skin")

SKIN_COLORS = [
    ("#ffe0b1", "#f5d29d"),
    ("#f5d29d", "#e7c38c"),
    ("#ffe9c9", "#ffe0b1"),
    ("#ffe0b1", "#d2ac73"),
    ("#d2ac73", "#bf9c66"),
    ("#bf9c66", "#aa8956"),
    ("#aa8956", "#957544"),
    ("#957544", "#836538"),
]

### Hair cut ###

HAIRCUT_MALE_Y_CENTER = HEIGHT * 82 / 250
HAIRCUT_FEMALE_Y_CENTER = HEIGHT * 165 / 250
HAIRCUT_Y_MAX_OFFSET = 7
HAIRCUT_MALE_FOLDER = os.path.join(RESOURCES_FOLDER, "men_hair")
HAIRCUT_FEMALE_FOLDER = os.path.join(RESOURCES_FOLDER, "women_hair")

HAIR_COLOR = [ # TODO supprimer maintenant
    "#3c3c3c",
    "#d7bf94",
    "#d7bf94",
    "#d7bf94",
    "#989898",
    "#d4946b",
    "#d4cbb9",
    "#e5e5e5"
]
HAIR_COLOR_FEMALE = [
    "#3c3c3c", # gray
    "#d7bf94", # light blond
    "#d4946b", # light brown
    "#160800", # black
    "#160800", # black
    "#160800", # black
    "#370d00", # dark brown
    "#370d00", # dark brown
    "#370d00", # dark brown
    "#ff5600", # ginger
    "#ff5600", # ginger
    "#ffab27", # blond
    "#ffab27", # blond
    "#ffab27", # blond
    "#a30000", # red
    "#e51364", # pink lupa
    "#247a91", # blue lupa
    "#7700db", # purple
    "#080072", # dark blue
    "#006e03", # green
]
HAIR_COLOR_MALE = [
    "#3c3c3c", # gray
    "#d7bf94", # light blond
    "#d4946b", # light brown
    "#160800", # black
    "#160800", # black
    "#160800", # black
    "#370d00", # dark brown
    "#370d00", # dark brown
    "#370d00", # dark brown
    "#612a00", # brown
    "#612a00", # brown
    "#ff5600", # ginger
    "#ff5600", # ginger
    "#ffab27", # blond
    "#ffab27", # blond
    "#ffab27", # blond
    "#a30000", # red
    "#247a91", # blue lupa
    "#080072", # dark blue
    "#006e03", # green
]

HAIRCUT_MALE_SHAPES = [name.replace(".png", "")
                       for name in os.listdir(HAIRCUT_MALE_FOLDER)]
HAIRCUT_FEMALE_SHAPES = [name.replace(".png", "")
                         for name in os.listdir(HAIRCUT_FEMALE_FOLDER)]

### Nose ###

NOSE_X_MAX_OFFSET = 5
NOSE_Y_MAX_OFFSET = 5
NODE_X_CENTER = WIDTH / 2
NODE_Y_CENTER = HEIGHT * 140 / 250
NOSE_FOLDER = os.path.join(RESOURCES_FOLDER, "nose")

NOSE_SHAPES = [name.replace(".png", "") for name in os.listdir(NOSE_FOLDER)]

### Eyebrow ###

EYEBROW_X_MAX_OFFSET = 5
EYEBROW_Y_MAX_OFFSET = 5
EYEBROW_ANGLE_MAX_DEV = 5
EYEBROW_X_DEFAULT_OFFSET = 30
EYEBROW_Y_CENTER = HEIGHT * 82 / 250
EYEBROW_FOLDER = os.path.join(RESOURCES_FOLDER, "eyebrow")

EYEBROW_SHAPES = [name.replace(".png", "")
                  for name in os.listdir(EYEBROW_FOLDER)]

### Mouth ###

MOUTH_X_MAX_OFFSET = 5
MOUTH_Y_MAX_OFFSET = 5
MOUTH_X_CENTER = WIDTH / 2
MOUTH_Y_CENTER = HEIGHT * 170 / 250
MOUTH_ANGLE_MAX_DEV = 5
MOUTH_FOLDER = os.path.join(RESOURCES_FOLDER, "mouth")

MOUTH_SHAPES = [name.replace(".png", "") for name in os.listdir(MOUTH_FOLDER)]

### Eyes ###

EYES_DEFAULT_SPACING = 64
EYES_MAX_VAR_SPACING = 8
EYES_X_MAX_OFFSET = 5
EYES_Y_MAX_OFFSET = 5
EYES_X_CENTER = WIDTH / 2
EYES_Y_CENTER = HEIGHT * 120 / 250
EYES_FOLDER = os.path.join(RESOURCES_FOLDER, "eye")

EYES_COLORS = [
    # "#4d4743",
    # "#395269",
    # "#694c39",
    # "#4c6939",
    # "#396962"
    "#612a00", # brown
    "#612a00", # brown
    "#612a00", # brown
    "#03661e", # green
    "#03661e", # green
    "#2c1000", # dark brown
    "#2c1000", # dark brown
    "#2c1000", # dark brown
    "#09005e", # dark blue
    "#09005e", # dark blue
    "#4e5141", # gray
    "#005ebb", # light blue
    "#006b40", # turquoise
    "#160800", # black
    "#160800" # black
]

EYES_SHAPES = [name.replace(".png", "") for name in os.listdir(EYES_FOLDER)]

### Face ###

FACE_FILE = os.path.join(SKIN_FOLDER, "face.png")
LOWER_FACE_FILE = os.path.join(SKIN_FOLDER, "lower_face.png")

### Body ###

BODY_Y_MAX_OFFSET = 7
NECK_Y_CENTER = HEIGHT * 210 / 250
SHIRT_Y_CENTER = HEIGHT * 283 / 250
ARM_Y_CENTER = HEIGHT * 262 / 250
NECK_FILE = os.path.join(SKIN_FOLDER, "neck.png")
CLOTHES_FOLDER = os.path.join(RESOURCES_FOLDER, "clothes")
SHIRT_FOLDER = os.path.join(CLOTHES_FOLDER, "shirt")
SHIRT_SHAPES = [name.replace(".png", "") for name in os.listdir(SHIRT_FOLDER)]

ARM_ANGLE = 28
ARM_X_OFFSET = WIDTH * 77 / 250
ARM_FILE = os.path.join(CLOTHES_FOLDER, "arm.png")

CLOTHES_COLOR = [
    ("#eeeeee", "#d2d2d2"), # white
    ("#63b448", "#529c39"), # green
    ("#16a085", "#108a72"), # turquoise
    ("#00305f", "#001933"), # dark blue
    ("#3498db", "#2a81bb"), # light blue
    ("#e05848", "#bf493b"), # red
    ("#95a5a6", "#7b8f91"), # grey
    ("#ffcc00", "#e7b900"), # yellow
    ("#ff9500", "#e77000"), # orange
    ("#5e00ff", "#3d00a5"), # purple
    ("#ff8ccc", "#ff63c2") # pink
]


#################
### Functions ###
#################


def random_interval(min_value: float, max_value: float):
    """
    Return a random float in the given interval.

    Parameters
    ----------
    min_value : float
        Min boundary.
    max_value : float
        Max boundary

    Returns
    -------
    float
        Random number in the given interval
    """

    res = random() * (max_value - min_value) + min_value

    return res


def random_select(input_list: list):
    """
    Select an item randomly in a list.

    Parameters
    ----------
    input_list : list
        List where to pick a random item.

    Returns
    -------
    Any
        Random element of the list.
    """

    element_id = randrange(len(input_list))
    element = input_list[element_id]

    return element

###############
### Classes ###
###############


class Part:

    position: tuple[int]
    image_src: str
    primary_color: tuple[int] | str = (1, 1, 1)
    secondary_color: tuple[int] | str = (0, 0, 0)

    def paste_on_image(
            self,
            image: Image.Image,
            h_flip: bool = False,
            angle: float | None = None,
            colorize: bool = True):
        """
        Paste the representation of the part on the given image.

        Parameters
        ----------
        image : Image.Image
            Image to use to paste the part.
        h_flip : bool
            Indicate whether to flip the part horizontally before pasting.
        angle : float | None
            Angle of rotation to apply to the part if not None.
        colorize : bool
            Indicate whether it is necessary to colorize the part.
        """

        # Open the source of the part
        part = Image.open(self.image_src)

        # Rotate if needed
        if angle is not None:
            part = part.rotate(angle, expand=True, resample=Image.BILINEAR)

        # Flip horizontally if needed
        if h_flip:
            part = ImageOps.mirror(part)

        # Colorize the part
        if colorize:
            part_colorized = part.convert("L")
            part_colorized = ImageOps.colorize(
                part_colorized, black=self.secondary_color, white=self.primary_color)
        else:
            part_colorized = part

        # Paste the part onto the image
        image.paste(part_colorized, self.position, mask=part)


class HairCut(Part):

    def __init__(
            self,
            color: tuple[int] | str,
            y_offset: float,
            shape: str,
            gender: Literal["male", "female"] = "male") -> None:

        self.primary_color = color
        self.secondary_color = color
        self.y_offset = y_offset

        if gender == "male":
            hair_folder = HAIRCUT_MALE_FOLDER
            hair_shapes = HAIRCUT_MALE_SHAPES
            self.haircut_y_center = HAIRCUT_MALE_Y_CENTER
        else:
            hair_folder = HAIRCUT_FEMALE_FOLDER
            hair_shapes = HAIRCUT_FEMALE_SHAPES
            self.haircut_y_center = HAIRCUT_FEMALE_Y_CENTER

        self.image_src = os.path.join(hair_folder, shape + ".png")

        # Verify that the image is in the database
        if shape not in hair_shapes:
            raise ValueError(
                f"The shape {shape} is not recognized for the hair with the gender {gender}.")

    @property
    def position(self) -> tuple[int]:
        # Get the size of the part
        part_width, part_height = get_image_size(self.image_src)

        x_pos = int(WIDTH / 2 - part_width / 2)
        self.y_offset = 0
        y_pos = int(self.haircut_y_center + self.y_offset - part_height / 2)

        return (x_pos, y_pos)


class Nose(Part):

    def __init__(
            self,
            color: tuple[int] | str,
            x_offset: float,
            y_offset: float,
            shape: str) -> None:

        self.primary_color = color
        self.secondary_color = color
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.image_src = os.path.join(
            NOSE_FOLDER, shape + ".png")

        # Verify that the image is in the database
        if shape not in NOSE_SHAPES:
            raise ValueError(
                f"The shape {shape} is not recognized for the nose.")

    @property
    def position(self) -> tuple[int]:
        # Get the size of the part
        part_width, part_height = get_image_size(self.image_src)

        x_pos = int(NODE_X_CENTER + self.x_offset - part_width / 2)
        y_pos = int(NODE_Y_CENTER + self.y_offset - part_height / 2)

        return (x_pos, y_pos)


class Eye(Part):

    def __init__(self, eyes, side: Literal["left", "right"]) -> None:
        self.eyes: Eyes = eyes
        self.side = side
        self.primary_color = self.eyes.color
        self.secondary_color = self.eyes.color
        self.image_src = self.eyes.image_src

        self.paste_on_image = partial(
            self.paste_on_image, h_flip=side == "right")

    @property
    def position(self) -> tuple[int]:

        # Attribute a sign for the offset depending on the side
        if self.side == "left":
            sign = -1
        else:
            sign = 1

        x_offset = self.eyes.x_offset + sign * self.eyes.eye_spacing / 2
        y_offset = self.eyes.y_offset

        part_width, part_height = get_image_size(self.image_src)

        x_pos = int(EYES_X_CENTER + x_offset - part_width / 2)
        y_pos = int(EYES_Y_CENTER + y_offset - part_height / 2)

        return (x_pos, y_pos)


class Eyes:

    def __init__(
            self,
            color: tuple[int] | str,
            eye_spacing: float,
            x_offset: float,
            y_offset: float,
            shape: str) -> None:

        self.x_offset = x_offset
        self.y_offset = y_offset
        self.eye_spacing = eye_spacing
        self.color = color
        self.image_src = os.path.join(
            EYES_FOLDER, shape + ".png")

        # Verify that the image is in the database
        if shape not in EYES_SHAPES:
            raise ValueError(
                f"The shape {shape} is not recognized for the eyes.")

        # Create the right and left eyes
        self.left_eye = Eye(self, side="left")
        self.right_eye = Eye(self, side="right")

    def paste_on_image(self, image: Image.Image):
        self.right_eye.paste_on_image(image)
        self.left_eye.paste_on_image(image)


class Eyebrow(Part):

    def __init__(
            self,
            angle: float,
            x_offset: float,
            y_offset: float,
            color: tuple[int] | str,
            shape: str,
            side: Literal["left", "right"]) -> None:

        self.x_offset = x_offset
        self.y_offset = y_offset
        self.side = side
        # if side == "left":
        #     self.angle = -angle
        # else:
        #     self.angle = angle
        self.angle = angle
        self.primary_color = color
        self.secondary_color = color
        self.image_src = os.path.join(
            EYEBROW_FOLDER, shape + ".png")

        # Verify that the image is in the database
        if shape not in EYEBROW_SHAPES:
            raise ValueError(
                f"The shape {shape} is not recognized for the eyebrows.")

        self.paste_on_image = partial(
            self.paste_on_image, angle=self.angle, h_flip=side == "right")

    @property
    def position(self) -> tuple[int]:

        # Attribute a sign for the offset depending on the side
        if self.side == "left":
            sign = -1
        else:
            sign = 1

        # Use the size of the rotated image instead of the size of the source image
        part_width, part_height = get_image_size(self.image_src)
        part_rot_width = part_width * \
            cos(self.angle / 180 * pi) + \
            part_height * abs(sin(self.angle / 180 * pi))
        part_rot_height = part_width * \
            abs(sin(self.angle / 180 * pi)) + \
            part_height * cos(self.angle / 180 * pi)

        x_pos = int(WIDTH / 2 + self.x_offset * sign - part_rot_width / 2)
        y_pos = int(EYEBROW_Y_CENTER + self.y_offset - part_rot_height / 2)

        return (x_pos, y_pos)


class Mouth(Part):

    def __init__(
            self,
            angle: float,
            x_offset: float,
            y_offset: float,
            shape: str) -> None:

        self.angle = angle
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.image_src = os.path.join(
            MOUTH_FOLDER, shape + ".png")

        # Verify that the image is in the database
        if shape not in MOUTH_SHAPES:
            raise ValueError(
                f"The shape {shape} is not recognized for the mouth.")

        self.paste_on_image = partial(
            self.paste_on_image, angle=self.angle, colorize=False)

    @property
    def position(self) -> tuple[int]:

        # Use the size of the rotated image instead of the size of the source image
        part_width, part_height = get_image_size(self.image_src)
        part_rot_width = part_width * \
            cos(self.angle / 180 * pi) + \
            part_height * abs(sin(self.angle / 180 * pi))
        part_rot_height = part_width * \
            abs(sin(self.angle / 180 * pi)) + \
            part_height * cos(self.angle / 180 * pi)

        x_pos = int(MOUTH_X_CENTER + self.x_offset - part_rot_width / 2)
        y_pos = int(MOUTH_Y_CENTER + self.y_offset - part_rot_height / 2)

        return (x_pos, y_pos)


class Face(Part):

    image_src = FACE_FILE

    def __init__(self, primary_color: tuple[int] | str, secondary_color: tuple[int] | str) -> None:
        self.primary_color = primary_color
        self.secondary_color = secondary_color

    @property
    def position(self) -> tuple[int]:

        # Get the size of the face image
        face_width, face_height = get_image_size(self.image_src)

        # Center the face on the image
        x_pos = int(WIDTH / 2 - face_width / 2)
        y_pos = int(HEIGHT / 2 - face_height / 2)

        return (x_pos, y_pos)


class Neck(Part):

    image_src = NECK_FILE

    def __init__(
            self,
            primary_color: tuple[int] | str,
            secondary_color: tuple[int] | str,
            y_offset: float) -> None:

        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.y_offset = y_offset

    @property
    def position(self) -> tuple[int]:

        # Get the size of the part
        part_width, part_height = get_image_size(self.image_src)

        # Center the part on the image
        x_pos = int(WIDTH / 2 - part_width / 2)
        y_pos = int(NECK_Y_CENTER + self.y_offset - part_height / 2)

        return (x_pos, y_pos)


class Shirt(Part):

    def __init__(
            self,
            primary_color: tuple[int] | str,
            secondary_color: tuple[int] | str,
            y_offset: float,
            shape: str) -> None:

        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.y_offset = y_offset

        self.image_src = os.path.join(
            SHIRT_FOLDER, shape + ".png")

        # Verify that the image is in the database
        if shape not in SHIRT_SHAPES:
            raise ValueError(
                f"The shape {shape} is not recognized for the shirt.")

    @property
    def position(self) -> tuple[int]:

        # Get the size of the part
        part_width, part_height = get_image_size(self.image_src)

        # Center the part on the image
        x_pos = int(WIDTH / 2 - part_width / 2)
        y_pos = int(SHIRT_Y_CENTER + self.y_offset - part_height / 2)

        return (x_pos, y_pos)


class Arm(Part):
    image_src = ARM_FILE

    def __init__(
            self,
            primary_color: tuple[int] | str,
            secondary_color: tuple[int] | str,
            y_offset: float,
            side: Literal["left", "right"]) -> None:

        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.y_offset = y_offset
        self.angle = -ARM_ANGLE
        self.side = side

        self.paste_on_image = partial(
            self.paste_on_image, angle=self.angle, h_flip=side == "right")

    @property
    def position(self) -> tuple[int]:

        # Attribute a sign for the offset depending on the side
        if self.side == "right":
            sign = -1
        else:
            sign = 1

        # Use the size of the rotated image instead of the size of the source image
        part_width, part_height = get_image_size(self.image_src)
        part_rot_width = part_width * \
            cos(self.angle / 180 * pi) + \
            part_height * abs(sin(self.angle / 180 * pi))
        part_rot_height = part_width * \
            abs(sin(self.angle / 180 * pi)) + \
            part_height * cos(self.angle / 180 * pi)

        # Center the part on the image
        x_pos = int(WIDTH / 2 + ARM_X_OFFSET * sign - part_rot_width / 2)
        y_pos = int(ARM_Y_CENTER + self.y_offset - part_rot_height / 2)

        return (x_pos, y_pos)


class Body:

    def __init__(
            self,
            skin_secondary_color: tuple[int] | str,
            clothes_primary_color: tuple[int] | str,
            clothes_secondary_color: tuple[int] | str,
            y_offset: float,
            shape: str) -> None:

        self.neck = Neck(
            primary_color=skin_secondary_color,
            secondary_color=skin_secondary_color,
            y_offset=y_offset
        )
        self.t_shirt = Shirt(
            primary_color=clothes_primary_color,
            secondary_color=clothes_secondary_color,
            y_offset=y_offset,
            shape=shape
        )
        self.left_arm = Arm(
            primary_color=clothes_primary_color,
            secondary_color=clothes_secondary_color,
            y_offset=y_offset,
            side="left"
        )
        self.right_arm = Arm(
            primary_color=clothes_primary_color,
            secondary_color=clothes_secondary_color,
            y_offset=y_offset,
            side="right"
        )

    def paste_on_image(self, image: Image.Image):
        self.neck.paste_on_image(image)
        self.left_arm.paste_on_image(image)
        self.right_arm.paste_on_image(image)
        self.t_shirt.paste_on_image(image)


class LowerFace(Face):

    image_src = FACE_FILE


class Portrait:

    def __init__(
            self,
            gender: Literal["male", "female"] | None = None,
            hair_color: tuple[int] | str | None = None,
            hair_y_offset: float | None = None,
            hair_shape: str | None = None,
            eyes_color: tuple[int] | str | None = None,
            eyes_x_offset: float | None = None,
            eyes_y_offset: float | None = None,
            eyes_spacing: float | None = None,
            eyes_shape: float | None = None,
            nose_x_offset: float | None = None,
            nose_y_offset: float | None = None,
            nose_shape: str | None = None,
            eyebrow_shape: str | None = None,
            eyebrow_x_offset: float | None = None,
            eyebrow_y_offset: float | None = None,
            eyebrow_angle: float | None = None,
            mouth_shape: str | None = None,
            mouth_x_offset: float | None = None,
            mouth_y_offset: float | None = None,
            mouth_angle: float | None = None,
            body_y_offset: float | None = None,
            clothes_color: tuple[tuple[int]] | tuple[str] | None = None,
            shirt_shape: str | None = None,
            skin_color: tuple[tuple[int]] | tuple[str] | None = None) -> None:

        # Set the gender
        if gender is None:
            gender = random_select(["male", "female"])
        self.gender = gender

        # Set the hair color
        if hair_color is None:
            if self.gender == "male":
                hair_color = random_select(HAIR_COLOR_MALE)
            else:
                hair_color = random_select(HAIR_COLOR_FEMALE)
        self.hair_color = hair_color

        # Set the haircut position
        if hair_y_offset is None:
            hair_y_offset = random_interval(-HAIRCUT_Y_MAX_OFFSET,
                                            HAIRCUT_Y_MAX_OFFSET)
        self.hair_y_offset = hair_y_offset

        # Set the hair shape
        if hair_shape is None:
            if gender == "male":
                hair_shape = random_select(HAIRCUT_MALE_SHAPES)
            else:
                hair_shape = random_select(HAIRCUT_FEMALE_SHAPES)
        self.hair_shape = hair_shape

        # Set the skin color
        if skin_color is None:
            skin_color = random_select(SKIN_COLORS)
        self.skin_color = skin_color

        # Set the eyes color
        if eyes_color is None:
            eyes_color = random_select(EYES_COLORS)
        self.eyes_color = eyes_color

        # Set the eyes shape
        if eyes_shape is None:
            eyes_shape = random_select(EYES_SHAPES)
        self.eyes_shape = eyes_shape

        # Set the eyes position
        if eyes_x_offset is None:
            eyes_x_offset = random_interval(-EYES_X_MAX_OFFSET,
                                            EYES_X_MAX_OFFSET)
        self.eyes_x_offset = eyes_x_offset
        if eyes_y_offset is None:
            eyes_y_offset = random_interval(-EYES_Y_MAX_OFFSET,
                                            EYES_Y_MAX_OFFSET)
        self.eyes_y_offset = eyes_y_offset

        # Set the eyes spacing
        if eyes_spacing is None:
            eyes_spacing = random_interval(-EYES_MAX_VAR_SPACING,
                                           EYES_MAX_VAR_SPACING) + EYES_DEFAULT_SPACING
        self.eyes_spacing = eyes_spacing

        # Set the nose position
        if nose_x_offset is None:
            nose_x_offset = random_interval(-NOSE_X_MAX_OFFSET,
                                            NOSE_X_MAX_OFFSET)
        self.nose_x_offset = nose_x_offset
        if nose_y_offset is None:
            nose_y_offset = random_interval(-NOSE_Y_MAX_OFFSET,
                                            NOSE_Y_MAX_OFFSET)
        self.nose_y_offset = nose_y_offset

        # Set the nose shape
        if nose_shape is None:
            nose_shape = random_select(NOSE_SHAPES)
        self.nose_shape = nose_shape

        # Set the eyebrow shape
        if eyebrow_shape is None:
            eyebrow_shape = random_select(EYEBROW_SHAPES)
        self.eyebrow_shape = eyebrow_shape

        # Set the eyebrow angle
        if eyebrow_angle is None:
            eyebrow_angle = random_interval(-EYEBROW_ANGLE_MAX_DEV,
                                            EYEBROW_ANGLE_MAX_DEV)
        self.eyebrow_angle = eyebrow_angle

        # Set the eyebrow position
        if eyebrow_x_offset is None:
            eyebrow_x_offset = random_interval(-EYEBROW_X_MAX_OFFSET,
                                               EYEBROW_X_MAX_OFFSET) + EYEBROW_X_DEFAULT_OFFSET
        self.eyebrow_x_offset = eyebrow_x_offset
        if eyebrow_y_offset is None:
            eyebrow_y_offset = random_interval(-EYEBROW_Y_MAX_OFFSET,
                                               EYEBROW_Y_MAX_OFFSET)
        self.eyebrow_y_offset = eyebrow_y_offset

        # Set the mouth shape
        if mouth_shape is None:
            mouth_shape = random_select(MOUTH_SHAPES)
        self.mouth_shape = mouth_shape

        # Set the mouth angle
        if mouth_angle is None:
            mouth_angle = random_interval(-MOUTH_ANGLE_MAX_DEV,
                                          MOUTH_ANGLE_MAX_DEV)
        self.mouth_angle = mouth_angle

        # Set the mouth position
        if mouth_x_offset is None:
            mouth_x_offset = random_interval(-MOUTH_X_MAX_OFFSET,
                                             MOUTH_X_MAX_OFFSET)
        self.mouth_x_offset = mouth_x_offset
        if mouth_y_offset is None:
            mouth_y_offset = random_interval(-MOUTH_Y_MAX_OFFSET,
                                             MOUTH_Y_MAX_OFFSET)
        self.mouth_y_offset = mouth_y_offset

        # Set the position of the body
        if body_y_offset is None:
            body_y_offset = random_interval(-BODY_Y_MAX_OFFSET,
                                            BODY_Y_MAX_OFFSET)
        self.body_y_offset = body_y_offset

        # Set the clothes color
        if clothes_color is None:
            clothes_color = random_select(CLOTHES_COLOR)
        self.clothes_color = clothes_color

        # Set the shirt shape
        if shirt_shape is None:
            shirt_shape = random_select(SHIRT_SHAPES)
        self.shirt_shape = shirt_shape

    def export_as_dict(self) -> dict:
        """
        Export the portrait as a dictionary.

        Returns
        -------
        dict
            Dictionary representing the portrait.
        """

    def export_as_png(self, export_path: str):
        """
        Generate the image of the portrait.

        Parameters
        ----------
        export_path : str
            Path to export the image.
        """

        # Create an empty image
        image = Image.new("RGBA", IMAGE_SIZE, color=(0, 0, 0, 0))

        # Add the face
        face = Face(
            primary_color=self.skin_color[0],
            secondary_color=self.skin_color[1])
        face.paste_on_image(image)

        # Add the haircut
        haircut = HairCut(
            y_offset=self.hair_y_offset,
            shape=self.hair_shape,
            color=self.hair_color,
            gender=self.gender)
        haircut.paste_on_image(image)

        # Add the body
        body = Body(
            skin_secondary_color=self.skin_color[1],
            clothes_primary_color=self.clothes_color[0],
            clothes_secondary_color=self.clothes_color[1],
            y_offset=self.body_y_offset,
            shape=self.shirt_shape)
        body.paste_on_image(image)

        # Add the lower face
        lower_face = LowerFace(
            primary_color=self.skin_color[0],
            secondary_color=self.skin_color[1])
        lower_face.paste_on_image(image)

        # Add the eyes
        eyes = Eyes(
            color=self.eyes_color,
            eye_spacing=self.eyes_spacing,
            x_offset=self.eyes_x_offset,
            y_offset=self.eyes_y_offset,
            shape=self.eyes_shape)
        eyes.paste_on_image(image)

        # Add the eyebrows
        left_eyebrow = Eyebrow(
            angle=self.eyebrow_angle,
            x_offset=self.eyebrow_x_offset,
            y_offset=self.eyebrow_y_offset,
            color=self.hair_color,
            shape=self.eyebrow_shape,
            side="left"
        )
        left_eyebrow.paste_on_image(image)
        right_eyebrow = Eyebrow(
            angle=self.eyebrow_angle,
            x_offset=self.eyebrow_x_offset,
            y_offset=self.eyebrow_y_offset,
            color=self.hair_color,
            shape=self.eyebrow_shape,
            side="right"
        )
        right_eyebrow.paste_on_image(image)

        # Add the nose
        nose = Nose(
            x_offset=self.nose_x_offset,
            y_offset=self.nose_y_offset,
            shape=self.nose_shape,
            color=self.skin_color[1])
        nose.paste_on_image(image)

        # Add the mouth
        mouth = Mouth(
            angle=self.mouth_angle,
            x_offset=self.mouth_x_offset,
            y_offset=self.mouth_y_offset,
            shape=self.mouth_shape)
        mouth.paste_on_image(image)

        # Save the image
        image.save(export_path)


if __name__ == "__main__":
    for i in range(100):
        portrait = Portrait()
        portrait.export_as_png(os.path.join(CURRENT_FOLDER, f"draft/{i}.png"))
