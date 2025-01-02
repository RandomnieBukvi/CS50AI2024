from pagerank import *

corpus = crawl('corpus0')
print(corpus)
ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
print(f"PageRank Results from Sampling (n = {SAMPLES})")
count = 0
for page in sorted(ranks):
    print(f"  {page}: {ranks[page]:.4f}")
    count += ranks[page]
print(count)
count = 0
ranks = iterate_pagerank(corpus, DAMPING)
print(f"PageRank Results from Iteration")
for page in sorted(ranks):
    print(f"  {page}: {ranks[page]:.4f}")
    count += ranks[page]
print(count)