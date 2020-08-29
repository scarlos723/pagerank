import os
import random
import re
import sys
import copy


DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    distribution={}

    if corpus[page]:
        for aux_page in corpus:
            distribution[aux_page]=(1-damping_factor)/len(corpus)
        for link in corpus[page]:
            distribution[link]=damping_factor/len(corpus[page])
    else:
        for aux_page in corpus:
            distribution[aux_page]=1/len(corpus)
    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank={}
    for page in corpus:
        pagerank[page] = 0

    sample=random.choices(list(corpus.keys()), k=1)[0]
    pagerank[sample]+=1/n
    
    for i in range(1, n):
        trans_model = transition_model(corpus, sample, damping_factor)
        pages = tuple(trans_model.keys())
        prob = tuple(trans_model.values())
        sample = random.choices(pages, weights=prob, k=1)[0]
        pagerank[sample]+=1/n

    return pagerank        
                


    print("sample page rank")


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    pagerank={}

    for page in corpus:
        pagerank[page] = 1 / len(corpus)

    new_pagerank={}

    loop=True
    while loop:
        for page in pagerank:
            new_pagerank[page]=((1-damping_factor)/len(corpus))+damping_factor*sumatory(pagerank,corpus,page)
        for page in pagerank: 
            if abs(new_pagerank[page] - pagerank[page]) < 0.001:
                loop=False
            pagerank[page]=new_pagerank[page]     
    return pagerank
    
def sumatory(pagerank,corpus,page):
    suma=0
    for aux_page in corpus:
        if page in corpus[aux_page]:
            suma+=pagerank[aux_page] / len(corpus[aux_page])
        if not corpus[aux_page]:
            suma += pagerank[aux_page] / len(corpus)
    return suma

if __name__ == "__main__":
    main()
