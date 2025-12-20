import re
from typing import List, Dict

class LogPreprocessor:
    """Preprocesses user behavior logs for transformer model"""
    
    def __init__(self):
        # Common behavior patterns
        self.behavior_keywords = {
            'login', 'logout', 'admin', 'user', 'access', 'denied',
            'export', 'delete', 'modify', 'create', 'read', 'write',
            'database', 'file', 'system', 'config', 'password', 'sudo',
            'root', 'privilege', 'escalation', 'brute', 'force', 'attempt',
            'failed', 'success', 'unauthorized', 'forbidden', 'error'
        }
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep spaces
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def extract_sequence(self, log_entry: str) -> str:
        """Extract behavior sequence from log entry"""
        cleaned = self.clean_text(log_entry)
        
        # Extract keywords
        words = cleaned.split()
        sequence_words = [w for w in words if w in self.behavior_keywords or len(w) > 3]
        
        # Create sequence
        sequence = ' '.join(sequence_words[:20])  # Limit to 20 words
        
        return sequence if sequence else cleaned[:100]
    
    def process_log_file(self, content: str) -> List[Dict]:
        """Process entire log file content"""
        lines = content.strip().split('\n')
        processed_logs = []
        
        for line in lines:
            if line.strip():
                sequence = self.extract_sequence(line)
                if sequence:
                    processed_logs.append({
                        'original': line.strip(),
                        'sequence': sequence
                    })
        
        return processed_logs
    
    def process_csv(self, csv_content: str) -> List[Dict]:
        """Process CSV log file"""
        import csv
        from io import StringIO
        
        processed_logs = []
        csv_reader = csv.DictReader(StringIO(csv_content))
        
        for row in csv_reader:
            # Try to find event/action column
            event = None
            for key in ['event', 'action', 'activity', 'log', 'message']:
                if key in row:
                    event = row[key]
                    break
            
            if not event:
                # Concatenate all values
                event = ' '.join(str(v) for v in row.values())
            
            sequence = self.extract_sequence(event)
            if sequence:
                processed_logs.append({
                    'original': event,
                    'sequence': sequence,
                    'metadata': row
                })
        
        return processed_logs
    
    def create_training_examples(self) -> List[Dict]:
        """Create synthetic training examples for the model"""
        examples = [
            # Normal behaviors
            {'sequence': 'login user dashboard view logout', 'label': 0},
            {'sequence': 'user access file read document', 'label': 0},
            {'sequence': 'login check email send message logout', 'label': 0},
            {'sequence': 'user view report download file', 'label': 0},
            {'sequence': 'login user profile update settings', 'label': 0},
            
            # Suspicious behaviors
            {'sequence': 'login failed attempt retry password', 'label': 1},
            {'sequence': 'access denied unauthorized attempt', 'label': 1},
            {'sequence': 'multiple login failed brute force', 'label': 1},
            {'sequence': 'user access admin panel denied', 'label': 1},
            {'sequence': 'password reset multiple attempts', 'label': 1},
            
            # Malicious behaviors
            {'sequence': 'login admin export database delete', 'label': 2},
            {'sequence': 'sudo root privilege escalation system', 'label': 2},
            {'sequence': 'admin delete user database export', 'label': 2},
            {'sequence': 'unauthorized access system config modify', 'label': 2},
            {'sequence': 'brute force login admin delete database', 'label': 2},
            {'sequence': 'root access system file delete modify', 'label': 2},
            {'sequence': 'admin privilege escalation export database', 'label': 2},
        ]
        
        return examples

# Initialize preprocessor
preprocessor = LogPreprocessor()
