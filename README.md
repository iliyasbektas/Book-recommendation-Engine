# Book recommenation 
Goal of this project: Build a search engine over the "best books ever" list of GoodReads. 

1. Data collection

Since there is no provided dataset, we have to gather it myself. My search engine will run on text documents. 

1.1. Get the list of books

We start from the list of books to include in your corpus of documents. In particular, we focus on the best books ever list. From this list we want to collect the url associated to each book in the list. As you realize, the list is long and splitted in many pages. We ask you to retrieve only the urls of the books listed in the first 300 pages.

The output of this step is a .txt file whose single line corresponds to a book's url.

1.2. Crawl books

Once we get all the urls in the first 300 pages of the list, you:

We then Download the html corresponding to each of the collected urls.
After we collect a single page, immediatly save its html in a file. In this way, if our program stops, for any reason, we will not loose the data collected up to the stopping point. More details in Important (2).
We organize the entire set of downloaded html pages into folders. Each folder will contain the htmls of the books in page 1, page 2, ... of the list of books.


1.3 Parse downloaded pages

At this point, we should have all the html documents about the books of interest and we can start to extract the books informations. The list of information we desire for each book are the following:

Title (to save as bookTitle)

Series (to save as bookSeries)

Author(s), the first box in the picture below (to save as bookAuthors)

Ratings, average stars (to save as ratingValue)

Number of givent ratings (to save as ratingCount)

Number of reviews (to save as reviewCount)

The entire plot (to save as Plot)

Number of pages (to save as NumberofPages)

Published (Publishing Date)

Characters

Setting

Url

2. Search Engine

Now, we want to create two different Search Engines that, given as input a query, return the books that match the query.

First, we must pre-process all the information collected for each book by

Removing stopwords

Removing punctuation

Stemming

For this purpose, we can use the nltk library.

2.1. Conjunctive query

For the first version of the search engine, we narrow our interest on the Plot of each document. It means that we will evaluate queries only with respect to the book's plot.

2.1.1. Creating our index!

Before building the index,

We Create a file named vocabulary, in the format we prefer, that maps each word to an integer (term_id).
Then, the first brick of our project is to create the Inverted Index.

2.1.2. Executing the query

Given a query, that we let the user enter:

survival games
the Search Engine will return a list of documents.

What documents do we want?
Since we are dealing with conjunctive queries (AND), each of the returned documents should contain all the words in the query. 


2.2. Conjunctive query & Ranking score

For the second search engine, given a query, we want to get the top-k (the choice of k it's up to you!) documents related to the query. In particular:

Find all the documents that contains all the words in the query.

Sort them by their similarity with the query

Return in output k documents, or all the documents with non-zero similarity with the query when the results are less than k. You must use a heap data structure (you can use Python libraries) for maintaining the top-k documents.

To solve this task, we will have to use the tfIdf score, and the Cosine similarity. 


2.2.2) Execute the query

In this new setting, given a query we get the right set of documents (i.e., those containing all the words in the query) and sort them according to their similairty to the query. For this purpose, as scoring function we will use the Cosine Similarity with respect to the tfIdf representations of the documents.

Given a query, that you let the user enter:

'survival games'

the search engine is supposed to return a list of documents, ranked by their Cosine Similarity with respect to the query entered in input.

More precisely, the output will contain:

bookTitle

Plot

Url

The similarity score of the documents with respect to the query




