from typing import Any

import cv2
import numpy as np
import torch
from PIL import Image
from torch import softmax
from torchvision import transforms

from controller.global_variables import GlobalVariables
from enums import MovementType, CommandKeys
from settings import MODEL_PATH, MODEL_INPUT_SIZE

global_variables = GlobalVariables()
mind_of_sheila = torch.load(MODEL_PATH, map_location='cpu')

index_to_movement_type = {0: MovementType.FORWARD,
                          1: MovementType.LEFT,
                          2: MovementType.RIGHT}

movement_to_press_key = {
    MovementType.FORWARD: "'w'",
    MovementType.BACKWARD: "'s'",
    MovementType.LEFT: "'a'",
    MovementType.RIGHT: "'d'"
}


def get_loader(image_size: int) -> Any:
    loader = transforms.Compose([transforms.Resize((image_size, image_size)),
                                 transforms.ToTensor(),
                                 transforms.Normalize([0.485, 0.456, 0.406],
                                                      [0.229, 0.224, 0.225])])
    return loader


def image_loader(image, image_size: int):
    loader = get_loader(image_size)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    image = loader(image).float().unsqueeze(0)
    return image


def get_predicted_class_and_accuracy(model: Any, image, image_size: int):
    image = image_loader(image, image_size)
    prediction = model(image)
    prediction = softmax(prediction, dim=1).detach().numpy()
    label_index = np.argmax(prediction)
    scores = prediction[0]
    percentage = scores[label_index]

    return label_index, round(percentage * 100, 2)


def get_command_from_autonomous_system(frame):
    index, accuracy = get_predicted_class_and_accuracy(mind_of_sheila, frame, MODEL_INPUT_SIZE)
    movement_type = index_to_movement_type[index]
    key = movement_to_press_key[movement_type]
    command = global_variables.command_builder.build_commands([key], autonomous=True)
    command[CommandKeys.ACCURACY] = accuracy
    return command
