"""
Training script for the Transformer-based threat detection model.

This script demonstrates how to fine-tune the model on labeled data.
For production use, you would need a larger labeled dataset.
"""

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AdamW, get_linear_schedule_with_warmup
from transformer_model import ThreatDetectionModel
from preprocessor import preprocessor
from config import Config
import numpy as np
from sklearn.model_selection import train_test_split

class ThreatDataset(Dataset):
    """Dataset for threat detection"""
    
    def __init__(self, sequences, labels, tokenizer, max_length):
        self.sequences = sequences
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.sequences)
    
    def __getitem__(self, idx):
        sequence = self.sequences[idx]
        label = self.labels[idx]
        
        encoding = self.tokenizer(
            sequence,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'label': torch.tensor(label, dtype=torch.long)
        }


def train_model(epochs=10, batch_size=8, learning_rate=2e-5):
    """Train the threat detection model"""
    
    # Set device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    # Load training data
    print("Loading training data...")
    examples = preprocessor.create_training_examples()
    
    # Expand dataset with variations (data augmentation)
    expanded_examples = []
    for ex in examples:
        expanded_examples.append(ex)
        # Add variations
        words = ex['sequence'].split()
        if len(words) > 2:
            # Shuffle some words
            import random
            shuffled = words.copy()
            random.shuffle(shuffled)
            expanded_examples.append({
                'sequence': ' '.join(shuffled),
                'label': ex['label']
            })
    
    sequences = [ex['sequence'] for ex in expanded_examples]
    labels = [ex['label'] for ex in expanded_examples]
    
    # Split data
    train_seq, val_seq, train_labels, val_labels = train_test_split(
        sequences, labels, test_size=0.2, random_state=42, stratify=labels
    )
    
    print(f"Training samples: {len(train_seq)}, Validation samples: {len(val_seq)}")
    
    # Create tokenizer
    tokenizer = AutoTokenizer.from_pretrained(Config.MODEL_NAME)
    
    # Create datasets
    train_dataset = ThreatDataset(train_seq, train_labels, tokenizer, Config.MAX_SEQ_LENGTH)
    val_dataset = ThreatDataset(val_seq, val_labels, tokenizer, Config.MAX_SEQ_LENGTH)
    
    # Create dataloaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size)
    
    # Initialize model
    model = ThreatDetectionModel(Config.MODEL_NAME, num_classes=3)
    model.to(device)
    
    # Optimizer and scheduler
    optimizer = AdamW(model.parameters(), lr=learning_rate)
    total_steps = len(train_loader) * epochs
    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=0,
        num_training_steps=total_steps
    )
    
    # Loss function
    criterion = nn.CrossEntropyLoss()
    
    # Training loop
    print("\nStarting training...")
    best_val_acc = 0
    
    for epoch in range(epochs):
        # Training
        model.train()
        train_loss = 0
        train_correct = 0
        train_total = 0
        
        for batch in train_loader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['label'].to(device)
            
            optimizer.zero_grad()
            
            logits = model(input_ids, attention_mask)
            loss = criterion(logits, labels)
            
            loss.backward()
            optimizer.step()
            scheduler.step()
            
            train_loss += loss.item()
            _, predicted = torch.max(logits, 1)
            train_total += labels.size(0)
            train_correct += (predicted == labels).sum().item()
        
        train_acc = train_correct / train_total
        avg_train_loss = train_loss / len(train_loader)
        
        # Validation
        model.eval()
        val_loss = 0
        val_correct = 0
        val_total = 0
        
        with torch.no_grad():
            for batch in val_loader:
                input_ids = batch['input_ids'].to(device)
                attention_mask = batch['attention_mask'].to(device)
                labels = batch['label'].to(device)
                
                logits = model(input_ids, attention_mask)
                loss = criterion(logits, labels)
                
                val_loss += loss.item()
                _, predicted = torch.max(logits, 1)
                val_total += labels.size(0)
                val_correct += (predicted == labels).sum().item()
        
        val_acc = val_correct / val_total
        avg_val_loss = val_loss / len(val_loader)
        
        print(f"Epoch {epoch+1}/{epochs}")
        print(f"  Train Loss: {avg_train_loss:.4f}, Train Acc: {train_acc:.4f}")
        print(f"  Val Loss: {avg_val_loss:.4f}, Val Acc: {val_acc:.4f}")
        
        # Save best model
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), 'threat_detection_model.pth')
            print(f"  ✓ Saved best model (val_acc: {val_acc:.4f})")
    
    print(f"\nTraining completed! Best validation accuracy: {best_val_acc:.4f}")
    print("Model saved as 'threat_detection_model.pth'")


if __name__ == '__main__':
    train_model(epochs=10, batch_size=8, learning_rate=2e-5)
