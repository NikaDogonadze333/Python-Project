class Task:
    def __init__(self, title, description, deadline, priority, project="General", status="pending"):
        self.title = title
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.project = project
        self.status = status

    def update_status(self, new_status):
        valid_statuses = ["pending", "in-progress", "completed"]
        if new_status not in valid_statuses:
            raise ValueError("არასწორი სტატუსი")
        self.status = new_status

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "deadline": self.deadline,
            "priority": self.priority,
            "project": self.project,
            "status": self.status
        }