"""
Alternative search tools for CrewAI when Serper is not working
"""

from crewai import Agent, Task, Crew, LLM
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create LLM
llm = LLM(model="gemini/gemini-2.0-flash", temperature=0.2)

# Option 1: Use DuckDuckGo Search (no API key required)
try:
    from crewai_tools import DuckDuckGoSearchRun
    search_tool = DuckDuckGoSearchRun()
    print("✅ Using DuckDuckGo Search (no API key required)")
except ImportError:
    print("❌ DuckDuckGo tool not available")
    search_tool = None

# Option 2: Use Wikipedia Search (no API key required)
try:
    from crewai_tools import WikipediaSearchTool
    wiki_tool = WikipediaSearchTool()
    print("✅ Wikipedia Search available")
except ImportError:
    print("❌ Wikipedia tool not available")
    wiki_tool = None

# Option 3: Create a simple web scraper tool
from crewai_tools import ScrapeWebsiteTool
scrape_tool = ScrapeWebsiteTool()

# Define agents with alternative tools
researcher_agent = Agent(
    role='Research Specialist',
    goal='Research interesting facts about the topic: {topic}',
    backstory="You are an expert at finding relevant and factual data.",
    tools=[search_tool] if search_tool else [wiki_tool, scrape_tool],
    verbose=True,
    llm=llm
)

writer_agent = Agent(
    role="Creative Writer",
    goal="Write a short blog summary using the research",
    backstory="You are skilled at writing engaging summaries based on provided content.",
    llm=llm,
    verbose=True,
)

# Create tasks
task1 = Task(
    description="Find 3-5 interesting and recent facts about {topic} as of year 2025.",
    expected_output="A bullet list of 3-5 facts",
    agent=researcher_agent,
)

task2 = Task(
    description="Write a 100-word blog post summary about {topic} using the facts from the research.",
    expected_output="A blog post summary",
    agent=writer_agent,
    context=[task1],
)

# Create and run crew
crew = Crew(
    agents=[researcher_agent, writer_agent],
    tasks=[task1, task2],
    verbose=True,
)

if __name__ == "__main__":
    print("Running crew with alternative search tools...")
    result = crew.kickoff(inputs={"topic": "The future of electrical vehicles"})
    print("\n=== Final Result ===")
    print(result)
