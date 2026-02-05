import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hello, world! This is a test of the tokenization process."

tokens = enc.encode(text)
print("Tokens:", tokens)

decoded_text = enc.decode(tokens)
print("Decoded text:", decoded_text)