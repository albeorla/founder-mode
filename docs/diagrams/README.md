# PlantUML Diagrams

This folder contains PlantUML diagrams that visualize the FounderMode architecture and workflow.

## Available Diagrams

| Diagram | Description | Best For |
|---------|-------------|----------|
| [system-overview.puml](./system-overview.puml) | High-level system architecture | Understanding the big picture |
| [workflow-sequence.puml](./workflow-sequence.puml) | Agent interaction sequence | Understanding execution flow |
| [components.puml](./components.puml) | Module dependencies | Navigating the codebase |
| [state-machine.puml](./state-machine.puml) | Workflow states and transitions | Debugging and edge cases |

## Viewing the Diagrams

### Option 1: Online Renderer

Copy the `.puml` file contents to:
- [PlantUML Web Server](http://www.plantuml.com/plantuml/uml/)
- [PlantText](https://www.planttext.com/)

### Option 2: VS Code Extension

Install the "PlantUML" extension by jebbs:
1. Open VS Code
2. Install extension: `jebbs.plantuml`
3. Open `.puml` file
4. Press `Alt+D` to preview

### Option 3: Command Line

```bash
# Install PlantUML
brew install plantuml  # macOS
apt install plantuml   # Ubuntu

# Generate PNG
plantuml system-overview.puml

# Generate SVG
plantuml -tsvg system-overview.puml

# Generate all diagrams
plantuml *.puml
```

### Option 4: Docker

```bash
docker run --rm -v $(pwd):/data plantuml/plantuml *.puml
```

## Diagram Descriptions

### System Overview

Shows the layered architecture:
- **User Interface**: CLI and REST API entry points
- **Graph Layer**: LangGraph workflow with agent nodes
- **Tools Layer**: Search, scraping, and reporting utilities
- **Memory Layer**: ChromaDB vector storage
- **External Services**: OpenAI and Tavily APIs

### Workflow Sequence

Shows the temporal flow of a typical analysis:
1. User submits business idea
2. Planner decides research topics
3. Human approval checkpoint
4. Researcher gathers web data
5. Writer synthesizes memo
6. Critic evaluates quality
7. Feedback loop if rejected

### Components

Shows module dependencies within `src/foundermode/`:
- Package structure
- Import relationships
- Data flow between modules

### State Machine

Shows all possible workflow states:
- **Initializing**: Config loading and validation
- **Planning**: Gap analysis and topic selection
- **Researching**: Web search and scraping
- **Writing**: Memo synthesis
- **Critiquing**: Quality evaluation
- **Complete**: Output generation

Includes transition conditions and loop prevention mechanisms.

## Customizing Diagrams

The diagrams use PlantUML's `!theme plain` for a clean look. To customize:

```plantuml
' Change theme
!theme cerulean

' Customize colors
skinparam backgroundColor #F0F0F0
skinparam componentBackgroundColor #E0E0FF

' Adjust fonts
skinparam defaultFontName "Helvetica"
skinparam defaultFontSize 12
```

## Keeping Diagrams Updated

When the codebase changes significantly:
1. Review affected diagrams
2. Update the `.puml` source files
3. Regenerate images if storing rendered versions
4. Commit changes with the code

---

[← Back to Documentation Index](../README.md)
