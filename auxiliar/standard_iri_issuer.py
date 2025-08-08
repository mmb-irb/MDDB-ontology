from re import compile, findall

# Convert autmatically generated IRIs to our standard formatted IRIs

# IRIs issued by us and used in MDposit
# e.g. mdposit.mddbr.eu/mdo/MDO_000416
MDDB_IRI_REGEXP = compile(r'mdposit.mddbr.eu/mdo/MDO_([0-9]{6})')

# IRIs issued by web protege
# e.g. "http://webprotege.stanford.edu/R70emL4KdWEgkaAd2x7dp"
# e.g. "http://webprotege.stanford.edu/RsU5VIce0HoiFnHAEdGKeU"
# e.g. "http://webprotege.stanford.edu/RCQmuhlj988OmKhyks4tWaq"
WEBPROTEGE_IRI_REGEXP = compile(r'http://webprotege.stanford.edu/[-a-zA-Z0-9]+')

# IRIs issued by protege desktop
# e.g. "urn:webprotege:ontology:c5ff078b-f379-4d8f-903f-1ec3d21639f0#lipid21"
PROTEGE_IRI_REGEXP = compile(r'urn:webprotege:ontology:c5ff078b-f379-4d8f-903f-1ec3d21639f0#[-_a-zA-Z0-9]+')

# IRIs issued by protege desktop after changing the ontology name
# e.g. mdposit.mddbr.eu/mdo#ion_parameters
PROTEGE_MDDB_IRI_REGEXP = compile(r'mdposit.mddbr.eu/mdo#[-_a-zA-Z0-9]+')

# Read the ontology file
ontology_filepath = 'ontology.rdf'
content = None
with open(ontology_filepath, 'r') as file:
    content = file.read()

# Find the latest issued IRI
issued_codes = findall(MDDB_IRI_REGEXP, content)
last_issued_iri = max([ int(code) for code in issued_codes ])
print(f'Last issued IRI was MDO_{str(last_issued_iri).zfill(6)}')

# Set a counter to not repeat new issued codes
# We keep the first 100 numbers for core classes
counter = last_issued_iri + 1
# Get all matches together
matches = set([
    *findall(WEBPROTEGE_IRI_REGEXP, content),
    *findall(PROTEGE_IRI_REGEXP, content),
    *findall(PROTEGE_MDDB_IRI_REGEXP, content)
])
print(f'Found {len(matches)} different IRIs')
# Replace every match with a standard URL issuing a new code
for match in matches:
    # Issue the new IRI
    new_code = f'MDO_{str(counter).zfill(6)}'
    new_iri = 'mdposit.mddbr.eu/mdo/' + new_code
    print(f'{match} -> {new_iri}')
    # Add 1 to thecounter
    counter += 1
    # Replace old IRI with the new IRI
    content = content.replace(match, new_iri)

# Write the ontology file
new_ontology_filepath = 'issued_ontology.rdf'
with open(new_ontology_filepath, 'w') as file:
    file.write(content)