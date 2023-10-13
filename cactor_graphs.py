import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Read the CSV file
df = pd.read_csv("commits.csv")

# Create a folder with the current date and time as its name
current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
folder_name = f"CACTOR_DA_{current_time}"
os.makedirs(folder_name, exist_ok=True)

def save_plot(filename):
    plt.savefig(os.path.join(folder_name, filename))
    print(f"Graph saved as: {filename}")
    plt.close()

# Convert 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Create or open the text file to save the analysis data
txt_file_path = os.path.join(folder_name, "analysis_results.txt")
txt_file = open(txt_file_path, "w")

def save_to_txt(title, data, percentages=None):
    txt_file.write(f"{title}\n")
    if percentages is not None:
        combined_data = [f"{idx}: {val} ({pct:.1f}%)" for idx, val, pct in zip(data.index, data.values, percentages)]
        txt_file.write(f"{combined_data}\n")
    else:
        txt_file.write(f"{data}\n")
    txt_file.write("----------------------\n")



# 1. Commit Count by Author
plt.figure(figsize=(12, 7))
author_counts = df['Author'].value_counts()
ax = author_counts.plot(kind='pie', title='Commit Count by Author', autopct='%1.1f%%')
plt.legend(title='Authors', bbox_to_anchor=(1,1), loc="upper left")
save_plot('commit_count_by_author.png')

# Obtener porcentajes para guardar en txt
author_percentages = (author_counts / author_counts.sum()) * 100
save_to_txt('Commit Count by Author', author_counts, author_percentages)

# 2. Commit Distribution Over Time
plt.figure(figsize=(12, 7))
df['Day'] = df['Date'].dt.date
date_counts = df['Day'].value_counts().sort_index()
date_counts.plot(kind='line', title='Commit Distribution Over Time')
save_plot('commit_distribution_over_time.png')
save_to_txt('Commit Distribution Over Time', date_counts)

# 3. Commit Distribution by Branch
plt.figure(figsize=(12, 7))
branch_counts = df['Branch'].value_counts()
branch_counts.plot(kind='pie', title='Commit Distribution by Branch', autopct='%1.1f%%')
save_plot('commit_distribution_by_branch.png')
save_to_txt('Commit Distribution by Branch', branch_counts)

# 4. Most Active Days
plt.figure(figsize=(12, 7))
df['Weekday'] = df['Date'].dt.day_name()
weekday_counts = df['Weekday'].value_counts()
weekday_counts.plot(kind='pie', title='Most Active Days', autopct='%1.1f%%')
save_plot('most_active_days.png')
save_to_txt('Most Active Days', weekday_counts)

# 5. Commit Message Analysis
plt.figure(figsize=(12, 7))
df['Contains_merge'] = df['Message'].str.contains('merge')
view_counts = df['Contains_merge'].value_counts()
view_counts.plot(kind='pie', title='Commits Containing "merge"', labels=['Without "merge"', 'With "merge"'], autopct='%1.1f%%')
save_plot('commit_message_analysis.png')
save_to_txt('Commits Containing "merge"', view_counts)

# 6. Commit Frequency
plt.figure(figsize=(12, 7))
commit_frequency = df['Day'].value_counts().sort_index()
commit_frequency.plot(kind='bar', title='Commit Frequency')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
save_plot('commit_frequency.png')
save_to_txt('Commit Frequency', commit_frequency)

# 7. Commit Length Analysis
plt.figure(figsize=(12, 7))
df['Message_Length'] = df['Message'].str.len()
df['Message_Length'].plot(kind='hist', title='Commit Length Analysis', bins=20)
save_plot('commit_length_analysis.png')
save_to_txt('Commit Length Analysis', df['Message_Length'].describe())

# 8. Unique Branch Contributors
plt.figure(figsize=(12, 7))
unique_contributors = df.groupby('Branch')['Author'].nunique()
unique_contributors.plot(kind='bar', title='Unique Branch Contributors')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
save_plot('unique_branch_contributors.png')
save_to_txt('Unique Branch Contributors', unique_contributors)

