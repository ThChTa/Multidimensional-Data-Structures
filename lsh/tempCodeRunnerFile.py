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

    for i in range(len(strings)):
        for j in range(i + 1, len(strings)):
            jaccard_sim = jaccard_similarity(set(signatures[i]), set(signatures[j]))
            if jaccard_sim >= 0.4:   #example of Threshold
                print(f"Jaccard Similarity between {i+1} and {j+1}\n")
                print(f"Education {i+1}:\n\n{strings[i]}\nEducation {j+1}:\n\n{strings[j]}\n\n")
                print("=============================================================================\n")