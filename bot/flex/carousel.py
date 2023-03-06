
class Carousel:
    def __init__(self) -> None:
        self._contents = []
    
    def add_bubble(self, bubble):
        self._contents.append(bubble.to_flex())

    def to_flex(self):
        return {
            "type": "carousel", "contents": self._contents
        }