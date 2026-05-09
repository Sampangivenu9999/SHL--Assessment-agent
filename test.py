from utils.retriever import search_assessments

results = search_assessments("Java developer")

for item in results:
    print(item)