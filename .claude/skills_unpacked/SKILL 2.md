---
name: hoi4-event-searcher
version: 1.0.0
description: Helper for searching and analyzing events in Hearts of Iron IV mods
tags: [hoi4, modding, events, country_event, news_event, searcher]
---

# HOI4 Event Searcher

This skill helps you search and analyze **events** in Hearts of Iron IV mods. Quickly find events, analyze event chains, and understand event mechanics.

## What This Skill Does

- Search for specific events by ID or namespace
- Find events by effects or triggers
- Analyze event chains
- Find event options and outcomes
- Search by event type (country, news, state)
- Locate MTTH events
- Find triggered events

---

## Using This Skill

### Step 1: Ask User What to Search

Ask the user what they want to find:

1. **Search by event ID** - Find specific event
2. **Search by namespace** - Find all events in namespace
3. **Search by effect** - Find events with specific effects
4. **Search by trigger** - Find events with specific conditions
5. **Search by type** - Find country/news/state events
6. **Analyze event chain** - Trace event sequences
7. **Find MTTH events** - Find events with mean_time_to_happen

---

## Search Patterns

### Search 1: Find Event by ID

**Ask for:** Event ID (e.g., `german_events.1`)

**Use Grep:**
```
Pattern: id\s*=\s*german_events\.1\b
Path: events/
Output: content
-B: 2
-A: 50
```

**Explanation:** Shows the entire event definition

---

### Search 2: Find Events by Namespace

**Ask for:** Namespace (e.g., `german_events`)

**Use Grep:**
```
Pattern: namespace\s*=\s*german_events
Path: events/
Output: content
-A: 3
```

**Then list all events:**
```
Pattern: id\s*=\s*german_events\.\d+
Path: events/
Output: content
-A: 5
```

---

### Search 3: Find Events with Specific Effect

**Ask for:** Effect type (e.g., "add_political_power", "declare_war")

**Use Grep:**
```
Pattern: add_political_power
Path: events/
Output: content
-B: 30
-A: 5
```

**Explanation:** Shows events that grant political power (adjust -B to see event ID)

---

### Search 4: Find Country Events

**Use Grep:**
```
Pattern: country_event\s*=\s*\{
Path: events/
Output: content
-A: 15
```

---

### Search 5: Find News Events

**Use Grep:**
```
Pattern: news_event\s*=\s*\{
Path: events/
Output: content
-A: 15
```

---

### Search 6: Find State Events

**Use Grep:**
```
Pattern: state_event\s*=\s*\{
Path: events/
Output: content
-A: 15
```

---

### Search 7: Find Events by Trigger Condition

**Ask for:** Trigger (e.g., "has_war", "date")

**Use Grep:**
```
Pattern: has_war\s*=\s*yes
Path: events/
Output: content
-B: 20
-A: 5
```

---

### Search 8: Find MTTH Events

**Use Grep:**
```
Pattern: mean_time_to_happen\s*=\s*\{
Path: events/
Output: content
-B: 10
-A: 15
```

**Explanation:** Shows events that fire automatically

---

### Search 9: Find Triggered-Only Events

**Use Grep:**
```
Pattern: is_triggered_only\s*=\s*yes
Path: events/
Output: content
-B: 5
-A: 5
```

---

### Search 10: Find Event Chains

**Ask for:** Starting event ID or namespace

**Steps:**
1. Find the initial event
2. Look for `country_event = { id = X }` in options
3. Follow chain to next event
4. Repeat until chain ends

**Use Grep for event triggers:**
```
Pattern: country_event\s*=\s*\{[^}]*id\s*=
Path: events/
Output: content
-B: 25
-A: 5
```

---

### Search 11: Find Events with Specific Picture

**Ask for:** Picture GFX reference

**Use Grep:**
```
Pattern: picture\s*=\s*GFX_report_event_german_troops
Path: events/
Output: content
-B: 5
-A: 10
```

---

### Search 12: Find Events by Option Count

**Find events with multiple options:**
```
Pattern: option\s*=\s*\{
Path: events/
Output: count
```

---

### Search 13: Find Hidden Events

**Use Grep:**
```
Pattern: hidden\s*=\s*yes
Path: events/
Output: content
-B: 5
-A: 20
```

---

### Search 14: Find Events with Timeouts

**Use Grep:**
```
Pattern: timeout_days\s*=\s*\d+
Path: events/
Output: content
-B: 5
-A: 10
```

---

### Search 15: Find Fire-Once Events

**Use Grep:**
```
Pattern: fire_only_once\s*=\s*yes
Path: events/
Output: content
-B: 5
-A: 5
```

---

## Analysis Workflows

### Workflow 1: Analyze Event Chain

**Ask for:** Starting event ID

**Steps:**
1. Find initial event with Grep
2. Note all `country_event` calls in options
3. Search for each triggered event ID
4. Map the chain sequence
5. Report to user

