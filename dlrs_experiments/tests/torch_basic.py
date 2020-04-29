import torch
import torchvision
import inspect

def get_version():
    """
    get version
    """
    function_name = inspect.currentframe().f_code.co_name
    version = (torchvision.__version__)
    print("Torchvision Version: " + version )
    if version == "0.5.0":
        ret = True
    else:
        ret = False
    print(function_name + " : " + str(bool(ret)))


def torchvision_models():
    """
    Construct a model with random weights by calling its constructor:
    """
    ret = True
    function_name = inspect.currentframe().f_code.co_name
    import torchvision.models as models
    resnet18 = models.resnet18()
    alexnet = models.alexnet()
    vgg16 = models.vgg16()

    print(function_name + " : " + str(bool(ret)))

def FastRCNNPredictor():
    """
    FastRCNNPredictor
    """
    ret = True
    function_name = inspect.currentframe().f_code.co_name
    from torchvision.models.detection.faster_rcnn import FastRCNNPredictor

    # load a model pre-trained pre-trained on COCO
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)

    # replace the classifier with a new one, that has
    # num_classes which is user-defined
    num_classes = 2  # 1 class (person) + background
    # get number of input features for the classifier
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    # replace the pre-trained head with a new one
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)

    print(function_name + " : " + str(bool(ret)))

def main():
    print("Basic Torchvision Test Cases:\n")
    get_version()
    torchvision_models()
    FastRCNNPredictor()

if __name__== "__main__":
  main()

