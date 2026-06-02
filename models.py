class Bird:
    def __init__(self, common_name, species_code, months):
        self.common_name = common_name
        self.species_code = species_code
        self.months = months

    def to_dict(self):
        return {
                "common_name": self.common_name,
                "species_code": self.species_code,
                "months": self.months
            }

