from random import randint, shuffle, seed

# Set a seed for random number generation to ensure reproducibility
seed(42)
import sys
sys.path.insert(0, './trees')
from r_tree import education_array_from_r_tree
from kd_tree import education_array_from_kd_tree
from quad_tree import education_array_from_quad_tree
from range_tree import education_array_from_range_tree



# Modified shingle function to tokenize text into words
def shingle(text: str, k: int):
    words = text.decode('utf-8').split()  # Decode to UTF-8 and tokenize text into words
    shingle_set = []
    for i in range(len(words) - k + 1):
        shingle_set.append(" ".join(words[i:i+k]))  # Combine k consecutive words into a shingle
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
    # Create the signatures (matching)
    signature = []
    for func in minhash_func:
        for i in range(len(vector)):
            if vector[i] == 1 and i + 1 == func:
                signature.append(i)
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

# Function to perform LSH for multiple strings
def lsh_for_multiple_strings(strings, k, nbits, bands):
    # Create shingles and vocabulary
    shingles = [shingle(s, k) for s in strings]
    vocab = set().union(*shingles)

    # One-hot encoding for each string
    one_hots = [one_hot_encoding(vocab, list(s)) for s in shingles]

    # Create MinHash functions
    minhash_func = build_minhash_func(len(vocab), nbits, num_hashes=len(strings))

    # Create MinHash signatures for each string
    signatures = [create_hash(one_hot, minhash_func[i]) for i, one_hot in enumerate(one_hots)]

    for i in range(len(strings)):
        for j in range(i + 1, len(strings)):
            jaccard_sim = jaccard_similarity(set(signatures[i]), set(signatures[j]))
            if jaccard_sim >= 0.02:   # Example of Threshold
                print(f"Jaccard Similarity between {i+1} and {j+1}\n")
                print(f"Education {i+1}:\n\n{strings[i]}\nEducation {j+1}:\n\n{strings[j]}\n\n")
                print("=============================================================================\n")
       
            
user_choice = input("This is our LSH function!, For r_tree + LSH press 1, For kd_tree + LSH press 2, For quad_tree + LSH press 3, For range_tree + LSH press 4")
if user_choice == '1':
    # Call the function with data and use word shingles (k=1 for individual words)
    lsh_for_multiple_strings(education_array_from_r_tree, k=1, nbits=20, bands=10)

elif user_choice == '2':
    # Add code or function call for kd_tree + LSH
    lsh_for_multiple_strings(education_array_from_kd_tree, k=1, nbits=20, bands=10)
elif user_choice == '3':
    # Add code or function call for quad_tree + LSH
    lsh_for_multiple_strings(education_array_from_quad_tree, k=1, nbits=20, bands=10)
elif user_choice == '4':
    # Add code or function call for range_tree + LSH
    lsh_for_multiple_strings(education_array_from_range_tree, k=1, nbits=20, bands=10)
else:
    print("Invalid choice. Please enter a valid option.")


