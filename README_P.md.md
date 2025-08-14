# Rally Story Template Matrix (Agentic Dev)

This repo contains 25 lean templates (5 story types × 5 code bases) designed for an orchestrator agent to map stories to code files quickly.

## Structure
- `templates/<StoryType>/<CodeBase>.md` – Combination templates
- `samples/` – Example INITIAL.md files
- `CLAUDE.md` – Coding conventions & agent rules

## Usage
1. Pick a Story Type file and Code Base file, or use the combined template directly.
2. Fill in acceptance criteria, domains, and mapping hints.
3. Feed the completed template to your orchestrator agent.

## Story Types
- Feature, Defect, Task, Enhancement, Incident

## Code Bases
- React App, Node.js API, Java Spring Boot, Java Microservice, Apollo GraphQL Service