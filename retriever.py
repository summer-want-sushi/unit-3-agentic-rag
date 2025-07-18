from smolagents import Tool
from langchain_community.retrievers import BM25Retriever
from langchain.docstore.document import Document
from datasets import load_from_disk


class GuestInfoRetrieverTool(Tool):
    name = "guest_info_retriever"
    description = "Retrieves detailed information about gala guests based on their name or relation."
    inputs = {
        "query": {
            "type": "string",
            "description": "The name or relation of the guest you want information about."
        }
    }
    output_type = "string"

    def __init__(self, docs):
        self.is_initialized = False
        self.retriever = BM25Retriever.from_documents(docs)
       

    def forward(self, query: str):
        results = self.retriever.get_relevant_documents(query)
        if results:
            return "\n\n".join([doc.page_content for doc in results[:3]])
        else:
            return "No matching guest information found."


def load_guest_dataset():
   # Load the locally saved dataset
    guest_dataset = load_from_disk("local_guest_dataset")

    # Convert dataset entries into Document objects
    docs = [
        Document(
            page_content="\n".join([
                f"Name: {guest['name']}",
                f"Relation: {guest['relation']}",
                f"Description: {guest['description']}",
                f"Email: {guest['email']}"
            ]),
            metadata={"name": guest["name"]}
        )
        for guest in guest_dataset
    ]

    # Return the tool
    return GuestInfoRetrieverTool(docs)


if __name__ == "__main__":
    from datasets import load_dataset
    dataset = load_dataset("agents-course/unit3-invitees", split="train")
    dataset.save_to_disk("local_guest_dataset")



