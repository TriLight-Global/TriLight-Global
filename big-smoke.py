class DecisionTree:
    def __init__(self):
        self.business_model = None
        self.store_locations = None
        self.age_verification_needed = None
        self.loyalty_program_desired = None

    def decide(self):
        self.determine_business_model()
        self.determine_store_locations()
        self.determine_age_verification_needed()
        self.determine_loyalty_program_desired()

        if self.business_model == "online_only":
            return "Website"
        elif self.business_model == "physical_only":
            if self.store_locations > 1:
                return "Website with Store Locator"
            else:
                return "Simple Website"
        elif self.business_model == "hybrid":
            if self.age_verification_needed:
                return "Mobile App with Age Verification"
            elif self.loyalty_program_desired:
                return "Mobile App with Loyalty Program"
            else:
                return "Responsive Website"

    def determine_business_model(self):
        print("What is your business model?")
        print("1. Online-only sales")
        print("2. Physical store(s) only")
        print("3. Hybrid (both online and physical)")
        choice = input("Enter your choice (1/2/3): ")
        self.business_model = {
            "1": "online_only",
            "2": "physical_only",
            "3": "hybrid"
        }.get(choice)

    def determine_store_locations(self):
        if self.business_model != "physical_only":
            return
        self.store_locations = int(input("How many physical store locations do you have? "))

    def determine_age_verification_needed(self):
        self.age_verification_needed = input("Do you need age verification for purchases? (y/n): ").lower() == 'y'

    def determine_loyalty_program_desired(self):
        self.loyalty_program_desired = input("Do you want to implement a loyalty program? (y/n): ").lower() == 'y'


# Usage
tree = DecisionTree()
result = tree.decide()
print(f"Based on your inputs, you should create a {result}.")
