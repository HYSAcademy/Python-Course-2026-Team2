from openai import OpenAI

client = OpenAI()

async def generate_answer(query: str, context: list[str]):
    prompt = f"""
    Answer the question using the context below:

    Context:
    {context}

    Question:
    {query}
    """

    response = {}

    return response.choices[0].message.content