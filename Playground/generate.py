import csv
import string
import random

def generate_password(length):
    password = ''
    characters = string.ascii_uppercase + string.digits
    for i in range(length):
        password += random.choice(characters)
    return password

with open('input.csv', 'r') as input_file:
    reader = csv.reader(input_file)
    rows = []
    for row in reader:
        row.append(generate_password(8))
        rows.append(row)

with open('output.csv', 'w') as output_file:
    writer = csv.writer(output_file)
    writer.writerows(rows)
