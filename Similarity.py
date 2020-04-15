import binascii
import os
import shelve

import torch
from sklearn.neighbors import KDTree
from Embedding import get_embedding

import numpy as np
import io
from typing import Union,Tuple


class Similarity:
    def __init__(self):
        self.SIM_T=0.7
        self.serialized_persons_info='./serialized_person_data.dat'
        self.shelf=shelve.open(self.serialized_persons_info)

        self.build_kdtree()

    def __del__(self):
        if self.shelf:
            self.shelf.close()

    def build_kdtree(self):
        self.cache_info_dict = {}
        self.build_kttree_id = list(self.shelf.keys())
        if self.build_kttree_id:
            self.kdtree = KDTree(np.concatenate(list(self.shelf.values()), axis=0), metric='euclidean')

        else:
            self.kdtree=None


    def add_person(self,image_fp:Union[str,io.BufferedReader],duplicate_person=False)->Tuple[bool,str]:
        if duplicate_person:
            find_res=self.find_person(image_fp)
            if find_res:
                person_id, sim=find_res
                return False,person_id
        person_id = binascii.b2a_hex(os.urandom(15)).decode()
        embedding = get_embedding(image_fp)
        self.shelf[person_id]=embedding
        self.cache_info_dict[person_id]=embedding
        return True,person_id


    def rm_person(self,person_id:str)->bool:
        if person_id in self.shelf.keys():
            del self.shelf[person_id]
            self.build_kdtree()
            return True
        if person_id in self.cache_info_dict.keys():
            del self.shelf[person_id]
            self.build_kdtree()
            return True
        return False

    def find_person(self,image_path:Union[str,io.BufferedReader])->Tuple[str,float]:
        q=get_embedding(image_path)
        assert q.shape==(1,512)
        if self.kdtree:
            dist, ind = self.kdtree.query(q, k=1)
            ind=ind[0]
        else:
            ind=[]
        ids=[self.build_kttree_id[i] for i in ind]
        embeddings=[self.shelf[k] for k in ids]

        ids=list(self.cache_info_dict.keys())+ids
        embeddings=list(self.cache_info_dict.values())+embeddings

        face_embeddings_tensor=[torch.tensor(arr) for arr in embeddings]
        if not face_embeddings_tensor :
            return None

        embeddings_tensor = torch.cat([torch.tensor(arr) for arr in embeddings], dim=0)
        cos_sim_tensor=torch.nn.CosineSimilarity()(torch.tensor(q), embeddings_tensor)
        max_sim_index_tensor=torch.argmax(cos_sim_tensor)
        max_sim_tensor=cos_sim_tensor[max_sim_index_tensor]
        person_id,face_sim=ids[max_sim_index_tensor.numpy()],float(max_sim_tensor.numpy())
        return (person_id,face_sim) if face_sim> self.SIM_T else None

if __name__ == '__main__':
    data_dir='ffhq'
    import glob
    img_paths=glob.glob(os.path.join(data_dir,'./*'))
    sim=Similarity()
    for img_path in img_paths[:10]:
        sim.add_person(img_path)
    print(sim.find_person(img_paths[1]))
    sim.rm_person('da2beae044a32c65ce82e6bc2a9503')
