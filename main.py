from random import randint, shuffle, seed

# Set a seed for random number generation to ensure reproducibility
seed(42)
from trees.r_tree import *
from trees.kd_tree import *
from trees.quad_tree import *
from trees.range_tree import *
from lsh.lsh import *
threshold = float(input("Εισάγετε ελάχιστο ποσοστό ομοιότητας των πεδίων education(0 - 1): "))
min_letter, max_letter = input("Εισάγετε το εύρος τον ονομάτων στη μορφή X,X: ").upper().split(',')
awards = int(input("Εισάγετε τον ελάχιστο αριθμό βραβείων: "))
min_dblp = int(input("Εισάγετε τον ελάχιστο αριθμό των dblp_records: "))
max_dblp = int(input("Εισάγεται τον μέγιστο αριθμό dblp_records: "))
print("=================================")
user_choice = input("->For r_tree + LSH press 1 \n->For kd_tree + LSH press 2\n->For quad_tree + LSH press 3\n->For range_tree + LSH press 4\n->For testing the performance of each tree with lsh with random inputs press 5\nYour choice: ")
if user_choice == '1':
   # Call the function with data and use word shingles (k=1 for individual words)
    rtree = RTreeIndexer('data/scientists_data_complete.csv')
    query_results=rtree.query(min_letter, max_letter, awards, min_dblp, max_dblp)
    # print(query_results)
    if not query_results:
        print('No results found for these inputs. Try again.')
    else:
        #create an array for the education for LSH
        education_strings = [result["education"].encode('utf-8') for result in query_results]
        education_array_from_r_tree = np.array(education_strings)
        print("R-Tree Data Results = ",len(education_array_from_r_tree))
        info_from_r_tree = [f"Name: {result['lastName']}, Awards: {result['awards']}, DBLP Records: {result['dblp_records']}" for result in query_results]
        lsh_for_multiple_strings(education_array_from_r_tree, info_from_r_tree, threshold, k=1, nbits=20, bands=10)
elif user_choice == '2':

    kd_tree_results = create_and_query_kdtree('data/scientists_data_complete.csv', min_letter, max_letter, awards, min_dblp, max_dblp)
    if not kd_tree_results:
        print('No results found for these inputs. Try again.')
    else:
        lastname = [result["lastName"].encode('utf-8') for result in kd_tree_results]
        awards = [str(result["awards"]).encode('utf-8') for result in kd_tree_results]
        education_strings = [result["education"].encode('utf-8') for result in kd_tree_results]
        dblp_records = [str(result["dblp_records"]).encode('utf-8') for result in kd_tree_results]

        lastname_array_from_kd_tree = np.array(lastname)
        awards_array_from_kd_tree = np.array(awards)
        education_array_from_kd_tree = np.array(education_strings)  #for lsh
        dblp_records_array_from_kd_tree = [str(result["dblp_records"]).encode('utf-8') for result in kd_tree_results]
        print("KD-Tree Data Results = ",len(education_array_from_kd_tree))
        info_from_kd_tree = [f"Name: {result['lastName']}, Awards: {result['awards']}, DBLP Records: {result['dblp_records']}" for result in kd_tree_results]
        lsh_for_multiple_strings(education_array_from_kd_tree, info_from_kd_tree, threshold, k=1, nbits=20, bands=10)
elif user_choice == '3':
    
    quad_tree = build_data_quad_tree()
    quad_tree_results = test_data_quad_tree(quad_tree,min_letter,max_letter,awards,min_dblp,max_dblp)
    if not quad_tree_results:
        print('No results found for these inputs. Try again.')
    else:
        #create an array for the education for LSH
        education_strings = [result["education"].encode('utf-8') for result in quad_tree_results]
        education_array_from_quad_tree = np.array(education_strings)
        print("Quad-Tree Data Results = ",len(education_array_from_quad_tree))
        info_from_quad_tree = [f"Name: {result['lastName']}, Awards: {result['awards']}, DBLP Records: {result['dblp_records']}" for result in quad_tree_results]
        lsh_for_multiple_strings(education_array_from_quad_tree, info_from_quad_tree, threshold, k=1, nbits=20, bands=10)
elif user_choice == '4':
    
    range_tree = build_range_tree()
    results = query_range_tree(range_tree, min_letter, max_letter, awards, min_dblp, max_dblp)
    if not results:
        print('No results found for these inputs. Try again.')
    else:
        education_strings = [result.get("education","").encode('utf-8') for result in results]
        education_array_from_range_tree = np.array(education_strings)
        print("Range-Tree Data Results = ",len(education_array_from_range_tree))
        info_from_range_tree = [f"Name: {result['lastName']}, Awards: {result['awards']}, DBLP Records: {result['dblp_records']}" for result in results]
        lsh_for_multiple_strings(education_array_from_range_tree, info_from_range_tree,threshold, k=1, nbits=20, bands=10)
else:
    print("Invalid choice. Please enter a valid option.")