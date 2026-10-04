
import math


def cosine_similarity(a, b):
    dot_product = sum(x * y for x, y in zip(a, b))

    magnitude_a = math.sqrt(sum(x * x for x in a))
    magnitude_b = math.sqrt(sum(y * y for y in b))

    return dot_product / (magnitude_a * magnitude_b)


a = embed("The cat sat on the mat.")
b = embed("A kitten is resting on a rug.")
c = embed("Quarterly revenue grew 12%.")

print("A-B:", cosine_similarity(a, b))
print("A-C:", cosine_similarity(a, c))
print("B-C:", cosine_similarity(b, c))

long_text = """
Artificial intelligence is transforming the way people interact with
computers and software. Modern machine learning systems can process
large amounts of information, recognize patterns, generate text, and
help people solve complex problems. These systems are increasingly
being used in areas such as education, software development, scientific
research, customer service, and business analytics. As these
technologies continue to develop, understanding how they work and how
to use them responsibly is becoming increasingly important.
"""

long_embedding = embed(long_text)

print("Long paragraph embedding length:", len(long_embedding))