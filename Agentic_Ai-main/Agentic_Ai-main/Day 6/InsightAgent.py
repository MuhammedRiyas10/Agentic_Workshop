import gradio as gr
import requests
import google.generativeai as genai

# 🔐 API Keys (Ensure these are valid and secure in a production environment)
GEMINI_API_KEY = "AIzaSyDonBzngKXhdxepVLmsjKdZZtD5T6clmiE"
TAVILY_API_KEY = "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"

# Configure Gemini API for analysis
try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    raise Exception(f"Failed to configure Gemini API: {e}")

# Tavily Web Search Function
def search_web(query):
    """
    Fetches web data on clothing stores using Tavily API.
    Args:
        query (str): Search query (e.g., "top clothing stores in Koramangala")
    Returns:
        list: List of search results or error message
    """
    try:
        tavily_url = "https://api.tavily.com/search"
        payload = {
            "api_key": TAVILY_API_KEY,
            "query": query,
            "max_results": 5,
            "include_answer": False,
            "include_raw_content": False
        }
        response = requests.post(tavily_url, json=payload)
        response.raise_for_status()  # Raise an error for bad HTTP status
        return response.json().get("results", [])
    except requests.exceptions.RequestException as e:
        return f"❌ Error fetching Tavily data: {e}"

# Gemini Analysis Function
def analyze_results_with_gemini(location, results):
    """
    Analyzes search results using Gemini to provide insights on competitors, footfall, and strategy.
    Args:
        location (str): Location for analysis (e.g., Koramangala)
        results (list): Web search results from Tavily
    Returns:
        str: Analysis report or error message
    """
    if isinstance(results, str):
        return results  # Return error message if search failed

    # Format search results as context for Gemini
    context = "\n\n".join([
        f"Title: {r['title']}\nContent: {r['content']}\nURL: {r['url']}"
        for r in results
    ])

    # Prompt for Gemini to analyze the market
    prompt = f"""
You are a business analyst specializing in retail. Based on the search results about clothing stores in {location}, provide a detailed analysis:

1. Identify the top 3 competitors and explain their strengths.
2. Estimate daily footfall and peak hours based on available insights.
3. Suggest one actionable strategy for a new clothing business entering this area to improve market position.

Search Results:
{context}
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Gemini Analysis Error: {e}"

# Main Chatbot Function for Gradio
def chatbot_response(messages, chatbot_state):
    """
    Handles user input, searches for data, and generates analysis.
    Args:
        messages: Can be a string (raw user input) or a list of message dictionaries
        chatbot_state: Gradio state (not used here)
    Yields:
        dict: Chatbot responses in {"role": ..., "content": ...} format
    """
    # Handle the case where messages is a string (raw user input)
    if isinstance(messages, str):
        user_message = messages.strip()
        messages = [{"role": "user", "content": user_message}]
    else:
        # Assume messages is a list of dictionaries; get the last user message
        user_message = messages[-1]["content"].strip()

    if not user_message:
        yield {"role": "assistant", "content": "⚠️ Please provide a valid location (e.g., Koramangala)."}
        return

    location = user_message
    search_query = f"top clothing stores in {location}"

    # Step 1: Inform user about search
    yield {"role": "assistant", "content": f"🔍 Searching for clothing stores in {location}..."}

    # Step 2: Perform web search
    results = search_web(search_query)
    if isinstance(results, str):
        yield {"role": "assistant", "content": results}
        return

    if not results:
        yield {"role": "assistant", "content": f"⚠️ No results found for clothing stores in {location}. Try a different location."}
        return

    # Step 3: Analyze results with Gemini
    yield {"role": "assistant", "content": "🧠 Analyzing the data with Gemini..."}
    insights = analyze_results_with_gemini(location, results)

    # Step 4: Deliver final report
    yield {"role": "assistant", "content": f"📊 Insights for {location}:\n\n{insights}"}

# Gradio UI Setup
demo = gr.ChatInterface(
    fn=chatbot_response,
    title="🛍️ Clothing Market Analyzer",
    description="Analyze clothing store competition, footfall, and strategies in high-traffic areas like Koramangala, Bangalore, using real-time web data and AI insights.",
    textbox=gr.Textbox(placeholder="Enter area (e.g., Koramangala, Bangalore)", label="Location"),
    theme="soft",
    type="messages"  # Fixed to "messages"
)

# Launch the app
if __name__ == "__main__":
    demo.launch()