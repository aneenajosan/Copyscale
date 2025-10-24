import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import numpy as np

class ImageFingerprinter:
    def __init__(self):
        # Use modern weights syntax instead of deprecated 'pretrained=True'
        self.model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
        self.model.eval()
        
        # Use the transforms that match the weights
        self.transform = models.ResNet50_Weights.DEFAULT.transforms()
    
    def get_fingerprint(self, image_path):
        """Extract a feature vector (fingerprint) from an image"""
        try:
            image = Image.open(image_path).convert('RGB')
            image = self.transform(image).unsqueeze(0)  # Add batch dimension
            
            with torch.no_grad():
                features = self.model(image)
            
            return features.numpy().flatten()
        except Exception as e:
            print(f"Error processing image: {e}")
            return None

if __name__ == "__main__":
    fingerprinter = ImageFingerprinter()
    print("Fingerprinter initialized successfully with modern weights!")
