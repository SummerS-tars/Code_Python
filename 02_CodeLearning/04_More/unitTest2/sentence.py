class Sentence:
    def __init__(self, type, text):
        self.type = type
        self.text = text
    
    def __str__(self):
        return f"{self.type}: {self.text}"
    
    def __repr__(self):
        return f"Sentence(type={self.type}, text={self.text})"
    
    def __eq__(self, other):
        return self.type == other.type and self.text == other.text
