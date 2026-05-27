from collections import defaultdict

class MemoryStore:
    def __init__(self):
        self.user_memory = defaultdict(list)

    def add(self, user_id: str, query: str):
        self.user_memory[user_id].append(query)

    def get_context(self, user_id: str):
        return " ".join(self.user_memory[user_id][-10:])

memory_store = MemoryStore()        