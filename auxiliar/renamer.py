from re import compile, findall

label_regexp = compile(r'<rdfs:label>([a-zA-Z0-9]*)</rdfs:label>')

ontology_filepath = 'my_ontology.rdf'

# Read the ontology file
content = None
with open(ontology_filepath, 'r') as file:
    content = file.read()

# Set a function to check if the word is in camel case
def is_camel_case (string : str) -> bool:
    if ' ' in string or '_' in string: return False
    if not string[0].isupper: return False
    last_upper = True
    for letter in string[1:]:
        if not letter.isupper():
            last_upper = False
            continue
        if letter.isupper():
            if last_upper: return False
            last_upper = True
    return True

# Iterate matches
replaces = {}
for match in findall(label_regexp, content):
    # If the match is not in camel case then let it be, since it may be a name
    if not is_camel_case(match):
        #print(f'{match} -> No camel case')
        continue
    max_letter_index = len(match) - 1
    # Build a new name
    new_name = ''
    for l, letter in enumerate(match):
        # If it is not upper then there is nothing to do
        if not letter.isupper():
            new_name += letter
            continue
        # Check previous and next letters
        previous_letter = match[l-1] if l > 0 else None
        next_letter = match[l+1] if l < max_letter_index else None
        # In some cases we make
        if (not previous_letter or not previous_letter.isupper()) and next_letter and next_letter.islower():
            new_name += ' ' + letter.lower()
        elif previous_letter and previous_letter.islower():
            new_name += ' ' + letter
        # Leave it upper otherwise
        else:
            new_name += letter
    # Note that the first letter will have no previous space
    if new_name[0] == ' ':
        new_name = new_name[1:]
    # If it is the same then skip it
    if match == new_name: continue
    #raise SystemExit('Hold up')
    replaces[match] = new_name

# Now apply replacements
# Start with the longest keys, so there is not a small word replaced in a longer match
sorted_matches = [ match for match in replaces.keys() ]
sorted_matches.sort(key=len, reverse=True)
for match in sorted_matches:
    new_name = replaces[match]
    # Check how many times the match is present in the content, now that there were some replaces
    ocurrences = content.count(match)
    if ocurrences > 1:
        print(f'{match} -> {new_name} ({ocurrences})')
        continue
    # If there is only one then replace it
    content = content.replace(match, new_name)

# Write the ontology file
new_ontology_filepath = 'new_ontology.rdf'
with open(new_ontology_filepath, 'w') as file:
    file.write(content)