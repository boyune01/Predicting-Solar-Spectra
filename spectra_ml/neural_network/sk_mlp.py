import matplotlib.pyplot as plt
import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import learning_curve
from sklearn.model_selection import validation_curve
from sklearn.model_selection import train_test_split

# Load weather and radience data into arrays
X = np.loadtxt('data/input_cleaned/wea_input.csv', skiprows=1, delimiter=',', usecols=range(1, 14))
y = np.loadtxt('data/input_cleaned/rad_input.csv', skiprows=1, delimiter=',', usecols=range(1, 14))

for i in [X, y]:
    print(type(i), i.shape)

# Perform 80-20 train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=1)

# Initialize neural network with two 64-node hidden layers
reg = MLPRegressor(hidden_layer_sizes=(64, 64), activation='relu', random_state=1, max_iter=1000).fit(X_train, y_train)
pred = reg.predict(X_test)
print("Prediction shape:", pred.shape)
acc = reg.score(X_test, y_test)
print(acc)

fig, ax = plt.subplots()
plt.show()

"""
alphas = np.logspace(-5, 1, 60)
train_errors = list()
test_errors = list()
for alpha in alphas:
    reg.set_params(alpha=alpha)
    reg.fit(X_train, y_train)
    train_errors.append(reg.score(X_train, y_train))
    test_errors.append(reg.score(X_test, y_test))

i_alpha_optim = np.argmax(test_errors)
alpha_optim = alphas[i_alpha_optim]
print("Optimal regularization parameter : %s" % alpha_optim)

reg.set_params(alpha=alpha_optim)
coef_ = reg.fit(X, y).coef_


plt.subplot(2, 1, 1)
plt.semilogx(alphas, train_errors, label="Train")
plt.semilogx(alphas, test_errors, label="Test")
plt.vlines(
    alpha_optim,
    plt.ylim()[0],
    np.max(test_errors),
    color="k",
    linewidth=3,
    label="Optimum on test",
)
plt.legend(loc="lower right")
plt.ylim([0, 1.2])
plt.xlabel("Regularization parameter")
plt.ylabel("Performance")

# Show estimated coef_ vs true coef
plt.subplot(2, 1, 2)
plt.plot(reg, label="True coef")
plt.plot(coef_, label="Estimated coef")
plt.legend()
plt.subplots_adjust(0.09, 0.04, 0.94, 0.94, 0.26, 0.26)
plt.show()
"""