import rtree_build
import rtree_draw
import sys
import csv
import dtree_build

def main(col_names=None):
    # parse command-line arguments to read the name of the input csv file
    # and optional 'draw tree' parameter
    if len(sys.argv) < 2:  # input file name should be specified
        print("Please specify input csv file name")
        return

    csv_file_name = sys.argv[1]

    data = []
    with open(csv_file_name) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            information = []
            for attribute in row:
                try:
                    information += [float(attribute)]
                except ValueError:
                    information += [attribute]
            data.append(information)

    print("Total number of records = ", len(data))
    tree = rtree_build.buildtree(data, min_gain =0.001, min_samples = 5)

    rtree_build.printtree(tree, '', col_names)

    max_tree_depth = dtree_build.max_depth(tree)
    print("max number of questions=" + str(max_tree_depth))
    if len(sys.argv) > 2: # draw option specified
        import dtree_draw
        rtree_draw.drawtree(tree, jpeg=csv_file_name+'.jpg')

    if len(sys.argv) > 3:  # create json file for d3.js visualization
        import json
        import dtree_to_json
        json_tree = dtree_to_json.dtree_to_jsontree(tree, col_names)
        print(json_tree)

        # create json data for d3.js interactive visualization
        with open(csv_file_name + ".json", "w") as write_file:
            json.dump(json_tree, write_file)
    print("course ['teaching', 'minority', 'female', 'english', 30, 15, 'lower', 4, 3] is: ", rtree_build.classify(['teaching', 'not minority', 'female', 'english', 30, 15, 'lower', 4, 3], tree))
    print("course ['teaching', 'not minority', 'male', 'english', 40, 20, 'lower', 6, 4] is: ", rtree_build.classify(['teaching', 'not minority', 'male', 'english', 40, 20, 'lower', 6, 4], tree))
    print("course ['teaching', 'not minority', 'male', 'english', 50, 15, 'lower', 5, 4] is: ", rtree_build.classify(['teaching', 'not minority', 'male', 'english', 50, 15, 'lower', 5, 4], tree))

if __name__ == "__main__":
    col_names = ['rank',
                 'ethnicity',
                 'gender',
                 'language',
                 'age',
                 'class_size',
                 'cls_level',
                 'bty_avg',
                 'prof_eval']
    main(col_names)





