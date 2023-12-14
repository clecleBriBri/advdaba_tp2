import ijson
from neo4j import GraphDatabase
import time
import multiprocessing
import gc
import random
import sys
uri = "bolt://localhost:7687"
username = "neo4j"
password = "testtest"


def add_articles(batch):
    driver = GraphDatabase.driver(uri, auth=(username, password))
    with driver.session() as session:
        for _ in range(3):
            try:
                session.write_transaction(add_articles_tx, batch)
                break
            except Exception as e:
                print(f"Transaction failed: {e}")
                time.sleep(random.uniform(0.5, 2))
    driver.close()


def add_articles_tx(tx, articles):
    query = """
    UNWIND $jsonBatch AS jsonObj
    MERGE (article:ARTICLE {_id: jsonObj._id})
    ON CREATE SET article.title = jsonObj.title
    ON MATCH SET article.title = jsonObj.title
    WITH article, jsonObj.authors AS authors, jsonObj.references AS references
    WHERE authors IS NOT NULL AND size(authors) > 0
    UNWIND authors AS author
    WITH article, author, references
    WHERE author._id IS NOT NULL
    MERGE (a:AUTHOR {_id: author._id})
    ON CREATE SET a.name = author.name
    MERGE (a)-[:AUTHORED]->(article)
    WITH article, references
    WHERE references IS NOT NULL AND size(references) > 0
    UNWIND references AS ref
    MERGE (cited_article:ARTICLE {_id: ref})
    ON CREATE SET cited_article.title = ''
    MERGE (article)-[:CITES]->(cited_article)
    """
    tx.run(query, jsonBatch=articles)


def process_batch(batch):
    add_articles(batch)


def process_stdin():
    batch_size = 1000
    number_of_articles = 0
    start_time = time.time()
    parser = ijson.items(sys.stdin, "item")

    batch = []
    for article in parser:
        batch.append(article)
        if len(batch) >= batch_size:
            process_batch(batch)
            number_of_articles += len(batch)
            print(f"Processing batch of {len(batch)} articles")
            print(f"Total articles processed: {number_of_articles}")
            print(f"Elapsed Time: {time.time() - start_time} seconds")
            batch = []

    if batch:
        process_batch(batch)
        number_of_articles += len(batch)

    print(f"Total articles processed: {number_of_articles}")


if __name__ == "__main__":
    process_stdin()
