"""Put classify's prompt in Langfuse, and run an experiment there - given.

    python3 push_prompt.py --push        # classify.SYSTEM -> prompt "helpdesk-classify", production
    python3 push_prompt.py --experiment  # run the dataset "helpdesk" with the production prompt

The experiment shows up under the dataset in Langfuse, scored by your evaluators,
so two runs can be compared side by side.
"""

import sys

from dotenv import find_dotenv, load_dotenv
from langfuse import get_client

from classify import SYSTEM
from evaluators import right_kind, right_order
from experiment import classify_task, load_prompt
from models import connect

load_dotenv(find_dotenv(usecwd=True))


def main():
    client = get_client()
    if "--push" in sys.argv:
        client.create_prompt(name="helpdesk-classify", prompt=SYSTEM, labels=["production"])
        print("Prompt 'helpdesk-classify' is now production.")
    if "--experiment" in sys.argv:
        system = load_prompt(client, "helpdesk-classify", SYSTEM)
        items = client.get_dataset("helpdesk").items
        result = client.run_experiment(
            name="helpdesk-classify", data=items,
            task=lambda *, item, **kwargs: classify_task(connect(), system)(item={"input": item.input}),
            evaluators=[right_kind, right_order])
        print(result.format())
    client.flush()


if __name__ == "__main__":
    main()
