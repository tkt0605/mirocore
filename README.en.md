# Miroc Core v0.0.1

[日本語](README.md)

## Overview and Quick Start
Miroc Core is the foundation for a Personal Robot that builds long-term relationships with people.
It aims to do more than reply to a conversation: understand a user's events and relationships, and carry that memory into future conversations and actions.
The end goal is a system foundation where memory, personality, and relationships persist even when the robot's body changes.

Miroc Core v0.0.1 starts by setting up the development environment and a basic system structure, then builds the minimum form of a Personal Robot with long-term memory.

The development environment uses Docker.
```bash
docker compose up --build
```

From the repository root, run:
```bash
uv run python -m mirocore.terminal_robot
```

Run the tests as follows.
```bash
docker compose run --rm mirocore uv run pytest
```
Local test command:
```bash
uv run pytest -v
```
Command to launch FastAPI:
```bash
uv run uvicorn mirocore.api:app --app-dir src --reload
```

## Vision
MirocBot is not built as a merely convenient tool. It aims to be a presence that spends a long time with people and builds a relationship with them.
People build relationships with friends and family by sharing experiences.

Miroc aims for the same kind of abilities:

- Tell about past events.
- Understand and remember what is happening now.
- Understand the user's values and preferences.
- Remember long-term goals and concerns.
- Use past memories naturally in the current conversation.
- Remember time spent together.

MirocBot aims to be a Personal Robot that spends time with a person, accumulates experience, and continues a relationship over years and decades.
The robot's body may change. What is inside — its "mind" — stays.

This is one of the core ideas of Miroc Core.
> The body can change.
> The relationship remains.

## Why build MirocBot?
The name MirocBot comes from Maitreya (Miroku Bosatsu) in Buddhism.
Maitreya is regarded as a future Buddha who appears in this world in the distant future and saves people.
MirocBot does not try to reproduce that teaching directly.
It inherits it as this idea:
"A presence that, even in the distant future — as far as the far side of the galaxy — remains beside people and keeps supporting them."

Many current AI services mainly aim to answer questions or make work more efficient.
MirocBot takes on an additional question: whether a long-term relationship can form between a person and an AI.

The first product it aims for is a pocket-sized Personal Robot.
That robot remembers conversations and events with the user, and can recall past experiences even after time has passed.

## Core concepts
MirocBot is built mainly from the following elements.
```
Miroc Core
├── Identity
├── Memory
├── Relationship
├── Perception
└── Action
```
### Identity
Defines what kind of being Miroc is.
It mainly covers:

- Name
- Personality
- Way of speaking
- Values
- Principles of action
- Constraints of the system

Identity does not change easily through a short conversation. It is treated as the core of Miroc's personality.

### Memory
Stores information that needs to last, drawn from conversations and events with the user.
It does not simply keep every conversation log. It organizes them as memories that carry meaning.

In the future, it will mainly handle:

- Semantic Memory: memory of meaning.
- Episodic Memory: memory of conversations (episodes).
- Relationship Memory: memory of relationships.
- Autobiographical Memory: memory used to tell about itself.

### Relationship
Manages the relationship between the user and Miroc.

For example:

- Events experienced together
- What the user is working on now
- Change since the past
- Goals that continue
- The long-term relationship

### Perception
The layer that receives information from outside.

In the future it will handle:

- Text
- Audio
- Camera
- Various sensors

### Action
Handles what Miroc outputs to the outside.
In the future this covers:

- Conversation
- Audio output
- LEDs
- A display
- Motors
- Robot motion

## Architecture
Miroc Core does not treat the LLM as the controller of the whole system.
The LLM handles cognition: understanding input, referring to memory, and producing a response.
Actual system operations, such as the database and the robot, are handled by programs kept separate from the LLM.

The basic structure is:
```
User
 │
 ▼
Input
 │
 ▼
Miroc Core
 ├── Identity
 ├── Memory
 ├── Relationship
 └── Context
 │
 ▼
LLM
 │
 ▼
Response / Proposal
 │
 ▼
Policy
 │
 ▼
Output / Action
```
The LLM receives the information it needs and generates a response or a candidate action.
When an actual operation is required, it always goes through policy for verification, and only permitted processing runs.


## Security design and policy
In Miroc Core, safety is part of the basic system design. It is built in from the start.

The basic principle for the LLM is:
> An LLM has cognition, not authority.
The LLM can understand information, refer to memory, and propose responses or actions. It is not given the authority to operate the system directly.

As a rule, the LLM is not given direct access to the following.

- OS / Shell
- The host filesystem
- Direct writes to the database
- API keys and credentials
- Arbitrary network access
- Direct control of motors and other hardware

What the LLM generates is treated as a proposal, not a command. The system side verifies the actual processing.
> The model may suggest. The system decides.

## Sandbox design
Processing that involves the LLM runs, as far as possible, in a sandbox isolated from the rest of the system.
Functions available from the sandbox are limited to interfaces permitted in advance.

```bash
LLM Sandbox
─────────────────────
No Shell
No Host Filesystem
No Direct DB Access
No Direct Hardware Access
No Secrets
Restricted Network
─────────────────────
Allowed Interfaces Only
```
For example, even when handling memory, the LLM does not operate the database directly.
It goes through the search function provided by Miroc Core.
```bash
LLM
 │
 ▼
Memory Search Interface
 │
 ▼
Memory Database
```

Future robot control keeps the same boundary.
```bash
LLM
 │
 ▼
Action Proposal
 │
 ▼
Policy Check
 │
 ▼
Robot Controller
```
Security does not depend on the prompt alone. The basic policy is to enforce it technically through permission controls in Docker, the OS, and the application.

## MVP
This MVP does not aim to build the robot body.
It first builds the minimum structure that makes Miroc's personality and long-term memory work.

The goal of Miroc Core v0.0.1 is:
> Create a model that remembers important past events and can recall them naturally in conversation days or weeks later.

The initial MVP implements the following.

- Text conversation
- Conversation history
- Extraction of long-term memory candidates
- Saving memory
- Searching memory
- Retrieving related memories
- Building the context passed to the LLM
- Response generation by the LLM
- A basic Policy Layer
- Runtime isolation with Docker

The initial MVP leaves out the following.

- ROS 2
- The robot body
- Motor control
- Computer vision
- Autonomous movement
- A humanoid
- Autonomous operation of external services

First, establish Miroc with memory. Then give it a body.


## Development environment
Docker is the base of the main development environment, so differences in dependencies stay out of the way.

The initial stack is:
```
Python
Docker
Docker Compose
PostgreSQL
pytest
```

The basic layout is:
```
Host
 │
 ▼
Docker Compose
 │
 ├── Miroc Core
 │      └── Python
 │
 └── Database
        └── PostgreSQL
```
Later, services can be split as needed:
```
Miroc Core
Memory Service
LLM Sandbox
Policy Engine
Robot Controller
Database
```
At the start, this stays a small structure that is easy to understand, without splitting into too many microservices.