# 9. Time Between Commits
plt.figure(figsize=(12, 7))
df['Time_Diff'] = df.sort_values('Date').groupby('Author')['Date'].diff().dt.total_seconds() / 3600  # in hours
avg_time_diff = df.groupby('Author')['Time_Diff'].mean()
avg_time_diff.plot(kind='bar', title='Average Time Between Commits (in hours)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
save_plot('time_between_commits.png')
save_to_txt('Average Time Between Commits (in hours)', avg_time_diff)

# 10. Commits Without Issues/Task Reference
plt.figure(figsize=(12, 7))
df['Contains_Issue'] = df['Message'].str.contains('issue', case=False) | df['Message'].str.contains('task', case=False)
issue_counts = df['Contains_Issue'].value_counts()
issue_counts.plot(kind='pie', title='Commits Without Issues/Task Reference', labels=['Without Issues/Task', 'With Issues/Task'], autopct='%1.1f%%')
save_plot('commits_without_issues.png')
save_to_txt('Commits Without Issues/Task Reference', issue_counts)

# 11. Author Collaboration
plt.figure(figsize=(12, 7))
collaboration_df = df.groupby(['Branch', 'Day'])['Author'].unique().reset_index()
collaboration_df['Collaborators'] = collaboration_df['Author'].apply(lambda x: ', '.join(x))
collaboration_counts = collaboration_df['Collaborators'].value_counts()
collaboration_counts.head(10).plot(kind='bar', title='Top 10 Author Collaborations')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
save_plot('author_collaboration.png')
save_to_txt('Top 10 Author Collaborations', collaboration_counts.head(10))

# 12. Commit Time Analysis
plt.figure(figsize=(12, 7))
df['Hour'] = df['Date'].dt.hour
hourly_counts = df['Hour'].value_counts().sort_index()
ax = hourly_counts.plot(kind='bar', title='Commit Time Analysis')
ax.legend(["Commits"])
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
save_plot('commit_time_analysis.png')
save_to_txt('Commit Time Analysis', hourly_counts)

# 13. Commit Trend Analysis
plt.figure(figsize=(12, 7))
daily_commits = df['Day'].value_counts().sort_index()
daily_commits.plot(kind='line', title='Commit Trend Over Time')
save_plot('commit_trend_analysis.png')
save_to_txt('Commit Trend Over Time', daily_commits)

# 14. Commit Impact Analysis
plt.figure(figsize=(12, 7))
df['Impact'] = df['Message_Length'].apply(lambda x: 'Low' if x < 50 else ('Medium' if x < 100 else 'High'))
impact_counts = df['Impact'].value_counts()
impact_counts.plot(kind='pie', title='Commit Impact Analysis (based on message length)', autopct='%1.1f%%')
save_plot('commit_impact_analysis.png')
save_to_txt('Commit Impact Analysis (based on message length)', impact_counts)

# 15. Keyword Alerts
keywords = ['bug', 'fix', 'error', 'feature', 'update', 'refactor', 'add', 'delete', 'improve', 'docs']

for keyword in keywords:
    plt.figure(figsize=(12, 7))
    df[f'Contains_{keyword}'] = df['Message'].str.contains(keyword, case=False)
    keyword_counts = df[f'Contains_{keyword}'].value_counts()
    without_keyword_count = keyword_counts[False] if False in keyword_counts else 0
    with_keyword_count = keyword_counts[True] if True in keyword_counts else 0
    keyword_counts.plot(kind='pie', title=f'Commits With/Without "{keyword}"', labels=None, autopct='%1.1f%%', startangle=140)
    plt.legend(labels=[f'Without "{keyword}" ({without_keyword_count})', f'With "{keyword}" ({with_keyword_count})'], loc="best")
    save_plot(f'keyword_alerts_{keyword}.png')
    save_to_txt(f'Commits With/Without "{keyword}"', keyword_counts)

txt_file.close()

print("\n--------------------------------------------\nCACTOR: Data analysis complete. Graphs and text file saved to directory successfully.")
