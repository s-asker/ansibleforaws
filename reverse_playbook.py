import yaml

def reverse_playbook(input_file, output_file):
    # Read the original playbook
    with open(input_file, 'r') as file:
        playbook = yaml.safe_load(file)

    # Get the tasks and reverse them
    tasks = playbook[0]['tasks']
    reversed_tasks = tasks[::-1]

    # Prepare the new playbook structure for deletion
    new_playbook = {
        'hosts': playbook[0]['hosts'],
        'connection': playbook[0]['connection'],
        'gather_facts': playbook[0]['gather_facts'],
        'tasks': []
    }

    # Modify tasks for deletion
    for task in reversed_tasks:
        # Change the state to 'absent' for deletion
        delete_task = task.copy()
        delete_task['state'] = 'absent'
        new_playbook['tasks'].append(delete_task)

    # Write the new playbook to the output file
    with open(output_file, 'w') as file:
        yaml.dump([new_playbook], file, default_flow_style=False)

if __name__ == "__main__":
    input_file = 'vpc.yml'  # Change to your input file name
    output_file = 'vpc_teardown.yml'  # Change to your desired output file name
    reverse_playbook(input_file, output_file)
    print(f"Reversed playbook saved as {output_file}")
