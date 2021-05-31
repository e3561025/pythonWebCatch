import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
from torch.autograd import Variable
import torchvision
from torchvision import datasets, models, transforms
from io import BytesIO
import os
from PIL import Image
import requests
class CheckR18:
    def __init__(self):
        self.model = torch.load('model2.pkl',map_location='cpu')
        self.data_transforms =transforms.Compose([
                    transforms.Scale(256),
                    transforms.CenterCrop(224),
                    transforms.ToTensor(),
                    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
                ])
    def checkR18(self,picList):
        num=0
        total=len(picList)
        for i in picList:
            im = Image.open(BytesIO(i))
            image_data=self.data_transforms(im)
            image_data=image_data.unsqueeze(dim=0)
            y=self.model(image_data)
            value = y.data.numpy()
            if (value[0,0]-value[0,1])<0:
                num+=1
        if total==0:
            #print('dsjlasjdlajsdlkjadljljadlasjdlajdlasjdd\n\n\n\n\n')
            return 10
        elif (num/total) > 0.1:
            return 0
        else:
            return 1
    