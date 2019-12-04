class Movie:

    def __init__(self, title):
        self.title = title
        self.original_title = None
        self.duration = None
        self.rating = None
        self.release_date = None
        self.id = None
        self.actors = []
        self.productors = []
        self.is_3d = None
        self.marketing_budget = None
        self.production_budget = None
        self.boxoffice = None

    def print_movie(self, id): # Permet d'afficher un film
        print(f"#{id} : {self.title}")

    def total_budget(self):
        if (self.production_budget == None or self.marketing_budget == None):
            return None
        
        return self.production_budget + self.marketing_budget