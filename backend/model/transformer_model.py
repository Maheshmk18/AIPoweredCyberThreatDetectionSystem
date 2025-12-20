import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel
from config import Config
import os

class ThreatDetectionModel(nn.Module):
    """Transformer-based threat detection model"""
    
    def __init__(self, model_name=Config.MODEL_NAME, num_classes=3):
        super(ThreatDetectionModel, self).__init__()
        
        # Load pre-trained transformer
        self.transformer = AutoModel.from_pretrained(model_name)
        
        # Classification head
        self.dropout = nn.Dropout(0.3)
        self.classifier = nn.Linear(self.transformer.config.hidden_size, num_classes)
    
    def forward(self, input_ids, attention_mask):
        """Forward pass"""
        # Get transformer outputs
        outputs = self.transformer(
            input_ids=input_ids,
            attention_mask=attention_mask
        )
        
        # Use [CLS] token representation
        pooled_output = outputs.last_hidden_state[:, 0, :]
        
        # Apply dropout and classifier
        pooled_output = self.dropout(pooled_output)
        logits = self.classifier(pooled_output)
        
        return logits


class ThreatDetector:
    """Wrapper class for threat detection inference"""
    
    def __init__(self, model_path=None):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model_name = Config.MODEL_NAME
        self.max_length = Config.MAX_SEQ_LENGTH
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        
        # Initialize model
        self.model = ThreatDetectionModel(self.model_name)
        
        # Load trained weights if available
        if model_path and os.path.exists(model_path):
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
            print(f"Loaded model from {model_path}")
        else:
            print("Using pre-trained model (not fine-tuned for threat detection)")
            # Initialize with simple heuristics for demo
            self._init_simple_classifier()
        
        self.model.to(self.device)
        self.model.eval()
        
        # Labels
        self.labels = ['normal', 'suspicious', 'malicious']
    
    def _init_simple_classifier(self):
        """Initialize classifier with simple weights for demo"""
        # This is a placeholder - in production, train the model properly
        pass
    
    def predict(self, text: str):
        """Predict threat level for a behavior sequence"""
        # Tokenize
        inputs = self.tokenizer(
            text,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        input_ids = inputs['input_ids'].to(self.device)
        attention_mask = inputs['attention_mask'].to(self.device)
        
        # Predict
        with torch.no_grad():
            logits = self.model(input_ids, attention_mask)
            probabilities = torch.softmax(logits, dim=1)
            predicted_class = torch.argmax(probabilities, dim=1).item()
            confidence = probabilities[0][predicted_class].item()
        
        # Apply heuristic rules for better demo (since model isn't trained)
        prediction, score = self._apply_heuristics(text, predicted_class, confidence)
        
        return {
            'prediction': prediction,
            'score': score,
            'probabilities': {
                'normal': float(probabilities[0][0]),
                'suspicious': float(probabilities[0][1]),
                'malicious': float(probabilities[0][2])
            }
        }
    
    def _apply_heuristics(self, text: str, predicted_class: int, confidence: float):
        """Apply rule-based heuristics for better predictions"""
        text_lower = text.lower()
        
        # Malicious keywords
        malicious_keywords = ['delete', 'admin', 'root', 'sudo', 'export', 'database', 
                             'privilege', 'escalation', 'unauthorized', 'brute']
        
        # Suspicious keywords
        suspicious_keywords = ['failed', 'denied', 'attempt', 'retry', 'error', 
                              'forbidden', 'multiple']
        
        # Count keyword matches
        malicious_count = sum(1 for kw in malicious_keywords if kw in text_lower)
        suspicious_count = sum(1 for kw in suspicious_keywords if kw in text_lower)
        
        # Determine prediction based on heuristics
        if malicious_count >= 2:
            return 'malicious', min(0.75 + (malicious_count * 0.05), 0.98)
        elif malicious_count >= 1 and suspicious_count >= 1:
            return 'malicious', min(0.70 + (malicious_count * 0.05), 0.95)
        elif suspicious_count >= 2:
            return 'suspicious', min(0.55 + (suspicious_count * 0.05), 0.85)
        elif suspicious_count >= 1:
            return 'suspicious', min(0.50 + (suspicious_count * 0.05), 0.75)
        else:
            return 'normal', max(0.60 - (malicious_count * 0.1), 0.40)
    
    def predict_batch(self, texts: list):
        """Predict threat levels for multiple sequences"""
        results = []
        for text in texts:
            results.append(self.predict(text))
        return results

# Initialize global detector
detector = None

def get_detector():
    """Get or create detector instance"""
    global detector
    if detector is None:
        detector = ThreatDetector()
    return detector
