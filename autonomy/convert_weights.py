from fastai.vision import *


def save_function(model, save_model_path):
    model.precompute = False
    model = model.model
    model[0].bs = 1
    model.eval()

    torch.save(model, save_model_path)


if __name__ == '__main__':
    import os

    print(os.getcwd())
    data = ImageDataBunch.from_folder(path="autonomy/data", size=224, bs=1).normalize(imagenet_stats)
    learn = cnn_learner(data, models.resnet18, metrics=error_rate)
    learn.load("sheila_0.897333")
    save_function(learn, "weights/sheila_88.7_v_0_2.pth")
