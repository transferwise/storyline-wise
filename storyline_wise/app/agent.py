import markdown
from typing import Optional
import logging

from langchain.prompts import ChatPromptTemplate

from motleycrew.agents.parent import MotleyAgentParent
from motleycrew.agents.langchain import ReActToolCallingMotleyAgent
from motleycrew.tools import MotleyTool
from motleycrew.common.exceptions import InvalidOutput
from storyline.rag.retrieve.retrieval_context import load_context

from storyline.rag.retrieve.retrieval_tool import QuestionAnsweringTool

logger = logging.getLogger(__name__)


class MarkdownWriterTool(MotleyTool):
    def __init__(self, output_location: dict):
        super().__init__(
            name="WriteMarkdownTool",
            description="Displays markdown in the UI",
            exceptions_to_reflect=[ValueError, InvalidOutput],
            return_direct=True,
        )
        self.output_location = output_location

    def run(self, markdown_string: str) -> str:
        err = errors_in_markdown(markdown_string)
        if errors_in_markdown(markdown_string) is not None:
            # Ask the agent to try again
            raise InvalidOutput(err)

        self.output_location["markdown"] = markdown_string
        self.output_location["rendered"] = False

        return "Markdown updated!"


# This is just a workaround for the Motleycrew bug
class PassthroughTool(MotleyTool):
    def __init__(self):
        super().__init__(
            name="Passthrough_tool",
            description="Return a simple message back to the user",
            exceptions_to_reflect=[ValueError, InvalidOutput],
            return_direct=True,
        )

    def run(self, reply: str) -> str:
        return reply


def make_agent(
    output_location: dict,
    context_location: str,
    config_path: str,
    data_tool: Optional[MotleyTool] = None,
) -> MotleyAgentParent:
    markdown_tool = MarkdownWriterTool(output_location)
    context = load_context(context_location, config_path)
    logger.info(f"for making the agent, loaded {context}")
    question_answering_tool = QuestionAnsweringTool(context)
    tools = [markdown_tool, question_answering_tool, PassthroughTool()]
    if data_tool is not None:
        tools.append(data_tool)

    writer = ReActToolCallingMotleyAgent(
        name="Summary producer agent",
        prompt_prefix=ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """Your job is to retreive information on the topic you asked about using the 
                    Question_Answering_Tool, 
                    summarize it in nice markdown format, and 
render it in the UI using the provided tool; then iterate with the user to refine the summary.
Here is the last message from the user: {human_input}.
When you are asked to create or modify the outline, DO IT USING THE MARKDOWN TOOL PROVIDED.
MAKE SURE YOU INCLUDE IN YOUR REPLY AS MANY RELEVANT LINKS AS POSSIBLE, BUT ONLY
FROM THE LINKS PROVIDED IN THE RESPONSE OF THE Question_Answering_Tool.

If a user asks you a question, just return the text of the answer using the Passthrough tool.
        {latest_draft}""",
                )
            ]
        ),
        tools=tools,
        force_output_handler=True,
        verbose=True,
    )
    return writer


def errors_in_markdown(md_string):
    try:
        # Convert Markdown to HTML
        html = markdown.markdown(md_string)
        return None  # If it renders without errors, it's valid
    except Exception as e:
        return str(e)  # If an error occurs, it's not valid


if __name__ == "__main__":
    output_location = {}
    agent = make_agent(
        output_location,
        "***\context.pkl",
    )
    agent.invoke({"human_input": "What color is the ocean?", "latest_draft": ""})
    print("yay!")
