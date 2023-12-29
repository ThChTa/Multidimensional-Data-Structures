from random import shuffle

# shingle function
def shingle(text: str, k: int):
    shingle_list = []
    for i in range(len(text) - k + 1):
        shingle_list.append(text[i:i+k])
    return shingle_list

# test shingle
a = set(shingle('The first test', 2))
b = set(shingle('It is the best', 2))
print(a)  # print the set of a
print(b)  # print the set of b

# create vocab 
vocab = list(a.union(b))

# one hot encoding
def one_hot_encoding(vocab, data):
    one_hot = [1 if x in data else 0 for x in vocab]
    return one_hot

# test one_hot_encoding
result = one_hot_encoding(vocab, list(a))
print(result)


# MinHash

def create_hash_func(size: int):
    hash_ex = list(range(1, len(vocab) + 1))
    print("hash = ", hash_ex)
    shuffle(hash_ex)  # shuffle list
    print("Shuffle = ", hash_ex)
    return hash_ex

def build_minhash_func(vocab_size: int, nbits: int):
    # with this function, you can build multiple minhash vectors
    hashes = []
    for _ in range(nbits):
        hashes.append(create_hash_func(vocab_size))
    return hashes

# here I create 2 minhash vectors
minhash_func = build_minhash_func(len(vocab), 2)

def create_hash(vector: list, hash_ex: list):
    # here I create the signatures (matching)
    signature = []
    for func in minhash_func:
        for i in range(1, len(vocab) + 1):
            id = hash_ex.index(i)
            signature_value = vector[id]
            print(f"{i} -> {id} -> {signature_value}")
            if signature_value == 1:
                print('we have a match!')
                break  # if I find the 1st (1), then break and print 'we have a match!'
    return signature

# create signatures
sign = create_hash(result, create_hash_func(len(vocab)))

print(sign)
