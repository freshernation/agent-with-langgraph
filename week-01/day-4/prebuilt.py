# Day 4 - the library's version of what you wrote yesterday, and tracing it.
#
# Copy desk_graph.py from day 3 into this folder.
#
#   build_prebuilt(model)
#       from langchain.agents import create_agent
#       the same Desk - desk_graph's TOOLS and SYSTEM - built by create_agent
#       (system_prompt=SYSTEM). Then read create_agent's source: READING.md.
#
#   config_for(user, session, callbacks, limit=10) -> dict
#       the config one traced run is invoked with:
#           {"callbacks": callbacks,
#            "recursion_limit": limit,
#            "metadata": {"langfuse_user_id": user, "langfuse_session_id": session}}
#       Langfuse's LangChain handler reads those two metadata keys, so every
#       run by one person, in one conversation, lands in one session.
