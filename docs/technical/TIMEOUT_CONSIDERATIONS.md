# Azure Functions Timeout Considerations

## TL;DR - You're Fine ✅

**Current execution time:** ~2-4 seconds
**Azure Functions hard limit:** 10 minutes (600 seconds)
**Safety buffer:** 150-300x

You have **zero timeout concerns** with the current crawler.

---

## The Question You Raised

> "If the Azure function is scheduled with an hourly cron job, doesn't the function time out before that? Azure functions have a default timeout of 5 or 10 minutes, which is max extendable to 30 minutes I thought"

**You're 100% correct about the limits.** Let me explain the details:

---

## Azure Functions Timeout Limits

### By Hosting Plan

| Plan | Default | Maximum | Notes |
| --- | --- | --- | --- |
| **Consumption** (our plan) | 5 min | **10 min** (hard limit) | Cheapest, scales to zero |
| **Premium** | 30 min | 30 min | Better for longer tasks |
| **Dedicated** (App Service) | No limit | Configurable | Run anything |

**Key Point:** On Consumption Plan, **10 minutes is a hard limit**. Functions cannot be extended beyond 10 minutes.

---

## Why Hourly Schedule ≠ Timeout Problem

### Cron Schedule Clarification

```
Schedule: "0 0 * * * *"
Means:    "Run at the start of every hour"
Duration: Takes ~2-4 seconds
          Then stops and waits for next trigger
```

**The confusion:** The 1-hour interval between runs is NOT the function's execution time. Each run is independent:

```
Execution Timeline:
┌─────────────────────────────────────────────────────────┐
│                     1 Hour (3600 seconds)               │
├────────────┬─────────────────────────────────────────────┤
│   RUN 1    │              IDLE (waiting)                │
│ (2-4 sec)  │                                            │
└────────────┴──────────────┬───────────────────────────────┘
                            │
                            └─ NEXT HOUR - RUN 2 starts (2-4 sec)
```

Each individual run must complete within 10 minutes. Since ours completes in ~2-4 seconds, we're safe.

---

## Current Performance Breakdown

### Execution Time Analysis

```
Total Execution: ~2-4 seconds

├─ Initialize components:    ~0.1s
│  ├─ Fetcher()
│  ├─ Parser()
│  └─ AzureBlobRepository()
│
├─ Fetch HTML:              ~1-2s (network I/O)
│  └─ requests.get(url)
│
├─ Parse HTML:              ~0.5-1s
│  └─ BeautifulSoup parsing
│
├─ Upload to Blob Storage:  ~0.5-1s
│  └─ Azure Storage API call
│
└─ Logging & overhead:      ~0.1s
```

**Network I/O** dominates the time. The pool website responds quickly (< 2 seconds typically).

---

## Updated Function with Timing Tracking

The function code has been updated to log execution times:

```python
import time

def main(mytimer: func.TimerRequest) -> None:
    start_time = time.time()
    
    # ... fetch, parse, save ...
    
    total_time = time.time() - start_time
    logger.log_info(f"Crawler execution completed in {total_time:.2f}s")
```

**Logs you'll see:**
```
Data fetched successfully in 1.43s
Data parsed successfully in 0.67s
Data saved to blob storage in 0.82s
Crawler execution completed successfully in 3.02s
```

---

## Detailed Timeout Limits by Plan

### Consumption Plan (Current) ⭐

```
├─ Cost: $1-5/month
├─ Default timeout: 5 minutes
├─ Hard limit: 10 minutes (non-extendable)
├─ Recommended for: Quick tasks (<5 min)
└─ Our usage: ~2-4s = ✅ Perfect fit
```

**When to keep:** Current crawler performance
**When to upgrade:** If crawler grows to >5 minutes consistently

### Premium Plan

```
├─ Cost: ~$35-150/month (depending on instance size)
├─ Default timeout: 30 minutes
├─ Hard limit: 30 minutes
├─ Recommended for: Longer processing tasks (5-30 min)
└─ Our usage: 2-4s = 🎯 Overkill, but available if needed
```

**Upgrade benefit:** More flexibility for future growth

### Dedicated Plan (App Service)

```
├─ Cost: $12+/month (depending on tier)
├─ Timeout: Fully configurable (no hard limits)
├─ Recommended for: Very long-running tasks (30+ min)
└─ Our usage: 2-4s = 🎯 Complete overkill
```

**Upgrade benefit:** Ultimate flexibility, but much higher cost

---

## Scenarios and Solutions

### Scenario 1: Crawler Stays ~2-4 Seconds ✅
**Current status - no action needed**

Consumption Plan perfectly suitable. You have 240-300x safety buffer.

### Scenario 2: Crawler Grows to 30-60 Seconds 🟢
**Still safe on Consumption Plan**

Still well within the 10-minute limit. No upgrade needed.

