# shingle function
def shingle(text: str, k: int):
    shingle_list = []
    for i in range(len(text) - k + 1):
        shingle_list.append(text[i:i+k])
    return shingle_list

# test shingle
a = set(shingle('The first test', 2))
b = set(shingle('It is the best', 2))
print(a)  #print the set of a
print(b)  #print the set of b

# create vocab 
vocab = list(a.union(b))

# one hot encoding
def one_hot_encoding(vocab, data):
    one_hot = [1 if x in data else 0 for x in vocab]
    return one_hot

# test one_hot_encoding

result = one_hot_encoding(vocab, list(a))
print(result)
