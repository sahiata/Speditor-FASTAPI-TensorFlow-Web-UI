import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.regularizers import l2
from tensorflow.keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt


# Input data (X) - 30 routes
X = np.array([
  [3420, 10, 15.00, 1539.00, 171.00, 200.00, 450.00, 100.00, 20.00, 50.00],
  [3220, 9, 13.50, 1449.00, 161.00, 200.00, 450.00, 100.00, 20.00, 50.00],
  [3380, 9, 13.50, 1512.00, 169.00, 200.00, 450.00, 100.00, 20.00, 50.00],
  [3300, 10, 15.00, 1485.00, 165.00, 200.00, 450.00, 100.00, 20.00, 50.00],
  [3000, 8, 12.00, 1350.00, 150.00, 200.00, 450.00, 80.00, 10.00, 40.00],
  [3100, 8, 12.00, 1395.00, 155.00, 200.00, 450.00, 85.00, 10.00, 45.00],
  [3050, 9, 13.00, 1372.50, 152.50, 200.00, 450.00, 82.00, 10.00, 42.00],
  [3200, 9, 13.00, 1440.00, 160.00, 200.00, 450.00, 90.00, 20.00, 50.00],
  [3500, 11, 16.00, 1575.00, 175.00, 200.00, 450.00, 110.00, 25.00, 60.00],
  [3400, 10, 15.00, 1530.00, 170.00, 200.00, 450.00, 105.00, 20.00, 55.00],
  [3600, 12, 17.00, 1620.00, 180.00, 200.00, 450.00, 115.00, 25.00, 65.00],
  [3250, 9, 13.00, 1462.50, 162.50, 200.00, 450.00, 92.00, 20.00, 50.00],
  [3150, 8, 12.00, 1417.50, 157.50, 200.00, 450.00, 87.00, 10.00, 45.00],
  [2800, 7, 10.50, 1260.00, 140.00, 200.00, 450.00, 70.00, 10.00, 35.00],
  [2750, 6, 9.00, 1237.50, 137.50, 200.00, 450.00, 68.00, 10.00, 30.00],
  [2850, 7, 10.50, 1282.50, 142.50, 200.00, 450.00, 72.00, 10.00, 36.00],
  [2950, 8, 12.00, 1327.50, 147.50, 200.00, 450.00, 76.00, 10.00, 38.00],
  [2700, 6, 9.00, 1215.00, 135.00, 200.00, 450.00, 66.00, 10.00, 30.00],
  [2650, 6, 9.00, 1192.50, 132.50, 200.00, 450.00, 64.00, 10.00, 28.00],
  [2900, 7, 10.50, 1305.00, 145.00, 200.00, 450.00, 74.00, 10.00, 37.00],
  [3350, 10, 15.00, 1507.50, 167.50, 200.00, 450.00, 98.00, 20.00, 52.00],
  [3450, 10, 15.00, 1552.50, 172.50, 200.00, 450.00, 102.00, 20.00, 54.00],
  [3550, 11, 16.50, 1597.50, 177.50, 200.00, 450.00, 108.00, 25.00, 58.00],
  [3700, 12, 18.00, 1665.00, 185.00, 200.00, 450.00, 120.00, 30.00, 66.00],
  [3750, 12, 18.00, 1687.50, 187.50, 200.00, 450.00, 122.00, 30.00, 67.00],
  [3800, 13, 19.50, 1710.00, 190.00, 200.00, 450.00, 125.00, 30.00, 68.00],
  [2900, 8, 12.00, 1305.00, 145.00, 200.00, 450.00, 74.00, 10.00, 37.00],
  [3000, 9, 13.50, 1350.00, 150.00, 200.00, 450.00, 80.00, 10.00, 40.00],
  [3100, 9, 13.50, 1395.00, 155.00, 200.00, 450.00, 85.00, 10.00, 45.00],
  [3200, 10, 15.00, 1440.00, 160.00, 200.00, 450.00, 90.00, 20.00, 50.00]
])


#  Output data (y) - total cost and time
y = np.array([
  [2530.00, 55.00], [2430.00, 52.50], [2510.00, 53.00], [2500.00, 54.00],
  [2320.00, 49.00], [2390.00, 50.00], [2355.00, 50.50], [2450.00, 51.50],
  [2660.00, 58.00], [2580.00, 56.00], [2700.00, 59.50], [2460.00, 52.00],
  [2410.00, 50.00], [2200.00, 45.00], [2150.00, 43.00], [2250.00, 46.00],
  [2300.00, 47.50], [2100.00, 42.00], [2050.00, 41.00], [2280.00, 47.00],
  [2520.00, 54.00], [2550.00, 55.00], [2600.00, 56.50], [2750.00, 60.00],
  [2780.00, 60.50], [2800.00, 61.00], [2280.00, 47.00], [2320.00, 49.00],
  [2390.00, 50.00], [2450.00, 51.50]
])


