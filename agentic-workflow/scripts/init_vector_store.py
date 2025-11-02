#!/usr/bin/env python3
"""Initialize or rebuild the vector store for document search."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from typhoon_it_support.tools.document_search import rebuild_vector_store


def main():
    """Main function to rebuild vector store."""
    print("Rebuilding vector store...")
    print("This will:")
    print("1. Load all documents from /documents directory")
    print("2. Split them into chunks")
    print("3. Generate embeddings")
    print("4. Create FAISS index")
    print()

    result = rebuild_vector_store()
    print(result)
    print()
    print("Vector store is ready for use!")


if __name__ == "__main__":
    main()
