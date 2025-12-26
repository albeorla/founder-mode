# AgentKit

A functional toolkit for building LangGraph AI agents. Provides reusable infrastructure so you can focus on domain logic.

## Philosophy

**Toolkit, Not Framework**
- Use decorators instead of base classes
- Write LangGraph directly, no wrappers
- Document patterns, don't encode them

## Structure

```
agentkit/
├── infra/           # Infrastructure utilities
│   ├── config.py    # Settings + environment-based overrides
│   ├── logging.py   # Structured logging with context
│   └── decorators.py # @logged, @with_fallback, @retry
│
├── services/        # External service wrappers
│   ├── llm.py       # create_llm() factory for model instantiation
│   ├── search.py    # Tavily wrapper with rate limiting
│   ├── extraction.py # Cascading scraper (Playwright → Readability → BS4)
│   └── vector_store.py # ChromaDB + InMemory backends
│
├── testing/         # Test utilities
│   └── fixtures.py  # Pytest fixtures for mocking external services
│
└── patterns/        # Documented workflow templates
    └── WORKFLOWS.md # Copy-paste LangGraph patterns
```

## Quick Start

```python
from agentkit import create_llm, SearchService, ExtractionService

# Create an LLM instance
llm = create_llm()  # Uses MODEL_NAME env var, defaults to gpt-4o

# Search the web
search = SearchService()
results = await search.search("AI startup trends 2024")

# Extract content from a URL
extractor = ExtractionService()
content = await extractor.extract("https://example.com/article")
```

## Key Components

### Infrastructure (`infra/`)

**Config**: Environment-aware settings with validation
```python
from agentkit.infra import get_settings
settings = get_settings()
print(settings.model_name)  # gpt-4o
```

**Logging**: Structured, context-aware logging
```python
from agentkit.infra import get_logger
logger = get_logger(__name__)
logger.info("Processing request", extra={"user_id": 123})
```

**Decorators**: Functional composition patterns
```python
from agentkit.infra import logged, with_fallback, retry

@logged
@retry(max_attempts=3)
async def fetch_data(url: str) -> dict:
    ...
```

### Services (`services/`)

**LLM**: Factory for language model instances
```python
from agentkit.services import create_llm
llm = create_llm("gpt-4o")  # or claude-3-opus, etc.
response = await llm.ainvoke("Hello!")
```

**Search**: Web search with caching
```python
from agentkit.services import SearchService
search = SearchService()
results = await search.search("market size SaaS 2024")
```

**Extraction**: Multi-stage content extraction
```python
from agentkit.services import ExtractionService
extractor = ExtractionService()
# Tries: Playwright → Readability → BeautifulSoup
content = await extractor.extract(url)
```

**Vector Store**: Semantic memory
```python
from agentkit.services import VectorStoreService
store = VectorStoreService()
await store.add(texts=["fact 1", "fact 2"])
results = await store.query("related query")
```

### Testing (`testing/`)

Pytest fixtures for isolated tests:
```python
# conftest.py
from agentkit.testing import mock_llm, mock_search, mock_extraction

def test_my_agent(mock_llm, mock_search):
    mock_llm.set_response("Test response")
    mock_search.set_results([{"title": "Test", "url": "..."}])
    # Your test here
```

### Patterns (`patterns/`)

See [WORKFLOWS.md](./patterns/WORKFLOWS.md) for copy-paste LangGraph patterns:
- **Linear Chain**: Research → Write
- **Research Loop**: Search → Extract → Evaluate → Repeat
- **Council Pattern**: Multi-model consensus

## Design Principles

1. **Lazy Everything**: Heavy deps (Playwright, ChromaDB) loaded only when needed
2. **Async Native**: All I/O operations are asynchronous
3. **Graceful Fallbacks**: Handle missing API keys, use mock data for testing
4. **Minimal Dependencies**: Core infra has no heavy deps

## Integration with Apps

Apps import agentkit components directly:
```python
# In your app's nodes/researcher.py
from agentkit import SearchService, ExtractionService, logged

@logged
async def research_node(state: State) -> dict:
    search = SearchService()
    results = await search.search(state["query"])
    ...
```

## License

Part of the [founder-mode](https://github.com/albeorla/founder-mode) monorepo.
