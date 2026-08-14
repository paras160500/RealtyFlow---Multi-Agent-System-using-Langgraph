from typing import Annotated, Literal

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, SystemMessage
from langgraph.graph.message import add_messages
from langgraph.types import Command
from pydantic import BaseModel
from typing_extensions import TypedDict

from src.prompts import (
    PROPERTY_PROFILE_AGENT_PROMPT,
    SUPERVISOR_PROMPT,
    TRANSACTION_HISTORY_AGENT_PROMPT,
)
from src.tools import (
    calculate_mortgage_affordability,
    calculate_price_per_sqft,
    calculate_remaining_lease,
)

load_dotenv()

MODEL_NAME = "gpt-4o-mini"
TEMPERATURE = 0.0

routing_llm = init_chat_model(
    model=MODEL_NAME,
    temperature=TEMPERATURE,
)

supervisor_agent = create_agent(
    model=init_chat_model(
        model=MODEL_NAME,
        temperature=TEMPERATURE,
    ),
    tools=[calculate_mortgage_affordability],
)

transaction_history_agent = create_agent(
    model=init_chat_model(
        model=MODEL_NAME,
        temperature=TEMPERATURE,
    ),
    tools=[calculate_price_per_sqft],
)

property_profile_agent = create_agent(
    model=init_chat_model(
        model=MODEL_NAME,
        temperature=TEMPERATURE,
    ),
    tools=[calculate_remaining_lease],
)


class SupervisorState(TypedDict, total=False):
    messages: Annotated[list, add_messages]
    next: str | None
    property_name: str


class SupervisorDecision(BaseModel):
    next_agent: Literal[
        "transaction_history_agent",
        "property_profile_agent",
        "none",
    ]
    property_name: str = ""
    response: str = ""


def _invoke_agent(agent, prompt: str, messages: list, agent_name: str):
    agent_input = {
        "messages": [SystemMessage(content=prompt)] + messages
    }

    agent_result = agent.invoke(agent_input)
    response_message = agent_result["messages"][-1]
    response_message.name = agent_name

    return response_message


def supervisor_conditional_node(state: SupervisorState) -> dict:
    response = _invoke_agent(
        supervisor_agent,
        SUPERVISOR_PROMPT,
        state["messages"],
        "supervisor",
    )

    print(f"Supervisor: {response.content}")

    return {"messages": [response]}


def supervisor_command_node(state: SupervisorState) -> Command:
    decision: SupervisorDecision = (
        routing_llm
        .with_structured_output(SupervisorDecision)
        .invoke(
            [SystemMessage(content=SUPERVISOR_PROMPT)]
            + state["messages"]
        )
    )

    print(
        f"Supervisor Decision: "
        f"next_agent={decision.next_agent}, "
        f"property={decision.property_name}"
    )

    if decision.next_agent == "none":
        response = _invoke_agent(
            supervisor_agent,
            SUPERVISOR_PROMPT,
            state["messages"],
            "supervisor",
        )

        print(f"Supervisor: {response.content}")

        update = {"messages": [response]}

        if decision.property_name:
            update["property_name"] = decision.property_name

        return Command(
            goto="__end__",
            update=update,
        )

    update = {
        "messages": [
            AIMessage(
                content=f"Routing to {decision.next_agent}",
                name="supervisor",
            )
        ]
    }

    if decision.property_name:
        update["property_name"] = decision.property_name
        print(
            f"Supervisor: Extracted property_name = "
            f"{decision.property_name}"
        )

    print(f"Supervisor: Routing to {decision.next_agent}")

    return Command(
        goto=decision.next_agent,
        update=update,
    )


def transaction_history_agent_node(state: SupervisorState) -> Command:
    property_name = state.get("property_name", "")
    context = f"Property: {property_name}" if property_name else ""

    prompt = TRANSACTION_HISTORY_AGENT_PROMPT.format(
        context=context
    )

    response = _invoke_agent(
        transaction_history_agent,
        prompt,
        state["messages"],
        "transaction_history_agent",
    )

    print(f"Transaction History Agent: {response.content}")

    return Command(
        goto="__end__",
        update={"messages": [response]},
    )


def property_profile_agent_node(state: SupervisorState) -> Command:
    property_name = state.get("property_name", "")
    context = f"Property: {property_name}" if property_name else ""

    prompt = PROPERTY_PROFILE_AGENT_PROMPT.format(
        context=context
    )

    response = _invoke_agent(
        property_profile_agent,
        prompt,
        state["messages"],
        "property_profile_agent",
    )

    context_str = f" ({property_name})" if property_name else ""

    print(
        f"Property Profile Agent{context_str}: "
        f"{response.content}"
    )

    return Command(
        goto="__end__",
        update={"messages": [response]},
    )