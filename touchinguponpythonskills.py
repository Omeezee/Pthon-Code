##Create a Python program that helps users track their daily expenses. The program should allow users to:
#Add Expenses: Users can input the amount, category (e.g., food, transportation, entertainment), and a brief description of the expense.
#View Expenses: Users can view all their expenses in a list, sorted by date, category, or amount.
#Calculate Total Spending: The program should calculate and display the total amount spent over a ##specific period (e.g., daily, weekly, monthly).
#Set a Budget: Users can set a monthly budget, and the program should notify them when they are close to or exceed their budget.
#Generate Reports: Allow users to generate a summary report of their expenses, either as a text file or a simple chart (using a library like matplotlib).


## creat a user profile dictionary so that it can incure users expenses recuring, groceries, ect. 
#have it so users can view their expenses whenver they want 
#calcualte the total spending for specific time frames daily, monthly, or anualy
#help create a budget using simple math Ill make ti so that spending on groceries is 20% of spending 15% goes to saving ect.
#generate a report of the users exenses and has it so it can be a csv or other. 

user_dictionary = {
    "Daily Expenses",0,
    "Monthly Expenses", 0,
    "Yearly Expenses", 0,
    "Grocery Expenses", 0,
    "Subscription Expenses", 0,
    "Saving Expenses", 0,
   }
spending = input('What are you daily spendings for this month include type and expense')
seperated_list = [spending.split(",")]
# find a way to seperate the list from words and numbers while grouping words and numbers to create a category

