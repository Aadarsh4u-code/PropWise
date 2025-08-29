from langchain.prompts import PromptTemplate

base_template = "Answer the question based on the following summaries:\n{context}\nQuestion: {question}\nAnswer:"
updated_template = "You are a helpful assistant for RealEstate research.\n" + base_template

PROMPT = PromptTemplate(
    template=updated_template,
    input_variables=["context", "question"]
)
EXAMPLE_PROMPT = PromptTemplate(
    template="Content: {page_content}\nSource: {source}",
    input_variables=["page_content", "source"],
)