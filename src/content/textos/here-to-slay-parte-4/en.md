---
titulo: 'Here To Slay, part 4: Kafka Streams and in-game achievements'
data: 2026-11-05
resumo: A service that only watches matches and turns patterns into alerts like First Blood and Combo, using time windows, state stores and even Allen's interval algebra.
tags: [tecnico, kafka]
projeto: here-to-slay
ordem: 4
---

In [part 3](/en/writing/here-to-slay-parte-3/), Here To Slay became a set of services that only talk through Kafka topics. That was the first stage of the Event-Driven Systems course project. The second stage asked for something different: using **Kafka Streams** to process the events already flowing through the system and get information out of them.

We turned that into a game feature: a service that watches matches and hands out "achievements" to players. If someone slays the first monster, everyone gets a **First Blood** notice. If you make three moves in six seconds, you earn a **Combo** badge. Gianluca built the first version of the topology, and I came in later with the event stream, the badges and the action history.

## A service that only watches

The most important decision came before any code: monitoring would be a **separate, read-only service**. It consumes the two topics the engine already uses, `game-actions-in` (what players ask for) and `game-state-out` (what the engine decides), and never writes back to them. The only place it produces to is a new topic, `game-monitoring-alerts`.

![Monitoring service topology: it reads game-actions-in and game-state-out, applies three kinds of processing and only produces to game-monitoring-alerts, which the gateway forwards to the players](./streams-topologia.en.svg)

That has a great consequence: if the topology has a bug, or if the service goes down, **the match carries on as usual**. Worst case, nobody gets the badge. Monitoring can evolve freely without any fear of breaking the game.

The way back reuses what already existed. The gateway consumes `game-monitoring-alerts` and delivers each alert over WebSocket. Some alerts go to the whole match, and to know who is in it the gateway keeps a cache of each match's players, fed by the compacted `match-state-store` topic from part 3.

## Three ways to process an event

There are ten detected situations, and they fall into three categories, each one showing off a different Kafka Streams feature.

**1. Stateless.** Some situations depend on a single event. **Generous Soul** fires when someone plays a positive Modifier on *another* player's roll. All it takes is looking at the message and deciding, so it's just a `filter` and a `map`:

```java
actionsIn
    .filter((key, value) -> isGenerousModifier(value))
    .map((key, value) -> KeyValue.pair(key, MonitoringAlert.generousSoul(actorOf(value))))
    .to("game-monitoring-alerts");
```

**2. Time windows.** Other situations depend on *how many times* something happened within a period. **Combo** is the simplest example: three actions by the same player in six seconds. The key becomes `matchId|playerId`, and messages are grouped by that key and counted inside a time window:

```java
actionsIn
    .map((key, value) -> KeyValue.pair(key + "|" + actorOf(value), value))
    .groupByKey()
    .windowedBy(TimeWindows.ofSizeAndGrace(Duration.ofSeconds(6), Duration.ZERO))
    .count()
    .toStream()
    .filter((windowedKey, count) -> count == 3)
```

The `count == 3` filter makes the alert fire only once, right when the third action arrives. Attack focus (30 s), chain effect (35 s) and Focusing (2 min) follow the same recipe, with different windows and keys.

One detail I only noticed while going back through the code: all of these windows are *tumbling*, meaning fixed, non-overlapping blocks of time. If a combo's three actions land half at the end of one window and half at the start of the next, the combo doesn't count. A sliding window would fix that, at the cost of more state. For a just-for-fun badge, the current behavior is acceptable, but it's the kind of choice worth knowing you made.

**3. The Processor API with a state store.** Some situations need a richer memory than a count, and that's where the Processor API comes in: a hand-written processor with its own *state store*. **First Blood** is the simplest of them. It remembers, per match, whether someone has already slain a monster:

```java
if (firstBloodStore.get(matchId) != null) return;   // this match already had its first blood
firstBloodStore.put(matchId, playerId);
context.forward(new Record<>(matchId, MonitoringAlert.firstBlood(playerId), record.timestamp()));
```

**Frequent Buyer** (six card draws in a row), **RNG Diff** (three attacks on a monster without slaying it) and the match's **last 25 actions history** use the same idea, each with its own store.

The stores live in memory. That sounds risky, but Kafka Streams keeps a *changelog topic* behind every store. If the service restarts, it rebuilds its state from that topic. It's the same topic-as-a-database idea from part 3, except here the framework does the work for you.

## The nerdiest situation: Allen's algebra

The **luck turnaround** was the most fun to build. The idea is to detect when two players' luck crosses: while one is on a streak of good rolls, the other's streak ends, for example.

Each player has a current streak, which is a time interval `[start, end)` of type **HOT** (successful rolls) or **COLD** (failed rolls). Every roll extends the open streak or, if the result flipped, closes the current one and opens a new one.

To compare two streaks, I used **Allen's interval algebra**, which defines exactly 13 ways two intervals can relate in time:

![Allen's 13 relations between two intervals A and B. Nine of them, where the intervals overlap, trigger the alert; BEFORE, MEETS, MET_BY and AFTER don't](./allen.en.svg)

When a player's streak closes, the processor compares that interval with each rival's still-open streak. If the relation is one of the nine where the intervals actually overlap, the two players' luck crossed in time, and the game tells everyone. If one interval simply comes before the other (`BEFORE`, `MEETS`, `MET_BY`, `AFTER`), there's no turnaround at all. The whole classification fits in a sequence of comparisons between starts and ends:

```java
if (ae < bs) return BEFORE;
if (ae == bs) return MEETS;
if (as == bs && ae == be) return EQUALS;
if (as > bs && ae < be) return DURING;
// ... and so on, up to all 13 relations
```

## What changed along the way

The topology wasn't born like this. Two changes tell its evolution well:

- **A join that became a history.** The first version of situation 1 was a *join* between `game-actions-in` and `game-state-out`, over a 2-second window, pairing each action with its result. It worked, but all it produced was a generic "action processed" notice. We replaced it with a processor that keeps the match's last 25 actions and sends the whole list, which became a history panel on the game screen. We went from a join to an aggregation with a state store, and the feature got a lot more useful.
- **A situation that went away.** There was a "stalled match" alert, with a *session window* that detected 60 seconds without any action. It didn't make it into the final version.

For me, that was the most interesting lesson of this stage: with events already flowing through Kafka, building a new feature became a matter of **reading what already exists** in a different way, without touching a single line of the engine. And that only works because of the architecture from part 3.

That wraps up the story of how Here To Slay got here. There's still stuff on the list, starting with the match recovery that's still missing. When it ships, it'll be the topic of the next part.
