## Principles for Building Agentic Systems

Agentic systems extend large language models (LLMs) beyond static text generation, enabling them to **act**, **reason**, and **adapt** through the use of **tools**, **context**, and **structured workflows**. This document summarizes key principles for building reliable, scalable, and intelligent agents, based on lessons learned from Typhoon 2.5 and the broader agentic paradigm.

---

## 1. Evaluation-Driven Development (EDD)

Before building any workflow, establish **evaluation-driven development** — the agentic equivalent of test-driven development (TDD). A solid evaluation suite is the foundation for reliability.

- **Metrics first:** Define what success means (accuracy, latency, throughput, etc.).
- **Automate evaluations:** Tests should be fast, repeatable, and consistent.
- **Handle non-determinism:** Use LLM-as-a-judge evaluation for semantic outputs.
- **Iterate scientifically:** Let data, not intuition, guide improvement.

**Goal:** Replace “it feels better” with “the data shows it’s better.”

---

## 2. Context Engineering

**Context is the agent’s working memory.** It includes everything the model sees or remembers—prompts, conversation history, tool results, and external data. Designing good context means curating what’s relevant and how it evolves over time.

### Core Ideas

- **Relevance:** Only include what helps the model decide or act.
- **Structure:** Organize information so the model can parse it easily.
- **Adaptation:** Update and summarize context dynamically as the workflow runs.

### Key Principles

1. **Start with intent** — include only what’s needed for the next decision.
2. **Curate relevant information** — trim noise, summarize past steps.
3. **Design for stages of understanding** — early (background), mid (data + feedback), late (summaries + validation).
4. **Edit context intentionally** — inject reminders, remove outdated data.

**Goal:** Every token in context should have a purpose.

---

## 3. Prompt Engineering

The prompt is the visible layer of the agent’s context. Treat it as **source code** — versioned, structured, and evaluated for quality.

### Principles

1. **Version control your prompts.** Track prompt edits and link them to behavior changes.
2. **Keep it simple.** Use concise, structured formats like XML for clarity.
3. **Prefer guidelines over examples.** Modern LLMs don’t need long few-shots.
4. **Avoid conflicting information.** Ensure all components align in intent.
5. **Make the agent aware of its tools and workflow.**
6. **Prompt in English internally.** Even in multilingual systems, keep reasoning layers in English.

**Goal:** A good prompt disappears — it just works.

---

## 4. Tool Design

Tools extend what the agent can know or do. They are the bridge from **thought** to **action**.

### Principles

1. **Name, document, and return cleanly.**
   - Use descriptive verbs and clear docstrings.
   - Never mislead the model about what a tool does.
2. **Treat the LLM as a flow composer.**
   - Tools should be expressive building blocks, not rigid scripts.
   - Deterministic logic belongs inside tools; reasoning belongs to the LLM.
3. **Be conversational about errors.**
   - Return human-readable messages that help the agent recover.
4. **Tools can be anything.**
   - Wrap APIs, models, or even multimodal components.
5. **Ask: Do you really need a tool?**
   - Instruct the LLM to check its context before calling one.

**Goal:** Tools should empower reasoning, not replace it.

---

## 5. Agentic Workflows

A workflow defines **how the agent thinks, acts, and learns over time**. It connects prompts, tools, and context into a coherent reasoning loop.

### Patterns

- **Agent loop:** “Think → Act → Observe” (the ReAct pattern).
- **Human-in-the-loop:** Add interrupts for safety or review.
- **Memory management:** Use short-, mid-, and long-term memory layers.
- **Pub/Sub communication:** Stream updates for transparency and coordination.

### Architectures

- **Single-agent:** Simple, flexible, ideal for prototypes.
- **Multi-agent:** Specialized agents with clear roles, coordinated by an orchestrator.

**Goal:** Deliver the right context, prompt, and tools at the right time.

---

## 6. Model Selection

Model choice depends on reasoning complexity, latency tolerance, and modality needs.

### Guidelines

- **Reasoning models**: Better for multi-step, tool-heavy workflows.
- **Standard LLMs**: Faster for straightforward tasks.
- **Multimodal models**: Add “senses” (vision, audio, etc.).
- **Model size**: Match capacity to use case — bigger isn’t always better.
- **Prompt optimization**: Use automated tools (e.g., DSPy) before fine-tuning.

**Goal:** Choose the model that fits your workflow, not just the biggest one.

---

## 7. Beyond LLMs

Agentic systems thrive when combined with **non-LLM models** that specialize in perception or classification.

- Use small models for intent detection, OCR, or ASR.
- Use LLMs for reasoning, orchestration, and planning.
- Let specialized models handle generation (image, audio, video).

**Goal:** Treat the LLM as the conductor — not the whole orchestra.

---

## 8. The Agentic Mindset

Building agents is not about chaining prompts and APIs. It’s about **designing context with intention**, **evaluating with discipline**, and **engineering workflows that adapt**.

> The magic doesn’t come from the model alone — it comes from how you build around it.

Iterate, measure, refine. Every improvement in context, tooling, and evaluation brings your system closer to true intelligence.

---

## Principles List (20 + bonuses)

- **#1 Metrics — Define what you measure.** Identify success metrics (accuracy, latency, throughput) and make them actionable.
- **#2 Design test cases for agentic workflows.** Cover happy paths first, then edge/unhappy paths; generate variants with LLMs.
- **#3 Embrace non-determinism.** Use LLM-as-a-judge or categorical checks for semantic evaluation.
- **#4 Context engineering is art and science.** Balance relevance, structure, and cost within the context window.
- **#5 Start with intent.** Include only information needed for the next decision or action.
- **#6 Curate relevant information.** Summarize history and surface key state, preferences, and tool outcomes.
- **#7 Design for stages of understanding.** Early: background; Mid: data + feedback; Late: summaries + validation.
- **#8 Version control your prompt.** Treat prompts as code; track changes and link to evaluation results.
- **#9 Keep it simple (KISS).** Prefer concise, structured prompts (e.g., XML blocks) over verbose instructions.
- **#10 Guidelines over examples.** Use rules and constraints; keep few-shots only when they add clear value.
- **#11 Avoid conflicting information.** Ensure prompts, tool specs, and context updates never disagree.
- **#12 Make the agent tool- and workflow-aware.** Explain what tools do, when to use them, and how they interact.
- **#13 Name it, document it, return it.** Clear verbs, honest docs, and readable returns (plus deterministic behavior).
- **#14 Treat the LLM as a flow composer.** Wrap deterministic steps; expose semantically meaningful building blocks.
- **#15 Be conversational about errors.** Return human-readable errors that enable recovery or retries.
- **#16 Remember: tools can be anything.** Wrap APIs, smaller models, OCR/ASR, or generators as tools.
- **#17 Do you really need tools?** Instruct the agent to search its context before calling a tool.
- **#18 The agent loop.** Implement Think → Act → Observe; mix deterministic and generative nodes judiciously.
- **#19 Human in the loop.** Add interrupts/approvals for sensitive or high-impact actions.
- **#20 Memory matters.** Combine short-, mid-, and long-term memory across loops and sessions.

**Bonuses**

- **Context editing.** Inject or prune messages to steer understanding; remove stale tool outputs.
- **Prompt in English internally.** Keep system/tool specs in English; localize I/O as needed.
- **Pub/Sub updates.** Stream intermediate progress to users and coordinate across agents.

**Build with intention. Evaluate with rigor. Design context that thinks.**