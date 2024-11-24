import torch
from PIL import Image
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np

# Load the image
image_path = 'IMG_20240311_21253945.jpg'  # Replace 'shre-image.jpeg' with the path to your image
image = Image.open(image_path)

# Define the transformation pipeline
transform = transforms.Compose([
    transforms.Resize((224, 224)),  # Resize the image to 224x224 pixels
    transforms.ToTensor(),  # Convert the image to a PyTorch tensor
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Normalize the image
])

# Apply the transformation pipeline to the image
normalized_image = transform(image)

# Convert the PyTorch tensor to a NumPy array for plotting
numpy_image = normalized_image.numpy()

# Calculate the histogram for each channel
histograms = [np.histogram(channel, bins=50, range=(0.0, 1.0))[0] for channel in numpy_image]

# Display the normalized image with histograms
fig, axs = plt.subplots(2, 2, figsize=(10, 10))

# Plot the normalized image
axs[0, 0].imshow(transforms.ToPILImage()(normalized_image))
axs[0, 0].set_title('Normalized Image')
axs[0, 0].axis('off')

# Plot the histograms for each channel
colors = ['red', 'green', 'blue']
for i, (hist, color) in enumerate(zip(histograms, colors)):
    axs[0, 1].plot(np.linspace(0, 1, 50), hist, color=color, label=f'Channel {i+1}')
axs[0, 1].set_title('Histograms')
axs[0, 1].set_xlabel('Pixel Intensity')
axs[0, 1].set_ylabel('Frequency')
axs[0, 1].legend()

# Hide the empty subplot
axs[1, 0].axis('off')
axs[1, 1].axis('off')

plt.tight_layout()
plt.show()
