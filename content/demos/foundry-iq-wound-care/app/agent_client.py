"""
Foundry IQ wound-care demo — agent client (Engineer rail, optional).

Adapted from Microsoft Learn exercise 04 "Integrate an AI agent with Foundry IQ":
https://microsoftlearning.github.io/mslearn-ai-agents/Instructions/Exercises/04-integrate-agent-with-foundry-iq.html

This is the *completed* client (the tutorial's two TODOs are filled in) pointed at the
`woundcare-iq-agent` you build in ../README.md. It connects to the agent by name and, if the agent
is set to "ask for approval for all tools", prompts you to approve each Foundry IQ knowledge-base
lookup so you can watch the grounded, cited answer come back.

Requires a live Foundry tenant + `az login`. See README.md in this folder.
"""
import os
import json
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Load environment variables
load_dotenv()
project_endpoint = os.getenv("PROJECT_ENDPOINT")
agent_name = os.getenv("AGENT_NAME")

# Validate configuration
if not project_endpoint or not agent_name:
    raise ValueError("PROJECT_ENDPOINT and AGENT_NAME must be set in .env file")

print(f"Connecting to project: {project_endpoint}")
print(f"Using agent: {agent_name}\n")

# --- Connect to the project and agent, and create a conversation ---
credential = DefaultAzureCredential(
    exclude_environment_credential=True,
    exclude_managed_identity_credential=True,
)
project_client = AIProjectClient(
    credential=credential,
    endpoint=project_endpoint,
)

# Get the OpenAI-compatible client
openai_client = project_client.get_openai_client()

# Get the agent by name
agent = project_client.agents.get(agent_name=agent_name)
print(f"Connected to agent: {agent.name} (id: {agent.id})\n")

# Create a new conversation
conversation = openai_client.conversations.create(items=[])
print(f"Created conversation (id: {conversation.id})\n")


# Conversation history for context (client-side tracking)
conversation_history = []


def send_message_to_agent(user_message):
    """
    Send a message to the agent and handle the response using the conversations API,
    including the Foundry IQ (MCP) approval flow when the agent requires approval.
    """
    try:
        print("\nAgent: ", end="", flush=True)

        # Add user message to the conversation
        openai_client.conversations.items.create(
            conversation_id=conversation.id,
            items=[{"type": "message", "role": "user", "content": user_message}],
        )

        # Store in conversation history (client-side)
        conversation_history.append({"role": "user", "content": user_message})

        # Create a response using the agent
        response = openai_client.responses.create(
            conversation=conversation.id,
            extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
            input="",
        )

        # Check if the response output contains an approval request (Foundry IQ tool call)
        approval_request = None
        if hasattr(response, "output") and response.output:
            for item in response.output:
                if hasattr(item, "type") and item.type == "mcp_approval_request":
                    approval_request = item
                    break

        # Handle approval request if present
        if approval_request:
            print(f"\n[Approval required for: {approval_request.name}]")
            print(f"Server: {approval_request.server_label}")
            try:
                args = json.loads(approval_request.arguments)
                print(f"Arguments: {json.dumps(args, indent=2)}\n")
            except Exception:
                print(f"Arguments: {approval_request.arguments}\n")

            # Prompt user for approval
            approval_input = input(
                "Approve this knowledge-base lookup? (yes/no): "
            ).strip().lower()
            approve = approval_input in ("yes", "y")
            print("Approving lookup...\n" if approve else "Lookup denied.\n")

            # Send the approval / denial back into the conversation
            openai_client.conversations.items.create(
                conversation_id=conversation.id,
                items=[{
                    "type": "mcp_approval_response",
                    "approval_request_id": approval_request.id,
                    "approve": approve,
                }],
            )

            # Get the actual response after approval/denial
            response = openai_client.responses.create(
                conversation=conversation.id,
                extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
                input="",
            )
            print("Agent: ", end="", flush=True)

        # Extract the response text
        if response and response.output_text:
            response_text = response.output_text
            print(f"{response_text}\n")

            # Check for citations if available (Foundry IQ grounding)
            if hasattr(response, "citations") and response.citations:
                print("\nSources:")
                for citation in response.citations:
                    print(f"  - {citation.content if hasattr(citation, 'content') else 'Knowledge Base'}")

            # Store in conversation history (client-side)
            conversation_history.append({"role": "assistant", "content": response_text})
            return response_text
        else:
            print("No response received.\n")
            return None
    except Exception as e:
        print(f"\n\nError: {str(e)}\n")
        return None


def display_conversation_history():
    """Display the full conversation history."""
    print("\n" + "=" * 60)
    print("CONVERSATION HISTORY")
    print("=" * 60 + "\n")
    for turn in conversation_history:
        print(f"{turn['role'].upper()}: {turn['content']}\n")
    print("=" * 60 + "\n")


def main():
    """Main interaction loop."""
    print("Care Pal - Wound-Care Information Agent (grounded on Foundry IQ)")
    print("Ask a wound-care question. Answers come only from the curated knowledge base.")
    print("Try: 'How should I care for a small cut at home?'")
    print("Type 'history' to see the conversation, or 'quit' to exit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() == "quit":
                print("\nEnding conversation...")
                break
            if user_input.lower() == "history":
                display_conversation_history()
                continue
            send_message_to_agent(user_input)
        except KeyboardInterrupt:
            print("\n\nInterrupted by user.")
            break
        except Exception as e:
            print(f"\nUnexpected error: {str(e)}\n")

    print("\nConversation ended.")


if __name__ == "__main__":
    main()
