def classify_animal_forward_chaining(initial_characteristics):
    known_facts = set(initial_characteristics)

    rules = [
        {"if_conditions": ["punya sayap", "bertelur", "punya bulu"], "then_conclusion": "Burung"},
        {"if_conditions": ["hidup di air", "punya sisik", "bertelur"], "then_conclusion": "Ikan"},
        {"if_conditions": ["punya bulu", "menyusui"], "then_conclusion": "Mamalia"},
        {"if_conditions": ["berkaki empat", "menyusui"], "then_conclusion": "Mamalia"},
        {"if_conditions": ["bertelur", "punya sisik", "tidak berkaki"], "then_conclusion": "Reptil"},
        {"if_conditions": ["bertelur", "punya sisik", "berkaki empat"], "then_conclusion": "Reptil"},
    ]

    new_fact_added = True
    iteration_count = 0

    print(f"Initial characteristics: {known_facts}")
 
    while new_fact_added:
        new_fact_added = False
        iteration_count += 1
        print(f"\n--- Iteration {iteration_count} ---")

        for rule in rules:
            all_conditions_met = True
            for condition in rule["if_conditions"]:
                if condition not in known_facts:
                    all_conditions_met = False
                    break

            if all_conditions_met and rule["then_conclusion"] not in known_facts:
                known_facts.add(rule["then_conclusion"])
                new_fact_added = True
                print(f"  Rule fired: {rule['if_conditions']} -> {rule['then_conclusion']}")
                print(f"  Known facts updated: {known_facts}")

    print("\n--- Forward Chaining Finished ---")

    animal_categories = {"Burung", "Ikan", "Mamalia", "Reptil", "Amfibi"}
    found_category = None
    for fact in known_facts:
        if fact in animal_categories:
            found_category = fact
            break

    if found_category:
        print(f"The animal is classified as: {found_category}")
    else:
        print("Could not classify the animal based on the given characteristics.")
        print(f"All derived facts: {known_facts}")

if __name__ == "__main__": 
    print("--- Classifying a Bird ---")
    characteristics_bird = ["punya sayap", "bertelur", "punya bulu"]
    classify_animal_forward_chaining(characteristics_bird)

    print("\n" + "="*50 + "\n")

    print("--- Classifying a Fish ---")
    characteristics_fish = ["hidup di air", "punya sisik", "bertelur"]
    classify_animal_forward_chaining(characteristics_fish)

    print("\n" + "="*50 + "\n")

    print("--- Classifying a Mammal ---")
    characteristics_mammal = ["punya bulu", "menyusui", "berkaki empat"]
    classify_animal_forward_chaining(characteristics_mammal)

    print("\n" + "="*50 + "\n")

    print("--- Classifying an Unclassified Animal (e.g., has scales only) ---")
    characteristics_unknown = ["punya sisik"]
    classify_animal_forward_chaining(characteristics_unknown)