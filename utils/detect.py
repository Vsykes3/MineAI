import torch
from torchvision import transforms
from PIL import Image
import torch.nn.functional as F

# Load model once at the top
model = torch.load("model.pth", map_location=torch.device('cpu'))
model.eval()

# Define your classes — must match training
# Example: index 0 = "zombie", 1 = "creeper", 2 = "skeleton", 3 = "none"
class_names = ["Bee", "Carrot", "Cave Spider", "Chest", "Chicken", "Cow", "Creeper", "Dolphin", "Enderman", "Flower", "Goat", "House", "Iron Golem", "Llama", "Panda", "Pig", "Player", "Polar Bear", "Potato", "Rabbit", "Sheep", "Spider", "Trader Llama", "Villager", "Villager House", "Wheat", "Wolf", "Zombified Piglin"]  # Replace with your actual classes

# Preprocessing must match what was used during training
transform = transforms.Compose([
    transforms.Resize((224, 224)),   # Or the size your model expects
    transforms.ToTensor(),
    transforms.Normalize([0.5]*3, [0.5]*3)  # Update if your training had different normalization
])

def detect_mob(image):
    """
    Takes a PIL image, returns the predicted mob name or None.
    """
    img_tensor = transform(image).unsqueeze(0)  # Add batch dimension
    with torch.no_grad():
        outputs = model(img_tensor)
        probs = F.softmax(outputs, dim=1)
        top_prob, top_class = probs.topk(1)
        label = class_names[top_class.item()]
        return None if label == "none" else label

