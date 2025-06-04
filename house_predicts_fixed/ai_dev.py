def answer_question(question):
    # Basic mock logic for testing
    if "revenue" in question.lower():
        return "Total revenue is $3,000 this month."
    elif "top" in question.lower() and "products" in question.lower():
        return "The top selling products are Product A, B, and C."
    else: 
        return "Sorry. I don't understand the question yet."
    