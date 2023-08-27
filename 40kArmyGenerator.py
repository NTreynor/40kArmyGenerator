import csv
import random

def load_units_from_csv(file_path):
    units = []
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        #headers = reader.fieldnames
        #print("CSV Headers:", headers)
        for row in reader:
            units.append({
                'name': row['name'],
                'cost': int(row['cost']),
                'role': row['role'],
                'max': int(row['max']),
                'current_count': 0
            })
    return units

def build_army(units, total_points, max_characters):
    army = []
    total_cost = 0
    character_count = 0

    # Shuffle the units list
    random.shuffle(units)

    # Track roles that are already added to ensure at least one of each role type
    added_roles = set()

    # Ensuring at least one of each type of role is present
    for unit in units:
        if unit['role'] in added_roles:  # Skip if this role is already added
            continue
        if total_cost + unit['cost'] <= total_points and unit['current_count'] < unit['max']:
            if unit['role'] == 'character' and character_count >= max_characters:
                continue
            army.append(unit)
            total_cost += unit['cost']
            unit['current_count'] += 1
            if unit['role'] == 'character':
                character_count += 1
            added_roles.add(unit['role'])  # Mark this role as added

    # After ensuring one of each role, continue to add units until no affordable unit can be added
    while True:
        affordable_units = [unit for unit in units if total_cost + unit['cost'] <= total_points and unit['current_count'] < unit['max']]
        
        if not affordable_units:
            break
        
        unit = random.choice(affordable_units)
        if unit['role'] == 'character' and character_count >= max_characters:
            continue

        army.append(unit)
        total_cost += unit['cost']
        unit['current_count'] += 1

        if unit['role'] == 'character':
            character_count += 1

    return army



def main():
    while True:
        print()
        total_points = int(input("Enter the total points for the army: "))
        max_characters = int(input("Enter the maximum number of characters: "))

        units = load_units_from_csv('orks.csv')
        army = build_army(units, total_points, max_characters)
        army = sorted(army, key=lambda x: x['role'])  # Sort by role

        print("\nGenerated Army List:")
        for unit in army:
            print(f"{unit['name']} - {unit['cost']} points - Role: {unit['role']}")


if __name__ == '__main__':
    main()