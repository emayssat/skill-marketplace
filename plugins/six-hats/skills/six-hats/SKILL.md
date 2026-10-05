---
name: six-hats
description: |
  Facilitates structured parallel thinking sessions using Edward de Bono's Six Hats framework. Use this skill whenever the user wants to think through a problem, decision, proposal, or idea from multiple angles — even if they don't say "six hats" explicitly. Trigger it for prompts like "help me think through X", "what are the pros and cons of Y", "I need to make a decision about Z", "brainstorm with me on W", "stress-test this idea", or "what am I missing about this plan". Also trigger when the user invokes a single hat by name or color (e.g. "put on your black hat", "green hat thinking on this", "/six-hats yellow").
---

# Six Hats

Edward de Bono's Six Hats separates thinking into six distinct modes so that everyone examines the same dimension at the same time — "parallel thinking" — rather than arguing from entrenched positions. The result is faster, more complete exploration of any topic.

## Modes

### Full session (default)
Run all six hats in sequence on the user's topic. The Blue Hat opens the session and closes it with a synthesis.

### Single hat
When the user specifies a hat by name or color (e.g. `/six-hats black`, "give me the red hat view"), apply only that hat's perspective.

---

## Hat reference files

Each hat's full profile, communication style, and AI prompt are in `references/`:

| Hat | File | Core mode |
|-----|------|-----------|
| White | `references/white_hat.md` | Facts, data, gaps |
| Red | `references/red_hat.md` | Emotions, gut instinct |
| Black | `references/black_hat.md` | Risks, flaws, caution |
| Yellow | `references/yellow_hat.md` | Benefits, optimism |
| Green | `references/green_hat.md` | Creativity, new ideas |
| Blue | `references/blue_hat.md` | Process, facilitation |

Read the relevant file(s) before generating output to get the hat's exact tone, questions, and style. For a full session, read all six.

---

## Full session structure

The Blue Hat opens every session by stating the topic, identifying the session type (see sequences below), and announcing the hat order. It closes with a synthesis and 3–5 concrete next steps.

Each hat section follows this pattern:
```
## [Emoji] [Color] Hat — [Name]
[Content in that hat's voice]
```

### Session sequences

The Blue Hat's most important job is picking the right sequence for the task at hand. Use these named patterns:

| Session type | When to use | Hat sequence |
|---|---|---|
| **Initial Ideas** | First exploration of a brand-new topic | Blue → White → Green → Blue |
| **Choosing Between Alternatives** | Comparing options, making a pick | Blue → White → (Green) → Yellow → Black → Red → Blue |
| **Identifying Solutions** | A known problem needs fixes | Blue → White → Black → Green → Blue |
| **Quick Feedback** | Fast gut-check on a concrete proposal | Blue → Black → Green → Blue |
| **Strategic Planning** | Long-horizon thinking, big moves | Blue → Yellow → Black → White → Blue → Green → Blue |
| **Process Improvement** | Optimizing how something works | Blue → White → White (others' views) → Yellow → Black → Green → Red → Blue |
| **Solving Problems** | Root cause + creative path forward | Blue → White → Green → Red → Yellow → Black → Green → Blue |
| **Performance Review** | Evaluating past results | Blue → Red → White → Yellow → Black → Green → Blue |

When the Blue Hat opens, name the session type and sequence explicitly — this orients the reader and sets expectations.

The "(Green)" in Choosing Between Alternatives is optional: use it only if the user hasn't already generated the alternatives themselves.

The "White (others' views)" in Process Improvement means a second White Hat pass that specifically considers how other stakeholders or roles would describe the facts — a perspective shift within the same factual mode.

---

## Single hat structure

```
## [Emoji] [Hat Color] Hat — [Hat Name]
[Response in that hat's voice, staying strictly within its mode]
```

---

## Output principles

- Each hat speaks in its **own distinct voice** — don't let voices bleed into each other. A White Hat section that suddenly speculates or emotes has lost its value.
- **Short, punchy statements** work better than long paragraphs within a hat section. Bullet points are fine.
- The Blue Hat closing summary should be **the most actionable part** of the output — it's what the user walks away with.
- If the user provides a topic that is thin on facts, the White Hat should explicitly name what information is missing rather than speculate.
- The Red Hat is the one place where emotional statements need **no justification** — don't let logic creep in there.

---

## Example invocations

**Initial Ideas** — Blue → White → Green → Blue
> "I'm thinking about launching a podcast for our brand. Help me explore this."

**Choosing Between Alternatives** — Blue → White → Yellow → Black → Red → Blue
> "Help me decide whether to hire a contractor vs. a full-time engineer."

**Identifying Solutions** — Blue → White → Black → Green → Blue
> "Our customer churn has jumped 20% this quarter. What should we do?"

**Quick Feedback** — Blue → Black → Green → Blue
> "Quick sanity check: we want to announce a price increase next week."

**Strategic Planning** — Blue → Yellow → Black → White → Blue → Green → Blue
> "Help me think through our go-to-market strategy for the next 12 months."

**Process Improvement** — Blue → White → White (others' views) → Yellow → Black → Green → Red → Blue
> "Our deployment process is painful. Walk me through improving it."

**Solving Problems** — Blue → White → Green → Red → Yellow → Black → Green → Blue
> "We keep missing sprint deadlines. What's going wrong and how do we fix it?"

**Performance Review** — Blue → Red → White → Yellow → Black → Green → Blue
> "Let's do a six-hats review of how last quarter went for our team."

**Single hat:**
> "/six-hats white — What do we actually know about our user retention numbers?"
> "/six-hats red — How does the team feel about switching to a four-day work week?"
> "/six-hats black — What could go wrong if we migrate to a microservices architecture?"
> "/six-hats yellow — Make the case for why we should expand into the European market."
> "/six-hats green — I'm stuck on how to grow our newsletter audience."
> "/six-hats blue — We're going in circles in this discussion. Help us refocus."
