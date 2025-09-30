import argparse
import os
from dotenv import load_dotenv
import openai

# It's good practice to structure imports, especially in a larger project.
from src.core import nl2cmd, executor, memory, safety
from src.core.mock_planner import create_mock_plan
from src.ui import persona, colors

def has_api_config():
    """Checks if the required API environment variables are set."""
    return all([
        os.environ.get("CODER_BASE_URL"),
        os.environ.get("CODER_MODEL_NAME"),
        os.environ.get("OPENAI_API_KEY")
    ])

def main():
    """
    Main entry point for the Samantha CLI.
    Orchestrates the conversion of a natural language prompt into an executable plan.
    """
    # Load environment variables from .env file for local development
    load_dotenv()

    # Setup argument parser
    parser = argparse.ArgumentParser(
        description=f"{colors.CYAN}Samantha - An AI terminal assistant for openEuler.{colors.RESET}",
        epilog="Example: python -m src.cli.samantha \"copy all pdfs from downloads to documents\""
    )
    parser.add_argument("prompt", nargs="+", help="The natural language command you want Samantha to execute.")
    parser.add_argument("--mock", action="store_true", help="Run in mock mode without calling the AI model.")
    args = parser.parse_args()

    # Combine arguments into a single user prompt
    user_intent = " ".join(args.prompt)
    print(persona.greet(user_intent))

    # Initialize memory
    memory_instance = memory.Memory()

    try:
        plan = None
        # 1. Convert natural language to a structured plan
        if args.mock or not has_api_config():
            if not has_api_config() and not args.mock:
                print(persona.inform("AI model configuration not found. Falling back to mock mode."))
            else:
                print(persona.inform("Running in mock mode."))
            plan = create_mock_plan(user_intent)
        else:
            # This calls the OpenAI-compatible model to get a JSON plan.
            plan = nl2cmd.nl_to_plan(user_intent)

        if not plan or not plan.get("steps"):
            print(persona.inform_error("I couldn't create a plan for that request."))
            return

        # 2. (Future) Sanitize and validate the plan for safety
        # plan = safety.sanitize_plan(plan)

        # 3. Execute the plan
        # The executor will preview, ask for confirmation, and then run the commands.
        results = executor.run(plan)

        # 4. Update memory with the context of this interaction
        memory_instance.update(plan=plan, results=results)

        # 5. Summarize the results for the user
        executor.summarize(results)

    except (nl2cmd.InvalidPlanError, ValueError) as e:
        print(persona.inform_error(str(e)))
    except openai.APIError as e:
        print(persona.inform_error(f"I'm having trouble connecting to the AI model. Please check your connection and API settings. Details: {e}"))
    except Exception as e:
        # Catch-all for any other unexpected errors
        print(persona.inform_error(f"An unexpected error occurred: {e}"))

if __name__ == "__main__":
    # To run this from the root directory:
    # python -m src.cli.samantha "your command here"
    #
    # You need to have your environment variables set:
    # export CODER_BASE_URL="http://your-model-endpoint/v1"
    # export CODER_MODEL_NAME="your-model-name"
    # export OPENAI_API_KEY="your-api-key-or-EMPTY"
    main()