import torch
from torch import nn

import wandb
import device_decision

def train(model, dataloader, meta_config):
	device = device_decision.device

	# get optimizer from string
	optimizer = get_optimizer_from_string(model, meta_config.optimizer, lr=meta_config.lr)

	# training begins here
	size = len(dataloader.dataset)
	last_print_point = 0
	epoch_loss_total = 0

	model.train()
	lossobj = torch.nn.BCELoss()
	for batch, (X, y) in enumerate(dataloader):
		current_point = batch * len(X)
		X, y = X.to(device), y.to(device)

		# Compute prediction error
		pred = model(X)

		# print(pred)
		# print(y)
		loss_total = lossobj(pred, y)
		
		epoch_loss_total += loss_total
		
		# Backpropagation
		optimizer.zero_grad()
		loss_total.backward()
		optimizer.step()

		# Print progress at ~10 checkpoints
		if meta_config.verbosity >= 2 and current_point - last_print_point > size//10:
			last_print_point = current_point
			loss_total, current = loss_total.item(), batch * len(X)
			print(f" - loss: total {loss_total: >7.3f} [{current:>5d}/{size:>5d}]", end="\t\t\r")
	
	epoch_loss_total /= batch

	if meta_config.wandbosity >= 2:
		metrics = {
			'total_loss': epoch_loss_total,
		}
		wandb.log(metrics)

	if meta_config.verbosity >= 1:
		print('\x1b[2K', end="\r") # line clear
		print(
			f" - mean train loss: \t{epoch_loss_total: >7.3f}",
			end="\t\t\t\n"
		)

	return epoch_loss_total

def early_stopping(model, checkpointFilePath: str, validation_history: list, patience: int):
	least_validation_loss_in_history =  min(validation_history)

	if validation_history[-1] == least_validation_loss_in_history:
		torch.save(model.state_dict(), checkpointFilePath)

	if len(validation_history) < patience:
		return False

	should_stop_early = validation_history[-patience] == least_validation_loss_in_history
	return should_stop_early

def get_optimizer_from_string(model, optimizer_string: str, **kwargs):
	if optimizer_string == 'adam':
		optimizer = torch.optim.Adam(model.parameters(), **kwargs)
	elif optimizer_string == 'adamw':
		optimizer = torch.optim.AdamW(model.parameters(), **kwargs)
	elif optimizer_string == 'adadelta':
		optimizer = torch.optim.Adadelta(model.parameters(), **kwargs)
	elif optimizer_string == 'rmsprop':
		optimizer = torch.optim.RMSprop(model.parameters(), **kwargs)
	else:
		raise Exception(f"Uknown optimizer {optimizer_string}")

	return optimizer