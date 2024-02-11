import openai


def get_answer(context, query,api_key): #function for the LLM response
    openai.api_key= api_key
    completion = openai.chat.completions.create(model="gpt-3.5-turbo",
            messages=[ #context we are passing the LLM
            {"role": "user", "content": "you only have this context for information: " + context + "concisely answer this question ONLY!!!! using the info from the following context if the question cannot be answered with the info return a 'cannot be found': " + query}
        ])
    
    answer= (completion.choices[0].message.content) #extracting the text from the LLM response

    return answer






