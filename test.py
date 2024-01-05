import pandas as pd
from rtree import index
import numpy as np


#Μετατροπή γράμματος σε αριθμό 
def letter_to_number(letter):
    return ord(letter.lower()) - 97

class RTreeIndexer:
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file)#διαβάζουμε το csv αρχείο
        self.datas = []#εδώ θα γίνει αποθήκευση των δεδομένων από το csv αρχείο για χρήση στα queries
        #εδώ φτιάχνουμε τα properties του r-tree για 3 διαστάσεις
        p = index.Property()
        p.dimension = 3 
        p.dat_extension = 'data'
        p.idx_extension = 'index'
        self.idx3d = index.Index(properties=p) 
        #φτιάχνουμε το index με τα δεδομένα
        self._build_index()

    def _build_index(self):
        #insert στο r-tree
        for i, row in self.data.iterrows():
            
            surname = letter_to_number(row['lastName'][0])
            awards = row['awards']
            dblp_record = row['dblp_records']
            education = row['education']
            self.idx3d.insert(i, (surname, awards, dblp_record, surname, awards, dblp_record)) #πέρασμα row στο r-tree
            data =(row['lastName'], row['awards'], row['education'], row['dblp_records'])#αποθήκευση στην λίστα μας
            self.datas.append(data)
            

    def query(self, left_letter, right_letter, awards_min, dblp_min, dblp_max):
        
        left_letter=letter_to_number(left_letter)
        right_letter=letter_to_number(right_letter)
        query_coordinates = (float(left_letter), awards_min, dblp_min, float(right_letter), float('inf'), dblp_max)#συντεταγμένες του query για να πάρουμε τα σχετικά αποτελέσματα
        
        results = list(self.idx3d.intersection(query_coordinates))
        print(results)
        #δομημένη επιστροφή των αποτελεσμάτων της αναζήτησης για χρήση τους στην πορεία
        query_results = []
        for result in results:
            lastName, awards, education, dblp_records = self.datas[result]
            query_results.append({"lastName": lastName, "awards": awards, "education": education, "dblp_records": dblp_records})
        
        return query_results

rtree = RTreeIndexer(r'C:\Users\Thomas\Desktop\Multidimensional-Data-Structures\data\scientists_data_complete.csv')
query_results=rtree.query('A', 'A', 3, 0, 200)
#print(query_results)

#create an array for the education for LSH
education_strings = [result["education"].encode('utf-8') for result in query_results]
education_array = np.array(education_strings)
print("len = ",len(education_array))
#print(education_array) print education_array




from random import randint, shuffle

#Shingle function
def shingle(text: str, k: int):
    shingle_set = []
    for i in range(len(text) - k + 1):
        shingle_set.append(text[i:i+k])
    return set(shingle_set)

#One-hot encoding
def one_hot_encoding(vocab, data):
    one_hot = [1 if x in data else 0 for x in vocab]
    return one_hot

#MinHash

def create_hash_func(size: int):
    #Create a list of random hash values
    hash_ex = list(range(1, size + 1))
    shuffle(hash_ex)
    return hash_ex

def build_minhash_func(vocab_size: int, nbits: int, num_hashes: int):
    #Build multiple MinHash vectors
    hashes = []
    for _ in range(num_hashes):
        hashes.append(create_hash_func(vocab_size))
    return hashes

def create_hash(vector: list, minhash_func):
    #Create the signatures (matching)
    signature = []
    for func in minhash_func:
        for i in range(1, len(vector) + 1):
            if vector[i-1] == func:
                signature.append(i-1)
                break
    return signature




def jaccard_similarity(set_a, set_b):
    return len(set_a.intersection(set_b)) / len(set_a.union(set_b))

#LSH 
def split_vector(signature, b):
    assert len(signature) % b == 0
    r = int(len(signature)/b)
    #Splitting signature into b parts
    subvecs = []
    for i in range(b, len(signature), r):
        subvecs.append(signature[i: i+r])
    return subvecs

#Function to perform LSH for multiple strings
def lsh_for_multiple_strings(strings, k, nbits, bands):
    #Create shingles and vocabulary
    shingles = [shingle(s, k) for s in strings]
    vocab = set().union(*shingles)

    #One-hot encoding for each string
    one_hots = [one_hot_encoding(vocab, list(s)) for s in shingles]

    #Create MinHash functions
    minhash_func = build_minhash_func(len(vocab), nbits, num_hashes=len(strings))

    #Create MinHash signatures for each string
    signatures = [create_hash(one_hot, minhash_func[i]) for i, one_hot in enumerate(one_hots)]

    #Perform LSH
    for i in range(len(strings)):
        for j in range(i + 1, len(strings)):
            jaccard_sim = jaccard_similarity(set(signatures[i]), set(signatures[j]))
            print(f"Jaccard Similarity between {i+1} and {j+1}: {jaccard_sim}")

    #Optional: Use LSH to find potential candidate pairs

#Test data
strings = ['The first test is the best', 'It is the best', 'One more string best']

#Call the function with the test data
lsh_for_multiple_strings(education_array, k=2, nbits=20, bands=10)

