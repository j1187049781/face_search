from time import time
from sklearn.neighbors import KDTree
import numpy as np
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image
import os
import itertools
import matplotlib.pyplot as plt
mtcnn = MTCNN(image_size=160, margin=0)
resnet = InceptionResnetV1(pretrained='vggface2').eval()
import torch

def get_embedding(img_path):
    img = Image.open(img_path)

    # Get cropped and prewhitened image tensor
    img_cropped = mtcnn(img)

    # Calculate embedding (unsqueeze to add batch dimension)
    img_embedding = resnet(img_cropped.unsqueeze(0))
    return img_embedding


def comp(img1, img2):

    img1 = torch.squeeze(img1)
    img2 = torch.squeeze(img2)
    product = torch.sum(img1 * img2)

    img1_normal = torch.sqrt(torch.sum(img1 * img1))
    img2_normal = torch.sqrt(torch.sum(img2 * img2))

    return product / (img1_normal * img2_normal)

def test1():
    jpg_paths = [os.path.join('data', name) for name in os.listdir('data')]
    embeddings = [get_embedding(path) for path in jpg_paths]
    plt.axis('off')
    t=0
    for (path1, embedding1), (path2, embedding3) in itertools.combinations(zip(jpg_paths, embeddings), 2):
        img1 = Image.open(path1)
        img2 = Image.open(path2)
        t1 = time()
        prob = comp(embedding1, embedding3)
        t2 = time()

        # t+=t2-t1
        if t2-t1>9e-5:
            print(t2 - t1)
        # print(f"t:{t}")
        if prob.item()>0.7:
            print(prob.item())

            # plt.subplot(121)
            # plt.imshow(img1)
            # plt.subplot(122)
            # plt.imshow(img2)
            # plt.show()
def test2():
    jpg_paths = [os.path.join('data', name) for name in os.listdir('data')]
    embeddings = [get_embedding(path) for path in jpg_paths]
    with torch.no_grad():
        t1 = time()
        vs=torch.cat(embeddings,dim=0)

        for q in embeddings:
            print(torch.nn.CosineSimilarity()(q,vs))
            # print(torch.sum(q*vs,dim=1))
        print(time()-t1)
if __name__ == '__main__':

    jpg_paths = [os.path.join('data', name) for name in os.listdir('data')]
    embeddings = [get_embedding(path) for path in jpg_paths]*300
    vs = torch.cat(embeddings, dim=0)
    print(vs.detach().numpy().shape)
    tree=KDTree(vs.detach().numpy(),metric='euclidean')
    t1=time()
    dist, ind = tree.query(vs.detach().numpy()[:1], k=3)
    print(time() - t1)