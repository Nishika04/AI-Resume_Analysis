import json
import matplotlib.pyplot as plt

def plot_career_trajectory(json_file):
    # Load the JSON data (career trajectory info)
    with open(json_file, 'r') as f:
        data = json.load(f)

    # If there are no career entries in the data, print a message
    if not data.get('career_path'):
        print("No career experience found. Plot not generated.")
        return

    # Extract years and job titles from the career path data
    years = [entry['year'] for entry in data['career_path']]
    titles = [entry['title'] for entry in data['career_path']]

    # Plot the data
    plt.figure(figsize=(12, 6))
    plt.plot(years, titles, marker='o', linestyle='-', color='b')  # Line plot with points
    plt.title('Career Trajectory Timeline')
    plt.xlabel('Year')
    plt.ylabel('Job Title')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()  # Adjust layout to prevent clipping
    plt.savefig('resume-report/career_trajectory_graph.png')  # Save the graph image
    plt.show()  # Display the graph
