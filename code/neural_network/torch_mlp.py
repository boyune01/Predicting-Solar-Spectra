import torch
from torch import nn
import numpy as np

X = np.loadtxt('data/input_cleaned/wea_input.csv', skiprows=1, delimiter=',', usecols=range(1, 14))
y = np.loadtxt('data/input_cleaned/rad_input.csv', skiprows=1, delimiter=',', usecols=range(1, 14))

for i in [X, y]:
    print(type(i), i.shape)

class Perceptron(torch.nn.Module):
    def __init__(self):
        super(Perceptron, self).__init__()
        self.fc = nn.Linear(1,1)
        self.relu = torch.nn.ReLU()
    def forward(self, x):
        output = self.fc(x)
        output = self.relu(x)
        return output

class FeedForward(torch.nn.Module):
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

X_train_size = int(0.8 * len(X))
X_test_size = len(X) - X_train_size
y_train_size = int(0.8 * len(y))
y_test_size = len(y) - X_train_size
X_train, X_test = torch.utils.data.random_split(X, [X_train_size, X_test_size])
y_train, y_test = torch.utils.data.random_split(y, [y_train_size, y_test_size])

model = FeedForward(2, 10)
optimizer = torch.optim.SGD(model.parameters(), lr = 0.01)
# criterion = torch.nn.BCELoss()

# model.eval()
# y_pred = model(X_test)
# before_train = criterion(y_pred.squeeze(), y_test)
# print('Test loss before training' , before_train.item())

# train_data, test_data = torch.utils.data.random_split(X, y)
# test_tensor = torch.tensor(X)
# train_dataset, test_dataset = torch.utils.data.random_split(full_dataset, [train_size, test_size])