from random import randint, shuffle, seed
import timeit
import matplotlib.pyplot as plt
import random
import string
# Set a seed for random number generation to ensure reproducibility
seed(42)
from trees.r_tree import *
from trees.kd_tree import *
from trees.quad_tree import *
from trees.range_tree import *
from lsh.lsh import *
user_choice = input("Welcome to our program!\n=============================\n->To insert your values and view results for a tree of your choice combined with the lsh method press 1\n->To compare the methods with random inputs press 2\nYour choice: ")
if user_choice=='1':
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
            lsh_for_multiple_strings(education_array_from_r_tree, info_from_r_tree, threshold,1, k=1, nbits=20, bands=10)
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
            lsh_for_multiple_strings(education_array_from_kd_tree, info_from_kd_tree, threshold,1, k=1, nbits=20, bands=10)
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
            lsh_for_multiple_strings(education_array_from_quad_tree, info_from_quad_tree, threshold,1, k=1, nbits=20, bands=10)
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
            lsh_for_multiple_strings(education_array_from_range_tree, info_from_range_tree,threshold,1, k=1, nbits=20, bands=10)

    else:
        print("Invalid choice. Please enter a valid option.")
elif user_choice=='2':
    def r_tree(min_letter, max_letter,awards,min_dblp,max_dblp,threshold):
        rtree = RTreeIndexer('data/scientists_data_complete.csv')
        query_results=rtree.query(min_letter, max_letter, awards, min_dblp, max_dblp)
        if not query_results:
            pass
        else:
            #create an array for the education for LSH
            education_strings = [result["education"].encode('utf-8') for result in query_results]
            education_array_from_r_tree = np.array(education_strings)
            info_from_r_tree = [f"Name: {result['lastName']}, Awards: {result['awards']}, DBLP Records: {result['dblp_records']}" for result in query_results]
            lsh_for_multiple_strings(education_array_from_r_tree, info_from_r_tree, threshold,0, k=1, nbits=20, bands=10)
            pass

    def kd_tree(min_letter, max_letter,awards,min_dblp,max_dblp,threshold):
        kd_tree_results = create_and_query_kdtree('data/scientists_data_complete.csv', min_letter, max_letter, awards, min_dblp, max_dblp)
        if not kd_tree_results:
            pass
        else:
            lastname = [result["lastName"].encode('utf-8') for result in kd_tree_results]
            awards = [str(result["awards"]).encode('utf-8') for result in kd_tree_results]
            education_strings = [result["education"].encode('utf-8') for result in kd_tree_results]
            dblp_records = [str(result["dblp_records"]).encode('utf-8') for result in kd_tree_results]

            lastname_array_from_kd_tree = np.array(lastname)
            awards_array_from_kd_tree = np.array(awards)
            education_array_from_kd_tree = np.array(education_strings)  #for lsh
            dblp_records_array_from_kd_tree = [str(result["dblp_records"]).encode('utf-8') for result in kd_tree_results]
            info_from_kd_tree = [f"Name: {result['lastName']}, Awards: {result['awards']}, DBLP Records: {result['dblp_records']}" for result in kd_tree_results]
            lsh_for_multiple_strings(education_array_from_kd_tree, info_from_kd_tree, threshold,0, k=1, nbits=20, bands=10)
            pass

    def quadtree(min_letter, max_letter,awards,min_dblp,max_dblp,threshold):
        quad_tree = build_data_quad_tree()
        quad_tree_results = test_data_quad_tree(quad_tree,min_letter,max_letter,awards,min_dblp,max_dblp)
        if not quad_tree_results:
            pass
        else:
            #create an array for the education for LSH
            education_strings = [result["education"].encode('utf-8') for result in quad_tree_results]
            education_array_from_quad_tree = np.array(education_strings)
            info_from_quad_tree = [f"Name: {result['lastName']}, Awards: {result['awards']}, DBLP Records: {result['dblp_records']}" for result in quad_tree_results]
            lsh_for_multiple_strings(education_array_from_quad_tree, info_from_quad_tree, threshold,0, k=1, nbits=20, bands=10)
            pass
    
    def rangetree(min_letter, max_letter,awards,min_dblp,max_dblp,threshold):
        range_tree = build_range_tree()
        results = query_range_tree(range_tree, min_letter, max_letter, awards, min_dblp, max_dblp)
        
        if not results:
            pass
        else:
            education_strings = [result.get("education","").encode('utf-8') for result in results]
            education_array_from_range_tree = np.array(education_strings)
            info_from_range_tree = [f"Name: {result['lastName']}, Awards: {result['awards']}, DBLP Records: {result['dblp_records']}" for result in results]
            lsh_for_multiple_strings(education_array_from_range_tree, info_from_range_tree,threshold,0, k=1, nbits=20, bands=10)
            pass


    num_runs=10
    times_method1 = []
    times_method2 = []
    times_method3 = []
    times_method4 = []

    # Run each method 5 times
    for _ in range(num_runs):
        min_letter = random.choice(string.ascii_uppercase)

        # Generate a random capital letter greater than or equal to min_letter for max_letter
        max_letter = random.choice(string.ascii_uppercase[string.ascii_uppercase.index(min_letter):])
        awards = random.randint(0, 6)
        threshold = round(random.uniform(0.4, 0.8),2)
        min_dblp = random.randint(0,199)
        max_dblp = random.randint(min_dblp, 200)
        print(min_letter)
        print(max_letter)
        print(awards)
        print(threshold)
        print(min_dblp)
        print(max_dblp)
        time_method1 = timeit.timeit(lambda: r_tree(min_letter, max_letter, awards, min_dblp, max_dblp, threshold), number=10)
        times_method1.append(time_method1)

        time_method2 = timeit.timeit(lambda: kd_tree(min_letter, max_letter, awards, min_dblp, max_dblp, threshold), number=10)
        times_method2.append(time_method2)

        time_method3 = timeit.timeit(lambda: quadtree(min_letter, max_letter, awards, min_dblp, max_dblp, threshold), number=10)
        times_method3.append(time_method3)

        time_method4 = timeit.timeit(lambda: rangetree(min_letter, max_letter, awards, min_dblp, max_dblp, threshold), number=10)
        times_method4.append(time_method4)

    # Calculate average times for each method
    avg_time_method1 = sum(times_method1) / num_runs
    avg_time_method2 = sum(times_method2) / num_runs
    avg_time_method3 = sum(times_method3) / num_runs
    avg_time_method4 = sum(times_method4) / num_runs

    # Create a bar plot to compare average execution times
    methods = ['R-Tree + LSH', 'KD-Tree + LSH', 'Quad-Tree + LSH', 'Range-Tree + LSH']
    avg_execution_times = [avg_time_method1, avg_time_method2, avg_time_method3, avg_time_method4]

    plt.bar(methods, avg_execution_times, color=['blue', 'green', 'orange', 'red'])
    plt.xlabel('Methods')
    plt.ylabel('Average Execution Time (seconds)')
    plt.title('Average Performance Comparison of Methods')
    plt.show()

else:
    print("Invalid choice. Please enter a valid option.")