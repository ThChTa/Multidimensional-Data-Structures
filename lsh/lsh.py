from random import randint, shuffle

# Shingle function
def shingle(text: str, k: int):
    shingle_set = []
    for i in range(len(text) - k + 1):
        shingle_set.append(text[i:i+k])
    return set(shingle_set)

# One-hot encoding
def one_hot_encoding(vocab, data):
    one_hot = [1 if x in data else 0 for x in vocab]
    return one_hot

# MinHash

def create_hash_func(size: int):
    # Create a list of random hash values
    hash_ex = list(range(1, len(vocab)+1))
    shuffle(hash_ex)
    return hash_ex

def build_minhash_func(vocab_size: int, nbits: int):
    # Build multiple MinHash vectors
    hashes = []
    for _ in range(nbits):
        hashes.append(create_hash_func(vocab_size))
    return hashes

def create_hash(vector: list):
    # Create the signatures (matching)
    signature = []
    for func in minhash_func:
        for i in range(1, len(vocab)+1):
            idx = func.index(i)
            signature_val = vector[idx]
            if signature_val == 1:
                signature.append(idx)
                break
    return signature

def jaccard_similarity(set_a, set_b):
    #intersection_size = len(set_a.intersection(set_b))
    #union_size = len(set_a.union(set_b))
    return len(set_a.intersection(set_b)) / len(set_a.union(set_b))

# Test data
a = shingle('The first test is the best', 2)
b = shingle('It is the best', 2)

print("shingle a: ", a)
print("shingle b: ", b)

# Create vocabulary
vocab = a.union(b)
print("vocab:", vocab)

# One-hot encoding for sets a and b
result_a = one_hot_encoding(vocab, list(a))
result_b = one_hot_encoding(vocab, list(b))

# Create MinHash functions
minhash_func = build_minhash_func(len(vocab), 20)

# Create MinHash signatures
signature_a = create_hash(result_a)
signature_b = create_hash(result_b)

# Compute Jaccard similarity using MinHash signatures
jaccard_sim = jaccard_similarity(set(signature_a), set(signature_b)), jaccard_similarity(a,b)

print("Signature A:", signature_a)
print("Signature B:", signature_b)
print("Jaccard Similarity:", jaccard_sim)



# LSH 
def split_vector(signature, b):
    assert len(signature) % b == 0
    r = int(len(signature)/b)
#splitting signature in b parts
    subvecs = []
    for i in range(b, len(signature), r):
        subvecs.append(signature[i: i+r])

    return subvecs

band_a = split_vector(signature_a, 10)
print("Band A:", band_a)

band_b = split_vector(signature_b, 10)
print("Band B:", band_b)


for a_rows, b_rows in zip(band_a, band_b):
    if a_rows == b_rows:
        print(f"Candidate pair: {a_rows} == {b_rows}")
        break
    else:
        print("No candidate pair found!")
        break



