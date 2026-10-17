# Week 6 milestone - Helpdesk that remembers. Start from your
# week-03/milestone/helpdesk.py:
#
#   1. build_helpdesk(model, backup=None, checkpointer=None, store=None)
#      compiles with store=store.
#
#   2. DESK_TOOLS = refunds.REFUND_TOOLS + [remember_fact, known_facts, forget_me]
#      used by lookup and by the ToolNode.
#
#   3. memory_for(store, customer, ticket) -> str
#      "" if store is None. Otherwise, joined with a blank line between those
#      that are not empty:
#          procedures_for_prompt(store)
#          facts_for_prompt(store, customer)
#          episodes_for_prompt(relevant_episodes(store, customer, ticket))
#
#   4. lookup(state, model, backup, runtime: Runtime)
#      (from langgraph.runtime import Runtime - LangGraph fills it in.)
#      The brief is SYSTEM + REFUND_RULE + MEMORY_RULE + " This ticket is about:
#      <kind>" + ", order <id>" if any + "." - then, if memory_for(runtime.store,
#      ...) is not empty, a blank line and the memory.
#
#   5. remember(state, config: RunnableConfig, model, runtime: Runtime)
#      a new node after draft: if there is a store, summarise the ticket and its
#      reply into an Episode and record it under the thread id
#      (config["configurable"]["thread_id"]) - or "untracked/<8 random hex>" when
#      run without a thread - dated today (date.today().isoformat()).
#      draft -> remember -> END. A ticket handed to a person is not remembered.
