

import tkinter as tk
from tkinter import filedialog, messagebox
import torch
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image, ImageTk
import os


class SimpleFoodDetector:
    def __init__(self, root):
        self.root = root
        self.root.title("Food Detection App")
        self.root.geometry("800x600")

        # Create labels file if not exists
        self.ensure_labels_file()

        # Load pre-trained model
        self.load_model()

        # Create UI
        self.create_ui()

    def ensure_labels_file(self):
        """Create labels file if it doesn't exist"""
        labels_path = 'imagenet_classes.txt'
        if not os.path.exists(labels_path):
            default_classes = [
                'pizza', 'burger', 'sandwich', 'apple', 'banana',
                'salad', 'cake', 'ice cream', 'soup', 'pasta'
                ]
            with open(labels_path, 'w') as f:
                for cls in default_classes:
                    f.write(f"{cls}\n")

    def load_model(self):
        """Load pre-trained ResNet model"""
        try:
            # Load pre-trained ResNet model
            self.model = models.resnet18(pretrained=True)
            self.model.eval()

            # Load class labels
            labels_path = 'imagenet_classes.txt'
            with open(labels_path, 'r') as f:
                self.classes = [line.strip() for line in f.readlines()]

        except Exception as e:
            messagebox.showerror("Model Loading Error", str(e))
            self.model = None

    def create_ui(self):
        """Create application user interface"""
        # Frame for better layout
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Image Upload Button
        upload_button = tk.Button(
            main_frame,
            text="Upload Food Image",
            command=self.upload_image,
            font=('Arial', 12)
            )
        upload_button.pack(pady=10)

        # Image Display Area
        self.image_label = tk.Label(main_frame)
        self.image_label.pack(pady=10)

        # Detection Results Display
        self.results_text = tk.Text(
            main_frame,
            height=10,
            width=50,
            wrap=tk.WORD,
            font=('Arial', 10)
            )
        self.results_text.pack(pady=10)

    def upload_image(self):
        """Handle image upload and food detection"""
        file_path = filedialog.askopenfilename(
            title="Select Food Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"),
                ("All files", "*.*")
                ]
            )

        if not file_path:
            return

        try:
            # Load and display original image
            original_image = Image.open(file_path)
            original_image.thumbnail((400, 400))
            photo = ImageTk.PhotoImage(original_image)
            self.image_label.config(image=photo)
            self.image_label.image = photo

            # Detect food
            results = self.detect_food(file_path)

            # Display results
            self.display_results(results)

        except Exception as e:
            messagebox.showerror("Image Processing Error", str(e))

    def detect_food(self, image_path):
        """Detect food in the image"""
        if not self.model:
            raise ValueError("Model not loaded")

        # Image preprocessing
        transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
                )
            ])

        # Load image
        image = Image.open(image_path)
        input_tensor = transform(image).unsqueeze(0)

        # Inference
        with torch.no_grad():
            outputs = self.model(input_tensor)

        # Get top 5 predictions
        _, indices = torch.topk(outputs, 5)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)[0]

        # Process results
        results = []
        for idx in indices[0]:
            probability = probabilities[idx].item()
            class_name = self.classes[idx]
            results.append((class_name, probability * 100))

        return results

    def display_results(self, results):
        """Display detection results"""
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Top Object Predictions:\n\n")

        for name, confidence in results:
            result_text = f"{name.capitalize()}: {confidence:.2f}%\n"
            self.results_text.insert(tk.END, result_text)


def main():
    root = tk.Tk()
    app = SimpleFoodDetector(root)
    root.mainloop()


if __name__ == "__main__":
    main()