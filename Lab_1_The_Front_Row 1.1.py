# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 20:57:22 2024

@author: geode
"""
# lab 1

import random

# List of students (fixed order)
students = ['Jeremy', 'Alan', 'David', 'Brittany', 'Zuhib', 'Sammy', 'Calvin']

# Get input from the user
user_input = input("Enter '?' to randomly select a crew-chief for Sunday or enter the name of a student: ")

# Select crew-chief for Sunday based on user input
if user_input == '?':  # Random selection
    n = random.randint(0, 6)
    crew_chief_sunday = students[n]
    print(f"{students[n]} was selected as the crew-chief for Sunday")
else:
    crew_chief_sunday = user_input
    print(f"{crew_chief_sunday} was selected as the crew-chief for Sunday")

# Handle Jeremy's special case: if Jeremy is selected as Sunday crew-chief, switch with Brittany
if crew_chief_sunday == 'Jeremy':
    crew_chief_sunday = 'Brittany'
    print("NOTE: Jeremy switched his Sunday shift with Brittany due to their deal.")

# Create the schedule starting from the selected crew-chief
sunday_index = students.index(crew_chief_sunday)
final_schedule = students[sunday_index:] + students[:sunday_index]

# Handle Sammy and Gabriel's special case
if crew_chief_sunday == 'Sammy':
    final_schedule.insert(1, 'Gabriel')  # Add Gabriel right after Sammy
    print("NOTE: Sammy cannot work Sunday shifts alone")
    
# this is to make sure that Gabriel is listed before Sammy
if 'Sammy' in final_schedule and 'Gabriel' in final_schedule:
    sammy_index = final_schedule.index('Sammy')
    gabriel_index = final_schedule.index('Gabriel')
    if gabriel_index > sammy_index:
        final_schedule[sammy_index], final_schedule[gabriel_index] = final_schedule[gabriel_index], final_schedule[sammy_index]

# Handle Calvin's special case: Swap Monday shift if Calvin is scheduled for Monday
if final_schedule[1] == 'Calvin':
    final_schedule[1], final_schedule[2] = final_schedule[2], final_schedule[1]
    print("NOTE: Calvin has a deal for not working Mondays")

# Print the final schedule
print("The final schedule for the week is:")
print(f"Sunday: {final_schedule[0]}")
print(f"Monday: {final_schedule[1]}")
print(f"Tuesday: {final_schedule[2]}")
print(f"Wednesday: {final_schedule[3]}")
print(f"Thursday: {final_schedule[4]}")
print(f"Friday: {final_schedule[5]}")
print(f"Saturday: {final_schedule[6]}")