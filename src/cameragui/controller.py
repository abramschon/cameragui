

class Controller:
    """
    Responsible for handling user input and updating the model.
    """
    def __init__(self, model, view):
        self.model = model
        self.view = view