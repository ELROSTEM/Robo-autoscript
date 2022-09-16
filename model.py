from transformers import pipeline

generator = pipeline("text-generation", model="distilgpt2")
output = generator(
    "Once Upon a time, there was a little boy who had a dream. A dream many did not believe was possible. Yet, he tried",
    max_length=100,
)

print(output)