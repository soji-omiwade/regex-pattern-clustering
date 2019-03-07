import re
import sys
"""Scope
    usage: python string_clustering.py regex_list_filename 
        strings_to_match_filename
    
    input: regex_list_filename and strings_to_match_filename
        Each regex line is two parts, separated by the first ':'. To the left 
            is the descriptor, and to the right the corresponding regex
    output: 
        A set of clusters, where each of the input strings is in exactly one of
            the clusters.
        This is implemented by mapping a set of regexes uniquely to the set of
            the strings that each returns a match for all such regexes
"""


def get_descriptor_loc(line):
    match = re.search(':', line)
    return match.start()

def print_clusters(clusters, ds):    
    """Resulting clusters
    
        Complexity to print them: O(len(clusters) * len(regexes))
    """
    for mv, ms in clusters.items():
        mrs = (d for (i,d) in enumerate(ds) if mv[i])
        print(list(mrs), '----->', ms)

def cluster_input(ds, sf):
    """String matching and clustering
    
        Put each string s in a container whose key is the set of all regexes
            that match all strings in that containter 
        Complexity: O(len(strings) * len(regexes) * max(len(s) for all 
            strings)) 
    """
    clusters = dict()
    with open(sf) as f:
        for s in f:
            s = s[:len(s)-1]
            mv = tuple(True if re.search(r, s) else False for r in ds.values())
            if mv not in clusters:
                clusters[mv] = []
            clusters[mv].append(s)
    return clusters

def get_regexes(rf):
    """Gather the regular expressions into a list"""
    ds = dict()
    with open(rf) as f:
        for line in f:
            start = get_descriptor_loc(line)
            descriptor = line[:start] 
            line = line[start+1:len(line)-1] 
            ds[descriptor] = line   
    return ds
    
def main(regexes_file, strings_file):
    ds = get_regexes(regexes_file)
    clusters = cluster_input(ds, strings_file)   
    print_clusters(clusters, ds)
        
if __name__ == '__main__':
    if len(sys.argv) != 3: 
        print('usage: python clustering.py regexes_filename strings_filename')
        sys.exit()
    strings_file = sys.argv[2]
    main(sys.argv[1], sys.argv[2])