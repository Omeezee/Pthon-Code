# List of names
names = [
    'Staubach, Roger',  # Staubach is the last name
    'James Wellington',  # This name is fine
    'bocard-Demis, Andreana',  # Bocard-Demis is the last name, Bocard needs to be capitalized
    '/Roger William Boyanard',  # Remove '/' and William is the middle name
    'May, there?sa',  # May is the last name, capitalize Theresa and remove '?'
    'mary mariata-delores',  # Capitalize Mary, Mariata, and Delores
    'Alan Lindsay',  # This name is fine
    'Alan Lin?dsey',  # Remove '?' from Lindsey
    'Lindsay, Zach Isiah',  # Lindsay is the last name, Zach Isiah is first and middle name
    'Nancy genovese'  # Capitalize Genovese
]

# Cleaned full names will be stored here
full_names = []

# Process the names
for name in names:
    # Remove invalid characters
    name = name.replace('?', '').replace('/', '').replace(':', '')

    # Split last name first format (if present)
    if ',' in name:
        last, first = name.split(',', 1) 
        last = last.strip().capitalize()
        first = ' '.join([part.capitalize() for part in first.strip().split()])
    else:
        # Otherwise, capitalize each part of the name
        parts = name.strip().split()
        first = ' '.join([part.capitalize() for part in parts[:-1]])  # First and middle names
        last = parts[-1].capitalize()  # Last name

    # Handle hyphenated last names
    last = '-'.join([part.capitalize() for part in last.split('-')])

    # Combine first and last names
    cleaned_name = f"{first} {last}"
    
    # Append cleaned name to full_names list
    full_names.append(cleaned_name)

# Sort names alphabetically by last name
full_names.sort()

# Create tuple of related names (e.g., those with last name 'Lindsay')
relatives = tuple(name for name in full_names if 'Lindsay' in name)

# Create tuple of names with middle names (those with more than 2 parts)
with_middle_names = tuple(name for name in full_names if len(name.split()) > 2)

# Output the results without using \n in the formatting
print("Related People:")
for name in relatives:
    print(f"{name} has a relative")

print("People with middle names:")
for name in with_middle_names:
    print(name)

print("The cleaned-up and sorted list of names is as follows:")
for name in full_names:
    print(name)