import os
from crewai import Agent
from crewai_tools import ScrapeWebsiteTool
from langchain.tools import tool
from langchain_groq import ChatGroq


class BrowserTools:

    @tool("Scrape website content")
    def scrape_and_summarize_website(website):
        """
        Scrape and summarize a website's content using ScrapeWebsiteTool.

        Args:
            website (str): The full URL of the website to scrape.

        Returns:
            str: A summary of the website's content or an error message.
        """
        try:
            # Initialize ScrapeWebsiteTool with the specified website URL
            scrape_tool = ScrapeWebsiteTool(website_url=website)

            # Extract text from the website
            text_content = scrape_tool.run()

        except Exception as e:
            return f"Error scraping website: {e}"

        # Split content into chunks for processing
        content_chunks = [text_content[i:i + 8000] for i in range(0, len(text_content), 8000)]
        summaries = []

        # Create a single agent responsible for summarizing
        agent = Agent(
            role='Principal Researcher',
            goal='Do amazing research and summaries based on the content you are working with',
            backstory="You're a Principal Researcher at a big company and you need to do research about a given topic.",
            llm=ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="mixtral-8x7b-32768"),
            allow_delegation=False
        )

        # Iterate through content chunks and summarize each
        for chunk in content_chunks:
            task_description = f'Analyze and make a LONG summary of the content below. Make sure to include ALL relevant information in the summary, return only the summary, nothing else.\n\nCONTENT\n----------\n{chunk}'

            # Use the LLM to summarize the content with the updated method call
            try:
                # Use invoke to get response from the LLM and ensure it's converted to a string
                response = agent.llm.invoke(task_description)

                # If response is an AIMessage or similar, convert to string
                if hasattr(response, 'content'):
                    summary = response.content
                else:
                    summary = str(response)

                summaries.append(summary)
            except Exception as e:
                return f"Error during summarization: {e}"

        # Combine all summaries into one string
        final_summary = "\n\n".join(summaries)
        print(f"sumaryy of data {final_summary}")

        return final_summary
