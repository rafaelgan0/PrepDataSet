def revise_review(sentence):
    prompt = f"""<s>[INST]
You are an assistant that helps users revise Paper Reviews.
Paper reviews exist to provide authors of academic research papers constructive critism.

This is a sentence found in a review.
This sentence is a problematic sentence, it contains critism can negatively impact the author.

Sentence: "{sentence}"

Revise this sentence such that it maintains the critism in the original sentence while delivering it in a concise, friendly, and encouraging manner. 
Your revision:[/INST]  """
    return prompt

def label_review(sentence):
    prompt = f"""<s>[INST]
Classify the following review as 'J', 'W', or 'V', where:
'J' is positive or encouraging or constructive or specific or has a positive tone or consists of factual statements and a positive tone.
'V' contains personal attacks and a discouraging tone or excessive negativity without constructive feedback.
'W' meets the standards of professionalism and is not discouraging and is not encouraging or consists of factual statements.

Review: "{sentence}"

Please classify this review as either 'J', 'W', or 'V'. Only output 'J', 'W', or 'V' with no additional explanation. [/INST] Your classification: """
    return prompt