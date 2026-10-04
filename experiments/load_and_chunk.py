from rag.loader import list_documents, load_document, chunk_document


bucket = "rag-system-docs-10ks"
prefix = "raw/"

keys = list_documents(bucket, prefix)

for key in keys:
    pages = load_document(bucket, key)
    chunks = chunk_document(pages)

    print(f"{key} → {len(pages)} pages, {len(chunks)} chunks")