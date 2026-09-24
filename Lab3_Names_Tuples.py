names = []
names.append('Staubach, Roger') # staubach is the last name 
names.append('James Wellington') # this name is aight
names.append('bocard-Demis, Andreana') # bocard-Demis is the last name and bocard needs to be Capital 
names.append('/Roger William Boyanard') # need to reomve / ## has a middle name 
names.append('May, there?sa') # may is the last name need to capitalize theresa and remove ?
names.append('mary mariata-delores') #need to capitalize mary mariata and delores
names.append('Alan Lindsay') # this name works ## related to zach 
names.append('Alan Lin?dsey') # same name as above remove ?
names.append('Lindsay, Zach Isiah') # Lindsay is last name Zach is a first name ## has a middle name related to alan lindsay 
names.append('Nancy genovese') #need to capitalize genovese
tup_names = tuple(names)
#print(tup_names)
                    ##rules
#There must be no leading or trailing white spaces in a full name
#There can be only 1 white space between the words in a full name
#Once cleaned up:
              #a. The alphabetically ordered (by last name) full names must be stored in the list
              #‘full_names’,
              #b. The full names of related people must be stored in a tuple called ‘relatives’,
              #c. The full names of people with middle names must be stored in a tuple called
              #‘with_middle_names
              
#create a range object to prevent creating one agian and again
theRange = range(len(tup_names))
#create an empty list
full_names = [None]*len(names)

 
# Start processing the names based on rules
for i in theRange:
    name = tup_names[i]
    
    # Remove invalid characters
    name = name.replace('?', '').replace('/', '').replace(':', '')
    
    # Split last name first format (if present)
    if ',' in name:
        last, first = name.split(',', 1) #google explained it as a way to split the list in one part at the , 
        last = last.strip().capitalize()
        first = ' '.join([part.capitalize() for part in first.strip().split()])
        cleaned_name = f"{first} {last}"
    else:
        # Otherwise, capitalize each part of the name
        cleaned_name = ' '.join([part.capitalize() for part in name.strip().split()])
    
    # Store cleaned name in full_names list
    full_names[i] = cleaned_name

# Sort full names alphabetically by last name # I found this line of code online to sort names I was trying to see if there was a function that could automatically sort the names 
full_names.sort()

# Create tuple of related names (e.g., those with last name 'Lindsay')
relatives = tuple(name for name in full_names if 'Lindsay' in name)

# Create tuple of names with middle names (those with more than 2 parts)
with_middle_names = tuple(name for name in full_names if len(name.split()) > 2)

# Output the results
#print("Full names (sorted):", full_names)
#print("Relatives:", relatives)
#print("With middle names:", with_middle_names)

# Related people section
# had to google this print style as well inorder to make it the same format as needed (how could we make the formating better without using a for statment?)
print("Related People:")
for name in relatives:
    print(f"{name} has a relative")

# People with middle names sectionnbjha
print("People with middle names:")
for name in with_middle_names:
    print(f"{name}")

# The cleaned-up and sorted list section
print("The cleaned-up and sorted list of names is as follows:")
for name in full_names:
    print(f"{name}")
