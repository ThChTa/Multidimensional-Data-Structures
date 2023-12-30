from random import randint, shuffle

# Shingle function
def shingle(text: str, k: int):
    shingle_list = []
    for i in range(len(text) - k + 1):
        shingle_list.append(text[i:i+k])
    return shingle_list

# One-hot encoding
def one_hot_encoding(vocab, data):
    one_hot = [1 if x in data else 0 for x in vocab]
    return one_hot

# MinHash

def create_hash_func(size: int):
    # Create a list of random hash values
    hash_ex = [randint(1, 1000) for _ in range(size)]
    return hash_ex

def build_minhash_func(vocab_size: int, nbits: int):
    # Build multiple MinHash vectors
    hashes = []
    for _ in range(nbits):
        hashes.append(create_hash_func(vocab_size))
    return hashes

def create_hash(vector: list, hash_ex: list):
    # Create the signatures (matching)
    signature = []
    for func in minhash_func:
        min_hash_value = float('inf')  # Initialize with positive infinity
        for i in range(len(vocab)):
            if vector[i] == 1:
                # Hash the index using the hash function
                hashed_index = hash_ex[i]
                # Update the minimum hash value
                min_hash_value = min(min_hash_value, hashed_index)

        signature.append(min_hash_value)
    return signature

def jaccard_similarity(set_a, set_b):
    intersection_size = len(set_a.intersection(set_b))
    union_size = len(set_a.union(set_b))
    return intersection_size / union_size if union_size != 0 else 0

# Test data
a = set(shingle('The first test', 2))
b = set(shingle('It is the best', 2))

# Create vocabulary
vocab = list(a.union(b))

# One-hot encoding for sets a and b
result_a = one_hot_encoding(vocab, list(a))
result_b = one_hot_encoding(vocab, list(b))

# Create MinHash functions
minhash_func = build_minhash_func(len(vocab), 2)

# Create MinHash signatures
signature_a = create_hash(result_a, minhash_func[0])
signature_b = create_hash(result_b, minhash_func[1])

# Compute Jaccard similarity using MinHash signatures
jaccard_sim = jaccard_similarity(set(signature_a), set(signature_b))

print("Signature A:", signature_a)
print("Signature B:", signature_b)
print("Jaccard Similarity:", jaccard_sim)
