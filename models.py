class Bird:
    def __init__(self, obs, taxonomy_lookup):
        for key, value in obs.items():
            setattr(self, key, value)
        self.family = taxonomy_lookup.get(obs["speciesCode"], "Unkown")
        self.months = []

    def to_dict(self):
        return self.__dict__

    def add_months_seen(self, month):
        if month not in self.months:
            self.months.append(month)