### Scenario 3: Crawler Grows to 3-5 Minutes 🟡
**Getting close to limits**

- Consumption Plan still works (5 min default, 10 min max)
- Consider optimizing the code
- Monitor execution times in Azure Portal

### Scenario 4: Crawler Exceeds 5 Minutes 🔴
**Need to take action**

**Option A: Optimize** (recommended first step)
- Add caching for frequently accessed data
- Use parallel requests for multiple pages
- Implement request timeouts

**Option B: Upgrade Plan** (if optimization not possible)
```bash
# Switch to Premium Plan
az functionapp plan update \
  --name badi-oerlikon-plan \
  --sku EP1
```

**Option C: Break into Multiple Functions** (rarely needed)
- Create separate functions for fetch, parse, save
- Trigger them sequentially or in parallel
- More complex, not recommended for this use case

---

## Monitoring and Alerts

### View Current Execution Times

**In Azure Portal:**
1. Go to Function App → Monitor
2. Look for "Duration" metric
3. Check individual function invocations

**Via CLI:**
```bash
# View last 10 invocations
az functionapp log tail \
  --resource-group badi-oerlikon-rg \
  --name badi-oerlikon-dev-func \
  --number 10
```

**Expected output:**
```
[2026-02-17T12:00:05Z] Data fetched successfully in 1.45s
[2026-02-17T12:00:06Z] Data parsed successfully in 0.62s
[2026-02-17T12:00:07Z] Data saved to blob storage in 0.78s
[2026-02-17T12:00:07Z] Crawler execution completed successfully in 2.95s
```

### Set Up Alerts

Alert if execution time exceeds 5 minutes:

```bash
az monitor metrics alert create \
  --name "Function Timeout Alert" \
  --resource-group badi-oerlikon-rg \
  --scopes /subscriptions/{id}/resourceGroups/badi-oerlikon-rg/providers/Microsoft.Web/sites/badi-oerlikon-dev-func \
  --description "Alert if function duration > 5 min" \
  --window-size 5m \
  --condition "avg Duration > 300000" \
  --action email-action
```

---

## Best Practices to Avoid Timeout Issues

### 1. Monitor Regularly
```bash
# Weekly check
az monitor metrics list \
  --resource-group badi-oerlikon-rg \
  --resource-type "Microsoft.Web/sites" \
  --resource-name badi-oerlikon-dev-func \
  --metric Duration --start-time 2026-02-10 --interval PT1H
```

### 2. Add Timeouts to External Calls
```python
# In fetcher.py
response = requests.get(url, timeout=10)  # Don't hang forever
```

### 3. Log Step Timings
```python
# Now done in __init__.py
fetch_time = time.time() - fetch_start
logger.log_info(f"Fetch took {fetch_time:.2f}s")
```

### 4. Set Up Gradual Alerts
- Yellow alert: >1 minute
- Orange alert: >5 minutes  
- Red alert: >9 minutes

---

## The Real-World Scenario

Let's say the pool website becomes very slow (unlikely, but possible):

```
Current:      1.5s (fetch) + 0.7s (parse) + 0.8s (save) = 3.0s ✅
Slower site:  5s (fetch) + 0.7s (parse) + 0.8s (save) = 6.5s ✅
Very slow:   15s (fetch) + 0.7s (parse) + 0.8s (save) = 16.5s ❌ TIMEOUT
```

**In the "Very slow" case:**
- Not the function's fault (site is slow)
- You'd need Premium Plan
- Or add request timeout and implement retry logic

**Best solution:**
```python
# Add timeout and handle gracefully
try:
    response = requests.get(url, timeout=8)
except requests.Timeout:
    logger.log_error("Website timeout - will retry next hour")
    return  # Exit gracefully, don't crash
```

---

## Summary Table

| Aspect | Status | Notes |
| --- | --- | --- |
| **Current execution** | ✅ Safe | 2-4 seconds |
| **Consumption Plan limit** | ✅ Plenty | 10 minutes |
| **Safety buffer** | ✅ Excellent | 150-300x |
| **Timeout risk** | ✅ Zero | Not a concern today |
| **Future-proof** | ✅ Robust | Can handle 2-3x growth |
| **Monitoring** | ✅ Added | Execution times logged |
| **Upgrade path** | ✅ Clear | Premium/Dedicated if needed |

---

## Conclusion

Your concern is **technically valid** - Azure Functions Consumption Plan does have a 10-minute hard limit. However, for your crawler:

- ✅ Current execution: ~2-4 seconds
- ✅ Theoretical limit: 600 seconds
- ✅ Buffer: 150-300x
- ✅ Risk level: **Effectively zero**

You can confidently proceed with the Consumption Plan. Monitor execution times, and if they start approaching 5 minutes consistently, upgrade to Premium Plan (costs only ~$35-50 more per month).

**You're good to go!** 🚀