**Report format:**
```
Event Chain: German Anschluss
1. german_events.1 - "Demand Austria" (Player choice)
   → Option A: Send demand → german_events.2
   → Option B: Wait → Chain ends

2. german_events.2 - "Austria Responds" (Austria)
   → Option A: Accept → german_events.3
   → Option B: Refuse → german_events.4

3. german_events.3 - "Austria Accepts" (Germany)
   → Annexation occurs

4. german_events.4 - "Austria Refuses" (Germany)
   → War goal created
```

---

### Workflow 2: Analyze Namespace

**Ask for:** Namespace name

**Steps:**
1. Find all events in namespace
2. Count events
3. Identify event types
4. Note special patterns

**Report:**
```
Namespace: german_events
Total events: 25
Types:
- Country events: 23
- News events: 2

Special properties:
- MTTH events: 3
- Fire-once events: 15
- Hidden events: 2
- Event chains: 4 chains identified
```

---

### Workflow 3: Find Event by Description

**Ask for:** Description text or keyword

**Steps:**
1. Search localization files for keyword
2. Note localization key
3. Search events for that key
4. Report event ID

---

## Common Search Patterns

### Pattern: Find War-Related Events

```
Pattern: (declare_war|has_war|capitulation)
Path: events/
Output: content
-B: 25
```

### Pattern: Find Economic Events

```
Pattern: (add_stability|consumer_goods|industrial_complex)
Path: events/
Output: content
-B: 25
```

### Pattern: Find Diplomatic Events

```
Pattern: (add_opinion_modifier|create_faction|puppet)
Path: events/
Output: content
-B: 25
```

### Pattern: Find Focus-Triggered Events

**In focus files:**
```
Pattern: country_event\s*=\s*\{[^}]*id\s*=
Path: common/national_focus/
Output: content
-B: 10
-A: 5
```

**Then search for those event IDs in events/**

---

## Understanding Event Structure

When you find an event, explain this structure to the user:

```
namespace = event_namespace

country_event = {
    id = event_namespace.1          # Event ID
    title = event_namespace.1.t     # Title localization
    desc = event_namespace.1.d      # Description localization
    picture = GFX_report_event_pic  # Event picture

    # Triggering
    is_triggered_only = yes         # Triggered by effect
    # OR
    trigger = { }                   # Conditions to fire
    mean_time_to_happen = { }       # How often it fires

    # Properties
    fire_only_once = yes            # One-time event
    major = yes                     # For news events
    hidden = yes                    # Invisible event

    # Immediate effects
    immediate = {
        # Effects before event shows
    }

    # Options
    option = {
        name = event_namespace.1.a  # Option text
        # Option effects
        # Trigger next event
        country_event = { id = event_namespace.2 }
    }

    option = {
        name = event_namespace.1.b
        # Different effects
    }
}
```

---

## Response Format

When providing search results, format like this:

**Event Found:** `german_events.5`
**File:** `events/german_events.txt:142`
**Type:** Country event
**Trigger:** Triggered only (called from focus completion)

**Title:** "The Anschluss"
**Description:** Germany has successfully annexed Austria...

**Options:**
1. "Excellent!" (default)
   - Gain 50 political power
   - Gain cores on Austrian states
   - Fire news event world_news.1

**AI Behavior:** No AI factor (only 1 option)

**Chain:** Triggers world_news.1 (news event)

---

## Tips for Users

- Event IDs follow pattern: `namespace.number`
- Namespaces group related events
- `is_triggered_only = yes` means called from effects
- MTTH events fire automatically based on conditions
- `ROOT` = country receiving event
- `FROM` = country that triggered event (if applicable)
- Options must have at least one
- Hidden events run without showing UI
- News events appear for multiple countries

---

## Common Use Cases

**Use Case 1:** "Find the event that fires when Germany completes Anschluss focus"
```
1. Search focus file for "anschluss" completion_reward
2. Note event ID triggered
3. Search for that event ID in events/
```

**Use Case 2:** "What events does the German focus tree trigger?"
```
Search german_focus.txt for "country_event"
List all triggered event IDs
```

**Use Case 3:** "Find all events that give stability"
```
Search: add_stability in events/
```

**Use Case 4:** "Trace the Spanish Civil War event chain"
```
Start with initial event ID
Follow option → country_event triggers
Map entire chain
```

**Use Case 5:** "Find all news events for major wars"
```
Search: news_event.*major = yes
Filter for war-related effects
```

---

## Reference Files

For detailed information, consult:
- `references/event_search_examples.md` - Common search examples
- `references/event_types_guide.md` - Event type explanations

---

## Limitations

- This skill searches existing events, it does not create them
- For creating new events, use hoi4-event-helper skill
- Event chains may span multiple files
- Localization is separate from event code

---

## Tips

- Start with namespace to understand event grouping
- Use -B (before) flag generously to see event IDs
- Event chains require multiple searches to trace
- Check both `complete_effect` and `option` blocks
- Hidden events are used for scripting
- MTTH events need both trigger and mean_time_to_happen
- News events with `major = yes` show to all major powers
- Look in focus/decision files to find what triggers events
