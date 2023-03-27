import ast
from flask import Flask, jsonify, request

app = Flask(__name__)

"""It takes the data from the request, creates a new voter with the data, and writes the new voter to
    the voters.txt file.
    :return: A JSON object containing the details of the new voter.
    """
# Endpoint to register a voter
@app.route('/voters', methods=['POST'])
def register_voter():
    data = request.get_json()
    
    # Check for existing voters with the same ID or email
    with open('voters.txt', 'r') as f:
        for line in f:
            voter = eval(line)
            if voter['id'] == data['id']:
                return jsonify({'error': 'Voter with this ID already exists.'})
            elif voter['email'] == data['email']:
                return jsonify({'error': 'Voter with this email already exists.'})
    
    # Add the new voter
    new_voter = {'id': data['id'], 'name': data['name'], 'student_id': data['student_id'], 'email': data['email'], 
                 'year_group': data['year_group'], 'major': data['major']}
    with open('voters.txt', 'a') as f:
        f.write(str(new_voter) + '\n')
    return jsonify(new_voter)

"""
    It opens the file, reads all the lines, iterates over the lines, and if the voter id matches the
    voter id in the request, it deletes the line from the file
    
    :param voter_id: The id of the voter to be de-registered
    :return: A JSON object with a message or error.
"""
# Endpoint to de-register a voter
@app.route('/voters/<int:voter_id>', methods=['DELETE'])
def deregister_voter(voter_id):
    lines = []
    with open('voters.txt', 'r') as f:
        lines = f.readlines()
    for i in range(len(lines)):
        voter = eval(lines[i])
        if voter['id'] == voter_id:
            del lines[i]
            with open('voters.txt', 'w') as f:
                f.writelines(lines)
            return jsonify({'message': f'Voter with id {voter_id} has been successfully de-registered.'})
    return jsonify({'error': 'Voter not found.'})

"""
    It opens the voters.txt file, reads all the lines, loops through the lines, and if the voter id
    matches the voter_id parameter, it updates the voter with the data from the request, and writes the
    updated voter to the voters.txt file
    
    :param voter_id: The ID of the voter to update
    :return: The voter is being returned.
"""
# Endpoint to update a voter's information
@app.route('/voters/<int:voter_id>', methods=['PUT'])
def update_voter(voter_id):
    lines = []
    with open('voters.txt', 'r') as f:
        lines = f.readlines()
    for i in range(len(lines)):
        voter = eval(lines[i])
        if voter['id'] == voter_id:
            data = request.get_json()
            for key in data.keys():
                voter[key] = data[key]
            lines[i] = str(voter) + '\n'
            with open('voters.txt', 'w') as f:
                f.writelines(lines)
            return jsonify(voter)
    return jsonify({'error': 'Voter not found.'})

"""
    It opens the file, reads all the lines, and then loops through each line, converting it to a
    dictionary, and then checking if the id matches the voter_id passed in. If it does, it returns the
    voter. If it doesn't, it returns an error
    
    :param voter_id: The ID of the voter to retrieve
    :return: A JSON object containing the voter's information.
"""
# Endpoint to retrieve a voter
@app.route('/voters/<int:voter_id>', methods=['GET'])
def get_voter(voter_id):
    lines = []
    with open('voters.txt', 'r') as f:
        lines = f.readlines()
    for line in lines:
        voter = eval(line)
        if voter['id'] == voter_id:
            return jsonify(voter)
    return jsonify({'error': 'Voter not found.'})

"""
    It takes the data from the request, creates a new election object, and writes it to the
    elections.txt file
    :return: The new election is being returned.
"""
# Endpoint to create an election
@app.route('/elections', methods=['POST'])
def create_election():
    data = request.get_json()
    
    # Check for existing election with the same ID
    with open('elections.txt', 'r') as f:
        for line in f:
            election = eval(line)
            if election['id'] == data['id']:
                return jsonify({'error': 'Election with this ID already exists.'})
    
    # Add the new election
    new_election = {'id': data['id'], 'name': data['name'], 'description': data['description'], 
                    'candidates': data['candidates'], 'voters': [], 'votes': data['votes']}
    with open('elections.txt', 'a') as f:
        f.write(str(new_election) + '\n')
    return jsonify(new_election)

"""
    It reads the elections.txt file, finds the election with the given id, and returns it as a JSON
    object
    
    :param election_id: The ID of the election to retrieve
    :return: A JSON object containing the election with the given ID.
"""
# Endpoint to retrieve an election
@app.route('/elections/<int:election_id>', methods=['GET'])
def get_election(election_id):
    lines = []
    with open('elections.txt', 'r') as f:
        lines = f.readlines()
    for line in lines:
        election = eval(line)
        if election['id'] == election_id:
            return jsonify(election)
    return jsonify({'error': 'Election not found.'})

"""
    It opens the file, reads all the lines, opens the file again, and writes all the lines except the
    one that matches the election_id
    
    :param election_id: The ID of the election to delete
    :return: a JSON object with a message or an error.
"""
# Endpoint to delete an election
@app.route('/elections/<int:election_id>', methods=['DELETE'])
def delete_election(election_id):
    lines = []
    with open('elections.txt', 'r') as f:
        lines = f.readlines()
    with open('elections.txt', 'w') as f:
        deleted = False
        for line in lines:
            election = eval(line)
            if election['id'] == election_id:
                deleted = True
            else:
                f.write(line)
        if deleted:
            return jsonify({'message': 'Election deleted.'})
        else:
            return jsonify({'error': 'Election not found.'})

"""
    It takes in a voter_id, candidate_name, and election_name, and if the voter_id is not in the
    election's voters list, it adds the voter_id to the voters list, and adds 1 to the candidate's vote
    count
    :return: a JSON object with a message or error.
"""
# Endpoint to vote in an election
@app.route('/vote', methods=['POST'])
def vote():
    data = request.get_json()
    voter_id = data['voter_id']
    candidate_name = data['candidate_name']
    election_id = data['election_id']
    canditate_names = []
    voters =[]
    
    with open('voters.txt', 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        voter = ast.literal_eval(line.strip())
        voters.append(voter['id'])
    if voter_id not in voters:
        return jsonify({'error': 'Voter not found.'})


    with open('elections.txt', 'r') as f:
        lines = f.readlines()
        
    for line in lines:
        election = ast.literal_eval(line.strip())
        if election['id'] == election_id:
            for candidate in election['candidates']:
                canditate_names.append(candidate['name'])
            if voter_id in election['voters']:
                return 'You have already voted in this election'
            elif candidate_name not in canditate_names:
                return 'Candidate not found'
            else:
                election['votes'][candidate_name] = election['votes'].get(candidate_name, 0) + 1
                election['voters'].append(voter_id)
                with open('elections.txt', 'w') as f:
                    for l in lines:
                        if l.strip() != line.strip():
                            f.write(l)
                    f.write(str(election) + '\n')
                return jsonify({"message": "Vote recorded successfully"})
    return jsonify({'error': 'Election not found.'})

if __name__ == '__main__':
    app.run(debug=True)
   
