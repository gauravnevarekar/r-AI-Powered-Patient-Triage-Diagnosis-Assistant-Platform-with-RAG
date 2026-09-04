import os
import sys
import glob
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
import numpy as np
from PIL import Image, ImageDraw
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

MODEL_SAVE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models", "chest_xray_cnn.pth"))

class ChestXRayCNN(nn.Module):
    """
    Fast PyTorch CNN Architecture for Chest X-Ray Binary Classification (NORMAL vs PNEUMONIA)
    """
    def __init__(self):
        super(ChestXRayCNN, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, padding=1),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(2, 2), # 64x64
            
            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2, 2), # 32x32

            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((4, 4)) # 4x4
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64 * 4 * 4, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, 2) # Class 0: NORMAL, Class 1: PNEUMONIA
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x

def generate_synthetic_xray(label: int) -> np.ndarray:
    """Generates a 128x128 grayscale chest radiograph image matrix."""
    img = Image.new("L", (128, 128), color=25)
    draw = ImageDraw.Draw(img)

    # Mediastinum & Cardiac Shadow
    draw.ellipse([48, 24, 80, 104], fill=140)

    # Lung Fields (Radiolucent dark areas)
    draw.ellipse([16, 26, 54, 98], fill=45)
    draw.ellipse([74, 26, 112, 98], fill=45)

    # Rib contours
    for y in range(30, 95, 12):
        draw.arc([14, y, 56, y + 15], start=180, end=360, fill=110, width=2)
        draw.arc([72, y, 114, y + 15], start=180, end=360, fill=110, width=2)

    # If PNEUMONIA (label=1): Add pulmonary opacity consolidation
    if label == 1:
        draw.ellipse([78, 58, 106, 90], fill=215)
        draw.ellipse([82, 65, 100, 85], fill=240)

    arr = np.array(img, dtype=np.float32)
    noise = np.random.normal(0, 6, (128, 128)).astype(np.float32)
    arr = np.clip(arr + noise, 0, 255) / 255.0
    return arr

def build_dataset():
    images = []
    labels = []

    kaggle_paths = [
        "c:/Users/Gaurav Nevarekar/Downloads/chest_xray",
        "backend/data/chest_xray",
        "data/chest_xray"
    ]
    found_kaggle_dir = None
    for p in kaggle_paths:
        if os.path.exists(p):
            found_kaggle_dir = p
            break

    if found_kaggle_dir:
        print(f"Loading Kaggle Chest X-Ray dataset from: {found_kaggle_dir}")
        for class_idx, class_name in enumerate(["NORMAL", "PNEUMONIA"]):
            files = glob.glob(os.path.join(found_kaggle_dir, "**", class_name, "*.jpeg")) + \
                    glob.glob(os.path.join(found_kaggle_dir, "**", class_name, "*.jpg")) + \
                    glob.glob(os.path.join(found_kaggle_dir, "**", class_name, "*.png"))
            for fpath in files[:200]:
                try:
                    with Image.open(fpath) as img:
                        img = img.convert("L").resize((128, 128))
                        arr = np.array(img, dtype=np.float32) / 255.0
                        images.append(arr)
                        labels.append(class_idx)
                except Exception:
                    pass
    else:
        print("Kaggle dataset directory not found locally. Generating 400 Chest Radiograph samples (200 Normal vs 200 Pneumonia)...")
        np.random.seed(42)
        for i in range(200):
            images.append(generate_synthetic_xray(0)) # Normal
            labels.append(0)
        for i in range(200):
            images.append(generate_synthetic_xray(1)) # Pneumonia
            labels.append(1)

    X = np.array(images, dtype=np.float32)
    y = np.array(labels, dtype=np.int64)

    X = np.expand_dims(X, axis=1) # (N, 1, 128, 128)

    indices = np.arange(len(X))
    np.random.shuffle(indices)

    split = int(0.8 * len(X))
    train_idx, test_idx = indices[:split], indices[split:]

    return X[train_idx], y[train_idx], X[test_idx], y[test_idx]

def train_and_eval():
    print("=" * 60)
    print("HEALTHBRIDGE AI — CHEST X-RAY CNN MODEL TRAINING")
    print("=" * 60)

    X_train, y_train, X_test, y_test = build_dataset()
    print(f"Dataset Loaded: Train shape={X_train.shape}, Test shape={X_test.shape}")

    train_dataset = TensorDataset(torch.tensor(X_train), torch.tensor(y_train))
    test_dataset = TensorDataset(torch.tensor(X_test), torch.tensor(y_test))

    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

    model = ChestXRayCNN()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.002)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    epochs = 8
    print(f"\nStarting CNN training on {device} for {epochs} epochs...")

    for epoch in range(1, epochs + 1):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for batch_x, batch_y in train_loader:
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)
            optimizer.zero_grad()
            outputs = model(batch_x)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * batch_x.size(0)
            preds = torch.argmax(outputs, dim=1)
            correct += (preds == batch_y).sum().item()
            total += batch_y.size(0)

        epoch_loss = running_loss / total
        epoch_acc = correct / total
        print(f"Epoch [{epoch:02d}/{epochs:02d}] - Loss: {epoch_loss:.4f} | Train Acc: {epoch_acc * 100:.2f}%")

    print("\nEvaluating on Held-Out Test Set...")
    model.eval()
    all_preds = []
    all_targets = []

    with torch.no_grad():
        for batch_x, batch_y in test_loader:
            batch_x = batch_x.to(device)
            outputs = model(batch_x)
            preds = torch.argmax(outputs, dim=1).cpu().numpy()
            all_preds.extend(preds)
            all_targets.extend(batch_y.numpy())

    all_preds = np.array(all_preds)
    all_targets = np.array(all_targets)

    acc = accuracy_score(all_targets, all_preds)
    prec = precision_score(all_targets, all_preds, pos_label=1, zero_division=0)
    rec = recall_score(all_targets, all_preds, pos_label=1, zero_division=0)
    f1 = f1_score(all_targets, all_preds, pos_label=1, zero_division=0)
    cm = confusion_matrix(all_targets, all_preds)

    print("\n" + "=" * 60)
    print("HELD-OUT TEST SET EVALUATION METRICS:")
    print("=" * 60)
    print(f"  - Accuracy:  {acc * 100:.2f}% ({np.sum(all_preds == all_targets)}/{len(all_targets)})")
    print(f"  - Precision: {prec * 100:.2f}% (Pneumonia Class)")
    print(f"  - Recall:    {rec * 100:.2f}% (Pneumonia Class)")
    print(f"  - F1 Score:  {f1 * 100:.2f}%")
    print(f"  - Confusion Matrix:\n{cm}")
    print("=" * 60)

    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
    torch.save({
        'model_state_dict': model.state_dict(),
        'acc': float(acc),
        'precision': float(prec),
        'recall': float(rec),
        'f1': float(f1)
    }, MODEL_SAVE_PATH)
    print(f"\nTrained CNN model checkpoint saved successfully to: {MODEL_SAVE_PATH}")
    return acc, prec, rec, f1

if __name__ == "__main__":
    train_and_eval()
