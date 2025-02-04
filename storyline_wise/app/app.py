import os

import streamlit as st
from streamlit_feedback import streamlit_feedback
import nest_asyncio

from dotenv import load_dotenv

from storyline.agent.data_analysis_tool import DataAnalysisTool
from storyline_wise.app.agent import make_agent
from storyline_wise.app.preload_data import cached_load

try:
    # This makes the app access the LLMs through the Wise gateway
    from wise_chain.init_defaults import (
        init_motleycrew_defaults,
        init_llamaindex_defaults,
    )

    team = "local"
    use_case = "Planning helper bot"
    init_motleycrew_defaults(team=team, use_case=use_case)
    init_llamaindex_defaults(team=team, use_case=use_case)

except ImportError:
    pass


assert load_dotenv("../../../.env"), "No .env file found"
# # Uncomment this if you run WiseChain from source
# import os, sys
#
# here = os.path.dirname(os.path.abspath(__file__))
# root = os.path.realpath(os.path.join(here, "../.."))
# sys.path.append(os.path.join(root, "wise-chain"))

current_dir = os.path.dirname(os.path.realpath(__file__))
AVATAR_AI = f"{current_dir}/assets/avatar_ai.png"
AVATAR_USER = f"{current_dir}/assets/avatar_user.png"
base_path = os.path.dirname(os.path.realpath(__file__)) + "/../../.."
context_location = os.path.realpath(
    os.path.join(base_path, "storyline/playground", "context.pkl")
)

config_path = os.path.realpath(
    os.path.join(base_path, "storyline/playground", "config.yaml")
)

query = "select * from rpt_marketing.TOP_MOVERS_RESULTS_PROFILES"

df = cached_load(query)
if "data_tool" not in st.session_state:
    st.session_state.data_tool = DataAnalysisTool(
        df, description="Use this tool for data analysis questions on MNCs"
    )


st.set_page_config(
    page_title="Question answerer", page_icon="open_file_folder", layout="wide"
)

# Init the bot


if "draft" not in st.session_state:
    st.session_state.draft = {
        "markdown": """## This is the draft stuff to evaluate
 * oh yes it is """,
        "rendered": False,
    }

if "last_input" not in st.session_state:
    st.session_state["last_input"] = ""


if "chatbot" not in st.session_state:

    st.session_state.chatbot = make_agent(
        st.session_state.draft,
        context_location=context_location,
        config_path=config_path,
        # data_tool=st.session_state.data_tool,
    )
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [
            {
                "role": "assistant",
                "avatar": AVATAR_AI,
                "content": "What's on your mind?",
            }
        ]

if "last_input" not in st.session_state:
    st.session_state["last_input"] = ""


st.subheader("Storyteller bot", divider="blue")
# with st.expander("Settings", expanded=True):


col6, col7, col8 = st.columns([0.3, 0.3, 0.4], gap="small")

with col7:
    st.markdown(st.session_state.draft["markdown"])
    st.session_state.draft["rendered"] = True

with col8:
    draft = st.text_area(
        label="Edit the draft here",
        value=st.session_state.draft["markdown"],
        height=800,
    )
    draft_changed = draft != st.session_state.draft["markdown"]
    st.session_state.draft["markdown"] = draft

with col6:
    with st.container(height=800):
        # Render message history
        for message in st.session_state.messages:
            # Write each message as a chat message
            with st.chat_message(message["role"], avatar=message["avatar"]):
                st.write(message["content"])

        # Append new draft to prompt if necessary
        if True:  # draft_changed:
            latest_draft = f"""Here is the latest version of draft. 
        Please ignore all earlier versions from now on:
        ```{draft}```
        """
        else:
            latest_draft = ""

        # This is just a hack: user input is entered last, so we need to store it and re-run
        last_input = st.session_state["last_input"]
        st.session_state["last_input"] = ""

        # If the user changed something, append it to chat history
        # Not great, we should maybe purge earlier drafts?
        if last_input:
            st.session_state.messages.append(
                {"role": "user", "avatar": AVATAR_USER, "content": last_input}
            )
            # and render it
            with st.chat_message("user", avatar=AVATAR_USER):
                st.write(last_input)

        # Generate a new response if last message is not from assistant
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant", avatar=AVATAR_AI):
                with st.spinner("Thinking... "):
                    # This is the only place where we interact with the bot
                    response = st.session_state.chatbot.invoke(
                        {"human_input": last_input, "latest_draft": latest_draft}
                    )
                    st.write(response)
                    feedback = streamlit_feedback(
                        feedback_type="faces",
                        optional_text_label="[Optional] Please provide an explanation",
                    )
                    # TODO! store this feedback somewhere

                    message = {
                        "role": "assistant",
                        "avatar": AVATAR_AI,
                        "content": response,
                    }
                    st.session_state.messages.append(message)

        new_user_input = st.chat_input(placeholder="Your input... ")
        if new_user_input or draft_changed or not st.session_state.draft["rendered"]:
            st.session_state["last_input"] = new_user_input
            st.rerun()  # el
