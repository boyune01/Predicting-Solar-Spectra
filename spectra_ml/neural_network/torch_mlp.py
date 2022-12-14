"""
Module to train deep neural network using PyTorch framework. It takes cleaned
weather data and manipulates it in torch tensors.
"""

import numpy as np
import torch
from torch import nn

# Load weather and radience data into arrays
X = np.loadtxt('data/input_cleaned/wea_input.csv', skiprows=1, delimiter=',', usecols=range(1, 14))
y = np.loadtxt('data/input_cleaned/rad_input.csv', skiprows=1, delimiter=',', usecols=range(1, 14))

# Check input dimensions
for i in [X, y]:
    print(type(i), i.shape)


class Perceptron(torch.nn.Module):
    """Initializes perceptron with ReLU activation function"""
    def __init__(self):
        super(Perceptron, self).__init__()
        self.fc = nn.Linear(1, 1)
        self.relu = torch.nn.ReLU()
    
    def forward(self, x):
        output = self.fc(x)
        output = self.relu(x)
        return output


class FeedForward(torch.nn.Module):
    """Defines forward feed object with (input_size) nodes and (hidden_size) layers"""
    def __init__(self, input_size, hidden_size):
        super(FeedForward, self).__init__()
        self.input_size = input_size
        self.hidden_size  = hidden_size
        self.fc1 = torch.nn.Linear(self.input_size, self.hidden_size)
        self.relu = torch.nn.ReLU()
        self.fc2 = torch.nn.Linear(self.hidden_size, 1)
        self.sigmoid = torch.nn.Sigmoid()
    def forward(self, x):
        hidden = self.fc1(x)
        relu = self.relu(hidden)
        output = self.fc2(relu)
        output = self.sigmoid(output)
        return output


class MLP(nn.Module):
    """Initialize multilayer perceptron for regression"""
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(13, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )


# Separate weather and radiance data into train and test with an 80-20 split
X_train_size = int(0.8 * len(X))
X_test_size = len(X) - X_train_size
y_train_size = int(0.8 * len(y))
y_test_size = len(y) - X_train_size
X_train, X_test = torch.utils.data.random_split(X, [X_train_size, X_test_size], generator=torch.Generator().manual_seed(1))
y_train, y_test = torch.utils.data.random_split(y, [y_train_size, y_test_size], generator=torch.Generator().manual_seed(1))

# Transform data to tensors
X_train = np.array(X_train)
X_test = np.array(X_test)
y_train = np.array(y_train)
y_test = np.array(y_test)

X_train = torch.FloatTensor(X_train)
X_test = torch.FloatTensor(X_test)
y_train = torch.FloatTensor(y_train)
y_test = torch.FloatTensor(y_test)

model = FeedForward(13, 2)
criterion = torch.nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr = 0.01)

model.eval()
y_pred = model(X_test)
dataset = torch.cat((X_train, y_train))
trainloader = torch.utils.data.DataLoader(dataset, batch_size=10, shuffle=True, num_workers=1)
mlp = MLP()

# Run the training loop
for epoch in range(0, 5): # 5 epochs at maximum

    # Print epoch
    print(f'Starting epoch {epoch + 1}')

    # Set current loss value
    current_loss = 0.0

    # Iterate over the DataLoader for training data
    for i, data in enumerate(trainloader, 0):

        # Get and prepare inputs
        inputs, targets = data
        inputs, targets = inputs.float(), targets.float()
        targets = targets.reshape((targets.shape[0], 1))

        # Zero the gradients
        optimizer.zero_grad()

        # Perform forward pass
        outputs = mlp(inputs)

        # Compute loss
        loss = criterion(outputs, targets)

        # Perform backward pass
        loss.backward()

        # Perform optimization
        optimizer.step()

        # Print statistics
        current_loss += loss.item()
        if i % 10 == 0:
            print('Loss after mini-batch %5d: %.3f' %
            (i + 1, current_loss / 500))
            current_loss = 0.0

# Training is complete.
print('Training process has finished.')
