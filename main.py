import os
from dotenv import load_dotenv

from textwrap import dedent
from crewai import Agent, Crew

from tasks import MarketingAnalysisTasks
from agents import MarketingAnalysisAgents

load_dotenv()


def main():
    tasks = MarketingAnalysisTasks()
    agents = MarketingAnalysisAgents()

    print("## Welcome to the marketing Crew")
    print('-------------------------------')
    product_website = input("What is the product website you want a marketing strategy for?\n")
    product_details = input("Any extra details about the product and or the Instagram post you want?\n")

    try:
        # Create Agents
        product_competitor_agent = agents.product_competitor_agent()
        strategy_planner_agent = agents.strategy_planner_agent()
        creative_agent = agents.creative_content_creator_agent()

        # Create Tasks
        website_analysis = tasks.product_analysis(product_competitor_agent, product_website, product_details)
        market_analysis = tasks.competitor_analysis(product_competitor_agent, product_website, product_details)
        campaign_development = tasks.campaign_development(strategy_planner_agent, product_website, product_details)
        write_copy = tasks.instagram_ad_copy(creative_agent)
    except Exception as e:
        print(f"Error creating agents or tasks: {e}")
        return

    try:
        # Create Crew responsible for Copy
        copy_crew = Crew(
            agents=[
                product_competitor_agent,
                strategy_planner_agent,
                creative_agent
            ],
            tasks=[
                website_analysis,
                market_analysis,
                campaign_development,
                write_copy
            ],
            verbose=True
        )

        ad_copy = copy_crew.kickoff()
    except Exception as e:
        print(f"Error during copy crew kickoff: {e}")
        return

    try:
        # Create Crew responsible for Image
        senior_photographer = agents.senior_photographer_agent()
        chief_creative_director = agents.chief_creative_director_agent()
        # Create Tasks for Image
        take_photo = tasks.take_photograph_task(senior_photographer, ad_copy, product_website, product_details)
        approve_photo = tasks.review_photo(chief_creative_director, product_website, product_details)

        image_crew = Crew(
            agents=[
                senior_photographer,
                chief_creative_director
            ],
            tasks=[
                take_photo,
                approve_photo
            ],
            verbose=True
        )

        image = image_crew.kickoff()
    except Exception as e:
        print(f"Error during image crew kickoff: {e}")
        return

    # Print results
    print("\n\n########################")
    print("## Here is the result")
    print("########################\n")
    print("Your post copy:")
    print(ad_copy)
    print("\n\nYour midjourney description:")
    print(image)


if __name__ == "__main__":
    main()
