from django.apps import AppConfig
import fasttext
import torch


class AppConfig(AppConfig):
    name = 'app'
    print("Loading Fasttext model in app config...")
    word_embedding = fasttext.load_model("/home/parth/College/BE_Project/BEProj/gallery/app/wiki.en.bin")
    print("Fasttext model loaded.")
    print("Loading fashion model in app config")
    device = torch.device('cpu')
    fashion_model = torch.load("/home/parth/College/BE_Project/BEProj/gallery/app/tagan/fashion_models/birds_G (11).pth", map_location=device)
    print("Loading bird model in app config")
    birds_model = torch.load("/home/parth/College/BE_Project/BEProj/gallery/app/tagan/birds_model/birds_G.pth", map_location=device)
