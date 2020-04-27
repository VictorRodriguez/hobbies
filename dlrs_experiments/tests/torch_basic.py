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
    if version == "0.6.0":
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

def torchvision_mean_std():
    """
    obtaining mean and std
    """
    ret = True
    from torchvision import datasets, transforms as T
    transform = T.Compose([T.Resize(256), T.CenterCrop(224), T.ToTensor()])
    dataset = datasets.ImageNet(".", split="train", transform=transform)

    means = []
    stds = []

    for img in subset(dataset):
        means.append(torch.mean(img))
        stds.append(torch.std(img))

    mean = torch.mean(torch.tensor(means))
    std = torch.mean(torch.tensor(stds))

    print(function_name + " : " + str(bool(ret)))

def main():
    print("Basic Torchvision Test Cases:\n")
    get_version()
    torchvision_models()
    torchvision_mean_std()

if __name__== "__main__":
  main()

