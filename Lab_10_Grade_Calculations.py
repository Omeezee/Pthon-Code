import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data
file_path = 'C:/Users/geode/Downloads/Final_Exam_Data.xlsx'
df_in = pd.read_excel(file_path)

# Remove the row of maximum scores (row 0) and save them for calculations
max_scores = df_in.iloc[0]
df_out = df_in.iloc[1:].copy()

# Initialize constants
N = 8  # Number of top quizzes to include
assignment_weights = {'SQ': 0.1, 'LAB': 0.3, 'QZ': 0.3, 'FNL': 0.3}

# Calculate overall scores for SQ, LAB, and FNL
for assignment_type in ['SQ', 'LAB', 'FNL']:
    relevant_cols = [col for col in df_in.columns if assignment_type in col]
    total_scores = df_out[relevant_cols].sum(axis=1)
    max_possible = max_scores[relevant_cols].sum()
    df_out[f'Overall {assignment_type}'] = ((total_scores / max_possible) * 100).round()

# Calculate overall score for quizzes (QZ) considering the top N quizzes
quiz_cols = [col for col in df_in.columns if 'QZ' in col]
quiz_scores = df_out[quiz_cols].apply(pd.to_numeric, errors='coerce').fillna(0)
normalized_quiz_scores = quiz_scores.div(max_scores[quiz_cols], axis=1)
sorted_quiz_scores = normalized_quiz_scores.apply(
    lambda row: row.sort_values(ascending=False).iloc[:N].sum(), axis=1
)
df_out['Overall QZ'] = (sorted_quiz_scores / N * 100).round()

# Calculate final grades
df_out['Final Grade'] = (
    df_out['Overall SQ'] * assignment_weights['SQ'] +
    df_out['Overall LAB'] * assignment_weights['LAB'] +
    df_out['Overall QZ'] * assignment_weights['QZ'] +
    df_out['Overall FNL'] * assignment_weights['FNL']
).round()

# Assign letter grades based on final grade
def get_letter_grade(score):
    if score >= 97: return 'A+'
    elif score >= 90: return 'A'
    elif score >= 87: return 'B+'
    elif score >= 80: return 'B'
    elif score >= 77: return 'C+'
    elif score >= 70: return 'C'
    elif score >= 67: return 'D+'
    elif score >= 60: return 'D'
    return 'F'

df_out['Letter Grade'] = df_out['Final Grade'].apply(get_letter_grade)

# Determine pass/fail
df_out['Pass/Fail'] = np.where(
    (df_out['Overall SQ'] >= 50) & (df_out['Final Grade'] >= 60),
    'Pass', 'Fail'
)

# Save results to Excel
output_path = 'C:/Users/geode/Downloads/Lab_10_Output.xlsx'
df_out.to_excel(output_path, index=False)

# Plot results
plt.figure(figsize=(7, 10))

# Histogram of final grades
plt.subplot(2, 1, 1)
plt.hist(df_out['Final Grade'], bins=7, edgecolor='black')
plt.title('Distribution of Final Grades')
plt.xlabel('Final Grade (%)')
plt.ylabel('Number of Students')
plt.grid(True)

# Crossplot of quiz grades vs final grades
plt.subplot(2, 1, 2)
plt.scatter(df_out['Overall QZ'], df_out['Final Grade'], color='red', marker='+')
plt.title('Quiz Grades vs Final Grades')
plt.xlabel('Quiz Grade (%)')
plt.ylabel('Final Grade (%)')
plt.grid(True)

# Save the plot
plot_path = 'C:/Users/geode/Downloads/Lab_10_Plot.png'
plt.tight_layout()
plt.savefig(plot_path)
plt.show()

print(f"Results saved to {output_path}")
print(f"Plot saved to {plot_path}")
