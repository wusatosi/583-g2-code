import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split

# Custom Dataset class
class CSVDataset(Dataset):
    def __init__(self, features, labels):
        self.features = features
        self.labels = labels

    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        return self.features[idx], self.labels[idx]

# Function to load the dataset
def load_dataset(file_path):
    df = pd.read_csv(file_path, header=None)
    indices = [1, 2] + list(range(4, 22))
    X = df.iloc[indices, :].values
    y = df.iloc[22, :].values
    X = torch.tensor(X, dtype=torch.float32)
    X = X.transpose(0, 1)
    y = torch.tensor(y, dtype=torch.float32).unsqueeze(1)
    return X, y

# Define the MLP model
class TwoLayerMLP(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(TwoLayerMLP, self).__init__()
        self.layer1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.layer2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = self.relu(self.layer1(x))
        x = self.layer2(x)
        return x

# Load your dataset
file_path = './combined_column.csv'  # Replace with your CSV file path
X, y = load_dataset(file_path)

# Split the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

# Create Dataset objects
train_dataset = CSVDataset(X_train, y_train)
test_dataset = CSVDataset(X_test, y_test)

# Create DataLoaders
train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=16,shuffle=False)

# Model, Loss function and Optimizer
input_size = 20
hidden_size = 64
output_size = 1
model = TwoLayerMLP(input_size, hidden_size, output_size)
criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=0.0001)

# Function to evaluate the model
def evaluate_model(model, test_loader, criterion):
    model.eval()  # Set the model to evaluation mode
    total_loss = 0
    with torch.no_grad():  # No need to track the gradients
        for inputs, labels in test_loader:
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            total_loss += loss.item()
    return total_loss / len(test_loader)

# Training Loop
num_epochs = 2000
inputs_sum = torch.zeros((20))
total = 0
for epoch in range(num_epochs):
    model.train()
    for inputs, labels in train_loader:
        # Forward pass
        inputs_sum += inputs.sum(0)
        total += inputs.shape[0]
        outputs = model(inputs)
        loss = criterion(outputs, labels)

        # Backward pass and optimization
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    # Evaluate the model
    test_loss = evaluate_model(model, test_loader, criterion)
    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}, Test Loss: {test_loss:.4f}')

# Save the model after the final epoch
# torch.save(model.state_dict(), 'model_final.pth')
print("Model saved as 'model_final.pth'")

# Assuming the model is already defined and loaded
# model = ...

# Ensure the model is in evaluation mode to not affect its parameters
model.eval()

# Initial input - this could be random or some starting point
input_tensor = (inputs_sum / total).unsqueeze(0)
input_tensor.requires_grad = True
input_tensor = torch.autograd.Variable(input_tensor, requires_grad=True)

# Learning rate for input update
learning_rate = 5

# Number of steps for gradient descent on inputs
steps = 100

for step in range(steps):

    # Forward pass
    # Manually update the inputs using the gradients
    f = torch.autograd.grad(model(input_tensor).sum(), [input_tensor], retain_graph=True)[0]
    print(f)
    input_tensor = input_tensor - learning_rate * f + torch.randn_like(input_tensor) * 0.01
    input_tensor = torch.clamp(input_tensor, min=1)
    # if step % 10 == 0:
        # print(out)
    # Print the loss

print(input_tensor)
input_tensor = input_tensor.squeeze(0)
df = pd.read_csv('ml_results.csv', header=None)
df.iloc[1:3,1] = input_tensor[0:2].detach().numpy()
df.iloc[4:, 1] = input_tensor[2:].detach().numpy()
df.to_csv('ml_loss.csv', index=False, header=False)

# The 'input_tensor' now holds the optimized input
