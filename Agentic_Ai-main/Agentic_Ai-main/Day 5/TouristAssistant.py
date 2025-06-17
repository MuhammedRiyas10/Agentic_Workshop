import gradio as gr
import requests
from langchain.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import time

# Define API keys directly
GEMINI_API_KEY = "AIzaSyCJ9QHCWrrh-j_d2ofS2h-BUMIGhGQHbVM"  # Replace with your Gemini API key
TAVILY_API_KEY = "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"  # Replace with your Tavily API key
WEATHER_API_KEY = "67f1db5a0d764fd8a2895815251306"  # Replace with your WeatherAPI.com API key

# Initialize Gemini 2.0 Flash model with the API key directly
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7,
    google_api_key=GEMINI_API_KEY
)

# Custom Weather Tool with Retry
@tool
def get_weather_forecast(city: str) -> str:
    """Fetches the current weather forecast for a given city using WeatherAPI.com."""
    city = city.strip().title()
    url = f"https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&aqi=no"
    retries = 3
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            weather = data["current"]
            return (
                f"Weather in {city}:\n"
                f"Temperature: {weather['temp_c']}°C\n"
                f"Condition: {weather['condition']['text']}\n"
                f"Humidity: {weather['humidity']}%\n"
                f"Wind: {weather['wind_kph']} kph"
            )
        except requests.exceptions.RequestException as e:
            error_message = f"Error fetching weather for {city}: {str(e)}"
            print(f"Attempt {attempt + 1}/{retries} - {error_message}")
            if attempt < retries - 1:
                time.sleep(2)  # Wait before retrying
                continue
            return error_message

# Custom Tavily Search Tool
@tool
def search_attractions(city: str) -> str:
    """Searches for top tourist attractions in a given city using Tavily API."""
    city = city.strip().title()
    url = "https://api.tavily.com/search"
    headers = {"Content-Type": "application/json"}
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": f"top tourist attractions in {city}",
        "search_depth": "basic",
        "max_results": 5
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=5)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])
        if not results:
            return f"No attractions found for {city}."
        attractions = "\n".join(
            f"- {result['title']}: {result['content'][:100]}..." for result in results[:3]
        )
        return f"Top attractions in {city}:\n{attractions}"
    except requests.exceptions.RequestException as e:
        error_message = f"Error searching attractions for {city}: {str(e)}"
        print(error_message)
        return error_message

# Define tools
tools = [get_weather_forecast, search_attractions]

# Create prompt template with agent_scratchpad
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful travel assistant. Use the provided tools to fetch weather forecasts and find top attractions for the user's destination. Summarize results clearly and concisely. If one tool fails, still provide results from the other tool if available, and include the specific error message for the failed tool."),
    ("human", "Please provide the weather forecast and top attractions for {destination}."),
    ("placeholder", "{agent_scratchpad}")
])

# Create tool-calling agent
agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Gradio interface function
def travel_assistant(destination):
    if not destination.strip():
        return "Please enter a valid destination city."
    try:
        result = agent_executor.invoke({"destination": destination})
        output = result.get("output", "No results found.")
        return output.strip()
    except Exception as e:
        return f"Error processing request: {str(e)}"

# Create Gradio interface
interface = gr.Interface(
    fn=travel_assistant,
    inputs=gr.Textbox(label="Enter Destination City", placeholder="e.g., Paris"),
    outputs=gr.Textbox(label="Travel Information"),
    title="Intelligent Travel Assistant",
    description="Enter a city to get the weather forecast and top attractions."
)

if __name__ == "__main__":
    interface.launch()