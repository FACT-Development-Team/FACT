import torch
from torchvision.transforms import ToTensor, Compose
import numpy as np

torch.set_default_dtype(torch.float64)

class IntegerDataset(torch.utils.data.Dataset):
	def __init__(self, x, y, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.x = x
		self.y = y
		self.transform = Compose([ ToTensor() ])

	def __getitem__(self, idx):
		if torch.is_tensor(idx):
			idx = idx.tolist()
		
		sample = [ self.x[idx], self.y[idx] ]
		# print(sample)
		#if self.transform:
		#	sample = self.transform(sample)
		return sample

	def __len__(self):
		return len(self.x)