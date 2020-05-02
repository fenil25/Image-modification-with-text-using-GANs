from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.db.models import Max

from django.core.files import File

from app.models import Edit
from app.forms import EditForm, OldEditForm
from app import views
from gallery import settings

from .apps import AppConfig

# DL libraries
import os
from .tagan.model import Generator

import torch
import torchfile

import torchvision.transforms as transforms
from torchvision.utils import save_image
from PIL import Image

import fasttext
import nltk
from nltk.tokenize import RegexpTokenizer

import matplotlib.pyplot as plt

# word_embedding = fasttext.load_model("/home/parth/College/BE_Project/BEProj/gallery/app/wiki.en.bin")

def split_sentence_into_words(sentence):
	tokenizer = RegexpTokenizer(r'\w+')
	return tokenizer.tokenize(sentence.lower())

transform_image = transforms.Compose([
	transforms.Resize(136),
	transforms.CenterCrop(128),
	transforms.ToTensor()
])

def _nums2chars(nums):
	alphabet = "abcdefghijklmnopqrstuvwxyz0123456789-,;.!?:'\"/\\|_@#$%^&*~`+-=<>()[]{} "
	chars = ''
	for num in nums:
		chars += alphabet[num - 1]
	return chars

def bird_model(original, text):
	device = torch.device('cpu')
	print("Original:", original, "Text:", text)
	G = Generator(fusing_method='lowrank_BP').to(device)
	G.load_state_dict(AppConfig.birds_model)
	_ = G.eval()
	img = Image.open(original)
	img = transform_image(img)
	img = img.unsqueeze(0)
	img = img.mul(2).sub(1).to('cpu')
	
	words = split_sentence_into_words(text)
	txt = torch.tensor([AppConfig.word_embedding.get_word_vector(w) for w in words], device='cpu')
	txt = txt.unsqueeze(1)
	len_txt = torch.tensor([len(words)], dtype=torch.long, device='cpu')

	output, _ = G(img, (txt, len_txt))
	output = output.mul(0.5).add(0.5)

	# plt.imshow(img.add(1).div(2).to('cpu').numpy()[0].transpose(1,2,0))
	# plt.imshow(output.to('cpu').detach().numpy()[0].transpose(1,2,0))
	# output = output.to('cpu').detach().numpy()[0].transpose(1, 2, 0)
	# temp = transforms.ToPILImage()
	save_image(img.add(1).div(2), "/home/parth/College/BE_Project/BEProj/gallery/app/bird_temp.jpg")
	save_image(output, "/home/parth/College/BE_Project/BEProj/gallery/app/temp.jpg")
	return None

def fashion_model(original, text):
	device = torch.device('cpu')
	print("Original:", original, "Text:", text)
	G = Generator(fusing_method='lowrank_BP').to(device)
	G.load_state_dict(AppConfig.fashion_model)
	_ = G.eval()
	img = Image.open(original)
	img = transform_image(img)
	img = img.unsqueeze(0)
	img = img.mul(2).sub(1).to('cpu')

	words = split_sentence_into_words(text)
	txt = torch.tensor([AppConfig.word_embedding.get_word_vector(w) for w in words], device='cpu')
	txt = txt.unsqueeze(1)
	len_txt = torch.tensor([len(words)], dtype=torch.long, device='cpu')

	output, _ = G(img, (txt, len_txt))
	output = output.mul(0.5).add(0.5)

	# plt.imshow(img.add(1).div(2).to('cpu').numpy()[0].transpose(1,2,0))
	# plt.imshow(output.to('cpu').detach().numpy()[0].transpose(1,2,0))
	# output = output.to('cpu').detach().numpy()[0].transpose(1, 2, 0)
	# temp = transforms.ToPILImage()
	save_image(output, "/home/parth/College/BE_Project/BEProj/gallery/app/temp.jpg")
	return None
	# return original


def transform(request):
# Handle file upload
	if request.method == 'POST':
		print("Transform POST")
		form = EditForm(request.POST, request.FILES)
		if form.is_valid():
			dataset = request.POST['dataset']
			num_id = Edit.objects.filter(dataset = dataset).aggregate(Max('num_id')).get('num_id__max')
			if num_id == None:
				num_id = 1
			else:
				num_id += 1
			desc = request.POST['desc']
			original = request.FILES['original']
			result = original
			new_edit = Edit(num_id = num_id, dataset = dataset, desc = desc, original = original, result = result)
			new_edit.save()
			
			if dataset == 'bird':
				result = bird_model(original, desc)
				new_edit.original.save(
					new_edit.original.url,
					File(open("/home/parth/College/BE_Project/BEProj/gallery/app/bird_temp.jpg", 'rb'))
				)
			
			else:
				result = fashion_model(original, desc)
			
			new_edit.result.save(
				new_edit.result.url,
				File(open("/home/parth/College/BE_Project/BEProj/gallery/app/temp.jpg", 'rb'))
			)
			new_edit.save()

			# Redirect to the document list after POST
			return HttpResponseRedirect(reverse(views.transform))
	else:
		print("Transform GET")
		form = EditForm()
		try:	
			last_edit = Edit.objects.latest('id')
			return render(request, 'app/form.html', {'last_edit': last_edit, 'form': form})
		except Exception as e:
			print(e)
			return render(request, 'app/form.html', {'form': form})


def transform_old(request, id, side):
	x = Edit.objects.get(id = id)
	field_object = Edit._meta.get_field(side)
	field_value = field_object.value_from_object(x)
	if request.method == 'POST':
		print("OLD POST")
		form = OldEditForm(request.POST)
		if form.is_valid():
			dataset = x.dataset
			num_id = Edit.objects.filter(dataset = dataset).aggregate(Max('num_id')).get('num_id__max')
			if num_id == None:
				num_id = 1
			else:
				num_id += 1
			desc = request.POST['desc']
			original = field_value
			result = original
			new_edit = Edit(num_id = num_id, dataset = dataset, desc = desc, original = original, result = result)
			new_edit.save()
			if dataset == 'bird':
				result = bird_model(original, desc)
			else:
				result = fashion_model(original, desc)
			new_edit.result = result
			new_edit.save()
			print('Old edit saved')
			return HttpResponseRedirect(reverse(views.transform))
	else:
		form = OldEditForm()
		img = field_value
		return render(request, 'app/old_edit.html', {'old': img, 'form': form, 'id': id, 'side': side})


def index(request):
	return render(request, 'app/index.html')


def list(request, dataset):
	return render(request, 'app/list.html', {'pairs': Edit.objects.filter(dataset = dataset).order_by('-num_id')})
