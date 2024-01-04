import pandas as pd
from scipy.spatial import KDTree

def letter_to_number(letter):
    return ord(letter.upper()) - 65

def load_csv(file_path):
    df = pd.read_csv(file_path)
    return df

# Δημιουργία του KD-tree
def create_kd_tree(data_frame):
    kd_data = data_frame.copy()
    kd_data['lastName'] = kd_data['lastName'].apply(lambda x: letter_to_number(x[0]))
    kd_tree = KDTree(kd_data[['lastName', 'awards', 'dblp_records']])
    return kd_tree, data_frame  # Χρησιμοποιούμε το αρχικό DataFrame για τα αποτελέσματα


def query_kd_tree(kd_tree, full_data, surname_range, awards_min, dblp_record_range):
    surname_min = letter_to_number(surname_range[0])
    surname_max = letter_to_number(surname_range[1])
    results = []

    # Εύρος αναζήτησης για το KD-tree
    search_min = [surname_min, awards_min, dblp_record_range[0]]
    search_max = [surname_max, float('inf'), dblp_record_range[1]]

    # Αναζητούμε όλα τα σημεία μέσα στο εύρος
    indices = kd_tree.query_ball_point(search_min, float('inf'))
    indices = [i for i in indices if all(search_min[j] <= kd_tree.data[i][j] <= search_max[j] for j in range(3))]

    for index in indices:
        row = full_data.iloc[index]
        
        results.append({
                'lastName': row['lastName'],
                'awards': row['awards'],
                #'education': row['education'],
                'dblp_records': row['dblp_records']
        })

    return results

# df = load_csv('./data/scientists_data_complete.csv')
# kd_tree, full_data = create_kd_tree(df)
# results = query_kd_tree(kd_tree, full_data, ('A', 'C'), 5, (10,50))
# print(results)