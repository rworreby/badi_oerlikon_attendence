# Quick Reference: Timeout & Performance

## Your Concern

> "Azure functions have a default timeout of 5 or 10 minutes, which is max extendable to 30 minutes"

**Status:** ✅ **Not a concern for your crawler**

---

## The Facts

### Azure Functions Timeout Limits

- **Consumption Plan** (your plan): 10 minute hard limit
- **Premium Plan**: 30 minute limit
- **Dedicated Plan**: Configurable (unlimited)

### Your Crawler Performance

- **Current execution time:** ~2-4 seconds
- **Safety buffer:** 150-300x the timeout limit
- **Risk level:** **Zero** 🟢

---

## In Plain English

```text

Every hour at :00 seconds...

Hour 1:  Function runs for ~3 seconds → completes → waits 59m 57s
Hour 2:  Function runs for ~3 seconds → completes → waits 59m 57s
Hour 3:  Function runs for ~3 seconds → completes → waits 59m 57s
...

```text

Each 3-second execution is well within the 10-minute (600-second) limit.

---

## Why It's Fine

| Metric | Value | Status |
| --- | --- | --- |
| Execution time | ~3-4s | ✅ |
| Hard limit | 600s (10 min) | ✅ |
| Safety margin | 150-200x | ✅ |
| Current risk | None | ✅ |

---

## When to Worry

**Upgrade needed when:** Execution time consistently exceeds **5-6 minutes**

**Current path:** Not until crawling grows by 100-150x 🎯

---

## What to Do

### Nothing (immediate)

Your setup is rock-solid. No changes needed.

### Monitor (good practice)

```bash

# Check execution times monthly

az functionapp log tail \
  --resource-group badi-oerlikon-rg \
  --name badi-oerlikon-dev-func \
  --number 50

```text

Look for lines like:

```text

Crawler execution completed successfully in 3.02s

```text

### Upgrade Path (if needed later)

```bash

# Costs ~$35-50/month extra for Premium Plan

az functionapp plan update \
  --name badi-oerlikon-plan \
  --sku EP1

```text

---

## TL;DR

✅ You're fine.
✅ No action needed.
✅ Monitor occasionally.
✅ Sleep well at night.

**See:** `TIMEOUT_CONSIDERATIONS.md` for full details.
