import io
import time
from typing import Union

import numpy
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image
import os
mtcnn = MTCNN(image_size=160, margin=0)
resnet = InceptionResnetV1(pretrained='vggface2').eval()
import torch

#计时装饰器：
#1.接收一个函数，对它进行修改(装饰)
def timeit_decorator(method):
    #2.定义一个 被 装饰的函数，返回这个函数对象
    def timed(*args,**kwargs):
        t1=time.time()
        res=method(*args,**kwargs)
        t2=time.time()
        print(f'calling {method.__name__} use time: {t2-t1} s')
        return res
    return timed


@timeit_decorator
def get_embedding(img_path:Union[str,io.BufferedReader])-> numpy.ndarray:
    img  = Image.open(img_path)

    with torch.no_grad():
        # Get cropped and prewhitened image tensor
        img_cropped = mtcnn(img)
        if img_cropped is None:
            raise  RuntimeError('cant find face')
        # Calculate embedding (unsqueeze to add batch dimension)
        img_embedding = resnet(img_cropped.unsqueeze(0))
        return img_embedding.numpy()





if __name__ == '__main__':
    import time
    jpg_paths = [os.path.join('data', name) for name in os.listdir('data')]
    t1=time.time()
    embeddings = [get_embedding(path) for path in jpg_paths]
    print((time.time()-t1)/len(embeddings))
