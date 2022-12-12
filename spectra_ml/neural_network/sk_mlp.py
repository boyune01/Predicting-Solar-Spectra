import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('pdf')
import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split

# Load weather and radience data into arrays
X = np.loadtxt('data/input_cleaned/wea_input.csv', skiprows=1, delimiter=',', usecols=range(1, 14))
y = np.loadtxt('data/input_cleaned/rad_input.csv', skiprows=1, delimiter=',', usecols=range(1, 14))

for i in [X, y]:
    print(type(i), i.shape)

# Perform 80-20 train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=1)

# Initialize neural network with two 64-node hidden layers
reg = MLPRegressor(hidden_layer_sizes=(64, 64), activation='relu', random_state=1, max_iter=1000, early_stopping=True).fit(X_train, y_train)
pred = reg.predict(X_test)
print("Prediction shape:", pred.shape)
acc = reg.score(X_test, y_test)
print(acc)

# Save training loss plot to root directory
fig, ax = plt.subplots()
plt.plot(reg.loss_curve_, label='Training')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('MLP Regression Training Loss Plot')
plt.legend()
plt.savefig('mlp_train_loss.png')

# Save validation loss plot to root directory
fig, ax = plt.subplots()
reg.fit(X_test, y_test)
plt.plot(reg.loss_curve_, label='Validation', color='orange')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('MLP Regression Validation Loss Plot')
plt.legend()
plt.savefig('mlp_valid_loss.png')

# Alternative implementation with both curves on same plot
"""
fig, ax = plt.subplots()
plt.plot(reg.loss_curve_, label='Training')
plt.plot(reg.validation_scores_, label='Validation')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('MLP Regression Loss Plot')
plt.legend()
plt.savefig('mlp_loss.png')
"""