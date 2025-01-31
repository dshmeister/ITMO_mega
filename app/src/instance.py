def get_llm():
    return llm

def set_llm(llm_instance):
    global llm
    llm = llm_instance

def get_search():
    return search

def set_search(search_instance):
    global search
    search = search_instance