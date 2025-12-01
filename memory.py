class ProjectMemory:
    def __init__(self):
        self.data = {
            "summary": None,
            "components": [],
        }

    def save_summary(self, text):
        self.data["summary"] = text

    def save_components(self, components):
        self.data["components"] = components

    def dump(self):
        return self.data