# Splitting data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)
# First, create index numbers
all_indexes = list(range(len(X)))

# Split and store test indices
train_indexes, test_indexes = train_test_split(all_indexes, test_size=0.1)

X_train = [X[i] for i in train_indexes]
X_test = [X[i] for i in test_indexes]
y_train = [y[i] for i in train_indexes]
y_test = [y[i] for i in test_indexes]

# Scaling input values
scaler_X = StandardScaler()
X_train_scaled = scaler_X.fit_transform(X_train)
X_test_scaled = scaler_X.transform(X_test)


# Scaling output values (targets)
scaler_y = StandardScaler()
y_train_scaled = scaler_y.fit_transform(y_train)
y_test_scaled = scaler_y.transform(y_test)
# Random selection of a route for testing
test_index = np.random.randint(len(X))
x_test = X[test_index].reshape(1, -1)
y_test_actual = y[test_index]


# Defining the model
model = Sequential([
  Dense(256, input_dim=10, activation='relu', kernel_regularizer=l2(0.01)),  # L2 regularization with a lambda factor of 0.01
  Dropout(0.3),  # Dropout with 20% probability to "drop" neurons
  Dense(128, activation='relu', kernel_regularizer=l2(0.01)),
  Dropout(0.3),
  Dense(2, activation='linear')  # For regression, use 'linear' activation
])  #2 output parameters (cost and time))


# Compiling the model
model.compile(optimizer='adam', loss=tf.keras.losses.MeanSquaredError())


# Define model with EarlyStopping callback
early_stopping = EarlyStopping(monitor='val_loss', patience=50, restore_best_weights=True)
# Train the model with EarlyStopping


history = model.fit(X_train_scaled, y_train_scaled, validation_data=(X_test_scaled, y_test_scaled),
          epochs=100, batch_size=64, callbacks=[early_stopping])


# Evaluating the model
mse_train = model.evaluate(X_train_scaled, y_train_scaled)
mse_test = model.evaluate(X_test_scaled, y_test_scaled)


print(f"Trening MSE: {mse_train}")
print(f"Test MSE: {mse_test}")
# Prediction on scaled test data
y_pred_scaled = model.predict(X_test_scaled)


# Inverse scaling to get real values (EUR, hours
y_pred = scaler_y.inverse_transform(y_pred_scaled)
y_true = scaler_y.inverse_transform(y_test_scaled)

# Nakon treniranja modela:
model.save("model.h5")
print("Model je uspešno sačuvan kao model.h5 ✅")

# Visualization of loss over epochs
plt.figure(figsize=(10, 5))
plt.plot(history.history['loss'], label='Trening loss')
plt.plot(history.history['val_loss'], label='Val loss')
plt.title('Trening loss')
plt.xlabel('Epochs')
plt.ylabel('MSE')
plt.legend()
plt.grid(True)
plt.show()


# Display of actual and predicted values
for i in range(len(y_true)):
  ruta_broj = test_indexes[i] + 1  # Adding +1 so it starts from 1
  print(f"\nChosen route number: {ruta_broj}")
  print(f"Actual value: Total cost = {y_true[i][0]:.2f} EUR, Total Travel Time = {y_true[i][1]:.2f} h")
  print(f"Prediction   : Total cost = {y_pred[i][0]:.2f} EUR, Total Travel Time = {y_pred[i][1]:.2f} h")
  print("-" * 50)
# Converting to NumPy arrays if not already
y_true = np.array(y_true)
y_pred = np.array(y_pred)

# Creating X-axis (route indices)
x = np.arange(len(y_true)) + 1  # Adding +1 so it starts from 1

# Displaying costs
plt.figure(figsize=(10, 5))
plt.plot(x, y_true[:, 0], label='Actual value cost', color='blue', linestyle='-')     
plt.plot(x, y_pred[:, 0], label='Prediction value cost', color='red', linestyle='--')  
plt.title('Actual vs Prediction value cost')
plt.xlabel('Test case serial number')
plt.ylabel('Cost (EUR)')
plt.legend()
plt.tight_layout()
plt.show()
# Displaying times
plt.figure(figsize=(10, 5))
plt.plot(x, y_true[:, 1], label='Actual Travel Time', color='green', linestyle='-')     
plt.plot(x, y_pred[:, 1], label='Predicted Travel time', color='orange', linestyle='--')  
plt.title('Actual vs Predicticted Travel Time')
plt.xlabel('Test case serial number')
plt.ylabel('Time (h)')
plt.legend()
plt.tight_layout()
plt.show()
