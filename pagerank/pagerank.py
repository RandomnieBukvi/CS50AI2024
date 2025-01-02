import os
import random
import re
import sys

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

    pd = {cpage: 0 for cpage in corpus}
    outgoing_links = corpus[page]
    if len(outgoing_links) == 0:
        probability = 1 / len(corpus)
        for cpage in corpus:
            pd[cpage] += probability
        return pd

    additional = (1 - damping_factor) / len(corpus)
    probability = damping_factor / len(outgoing_links)
    for pg in outgoing_links:
        pd[pg] = probability
    for cpage in corpus:
        pd[cpage] += additional
    return pd


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = {cpage: 0 for cpage in corpus}
    current_page = random.choice(list(corpus.keys()))
    for i in range(n):
        page_rank[current_page] += 1
        pd = transition_model(corpus, current_page, damping_factor)
        pages = list(pd.keys())
        probabilities = list(pd.values())
        current_page = random.choices(pages, weights=probabilities, k=1)[0]
    for page in page_rank:
        page_rank[page] /= n
    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    for cpage in corpus:
        if len(corpus[cpage]) == 0:
            corpus[cpage] = corpus.keys()
    initial_pr = 1 / len(corpus)
    page_rank = {cpage: initial_pr for cpage in corpus}

    num_links = {cpage: len(corpus[cpage]) for cpage in corpus}
    ingoing_links = {cpage1: {cpage2 for cpage2 in corpus if cpage1 in corpus[cpage2]} for cpage1 in corpus}

    random_pr = (1 - damping_factor) / len(page_rank)
    big_difference = True
    while big_difference:
        max_diff = -1
        for page in page_rank:
            new_pr = random_pr
            for link in ingoing_links[page]:
                new_pr += (page_rank[link] / num_links[link]) * damping_factor
            max_diff = max(abs(new_pr - page_rank[page]), max_diff)
            page_rank[page] = new_pr
        if max_diff < 0.001:
            big_difference = False
    return page_rank


if __name__ == "__main__":
    main()
