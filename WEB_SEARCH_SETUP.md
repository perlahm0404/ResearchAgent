# Web Search Setup Guide

Your platform supports **4 web search options** with automatic fallback. All have free tiers!

## 🆓 Free Options (Choose 1 or More)

### Option 1: Brave Search API (RECOMMENDED)
**Free Tier**: 2,000 searches/month (ongoing)
**Quality**: Excellent (independent index, privacy-focused)
**Cost**: $0/month

**Setup**:
1. Go to https://brave.com/search/api/
2. Sign up for free account
3. Get your API key
4. Add to `.env`:
   ```bash
   BRAVE_API_KEY=your_brave_api_key_here
   ```

---

### Option 2: Serper API
**Free Tier**: 2,500 searches/month
**Quality**: Excellent (Google results)
**Cost**: $0/month

**Setup**:
1. Go to https://serper.dev
2. Sign up for free account
3. Get your API key
4. Add to `.env`:
   ```bash
   SERPER_API_KEY=your_serper_api_key_here
   ```

---

### Option 3: SearxNG (DEFAULT - Already Configured!)
**Free Tier**: Unlimited
**Quality**: Good (metasearch aggregator)
**Cost**: $0/month

**Setup**: Nothing! Already works out of the box.

Uses public instance: https://searx.be

**Alternative instances**:
- https://searx.info
- https://searx.fmac.xyz
- https://searxng.org (find more instances)

Change in `.env`:
```bash
SEARXNG_URL=https://searx.info
```

---

### Option 4: Tavily API (Premium - Optional)
**Free Tier**: None (paid only)
**Quality**: Excellent (AI-optimized)
**Cost**: $29/month

**Setup** (if you want premium):
1. Go to https://tavily.com
2. Sign up and subscribe
3. Get your API key
4. Add to `.env`:
   ```bash
   TAVILY_API_KEY=your_tavily_api_key_here
   ```

---

## 🎯 Recommended Setup

**Best setup for $0/month**:

```bash
# In your .env file:

# Primary (best quality, 2,000/month free)
BRAVE_API_KEY=your_brave_key

# Backup (2,500/month free)
SERPER_API_KEY=your_serper_key

# Final fallback (unlimited free)
SEARXNG_URL=https://searx.be
```

This gives you **4,500 high-quality searches/month free**, then unlimited via SearxNG!

---

## 🔄 How Priority Works

The system tries APIs in this order:

1. **Brave** (if key provided) → High quality, 2,000/month
2. **Serper** (if key provided) → High quality, 2,500/month
3. **Tavily** (if key provided) → Premium, unlimited
4. **SearxNG** (always available) → Unlimited free

**If one fails, it automatically tries the next!**

---

## ⚙️ Current Configuration

Check your current setup:

```bash
cd ~/personal-knowledge-platform
cat .env | grep -E "BRAVE|SERPER|TAVILY|SEARXNG"
```

---

## 🧪 Testing Web Search

After adding API keys, test in Claude.ai:

```
Search the web for "latest AI trends 2026"
```

I'll tell you which API was used:
- "Found via Brave: ..." → Using Brave API
- "Found via Serper: ..." → Using Serper API
- "Found via SearxNG: ..." → Using free fallback
- "Found via Tavily: ..." → Using premium API

---

## 💰 Cost Comparison

| Option | Monthly Limit | Cost | Quality |
|--------|---------------|------|---------|
| **Brave** | 2,000 searches | **$0** | ⭐⭐⭐⭐⭐ |
| **Serper** | 2,500 searches | **$0** | ⭐⭐⭐⭐⭐ |
| **SearxNG** | Unlimited | **$0** | ⭐⭐⭐⭐ |
| Tavily | Unlimited | $29 | ⭐⭐⭐⭐⭐ |

**Recommended**: Use Brave + Serper + SearxNG = **4,500+ searches/month for $0**

---

## 🚀 Quick Start (5 Minutes)

### Get Brave API Key (Best Free Option)

1. **Sign up**: https://brave.com/search/api/
2. **Get API key** from dashboard
3. **Add to .env**:
   ```bash
   cd ~/personal-knowledge-platform
   nano .env
   # Add line: BRAVE_API_KEY=bsa_xxxxxxxxxxxxx
   # Save: Ctrl+O, Enter, Ctrl+X
   ```
4. **Restart MCP server** (or just use Claude - it auto-restarts)
5. **Test**: Ask me "Search web for test query"

That's it! You now have 2,000 high-quality searches/month for free.

---

## 🛡️ Privacy Comparison

| API | Privacy Level | Notes |
|-----|---------------|-------|
| **Brave** | ⭐⭐⭐⭐⭐ | Privacy-focused, independent index |
| **SearxNG** | ⭐⭐⭐⭐⭐ | No tracking, metasearch |
| **Serper** | ⭐⭐⭐ | Proxies Google, API-level tracking |
| Tavily | ⭐⭐⭐ | API-level tracking, AI-optimized |

**Most private**: Brave or SearxNG

---

## 📊 Usage Monitoring

### Check Brave Usage
Dashboard: https://brave.com/search/api/dashboard

### Check Serper Usage
Dashboard: https://serper.dev/dashboard

### SearxNG
No tracking, no limits, no monitoring needed!

---

## ❓ FAQ

**Q: Which API should I use?**
A: **Brave** for best free tier (2,000/month). Add Serper for backup (2,500/month). SearxNG always works as unlimited fallback.

**Q: Do I need all of them?**
A: No! SearxNG works without any API keys. Add Brave for better quality.

**Q: What happens when I hit the limit?**
A: System automatically falls back to next available API. Brave (2,000) → Serper (2,500) → SearxNG (unlimited).

**Q: Is Tavily worth $29/month?**
A: Only if you need >4,500 searches/month AND want premium quality. Otherwise, free options are excellent.

**Q: Can I self-host?**
A: Yes! Run your own SearxNG instance: https://github.com/searxng/searxng

**Q: Which gives best results?**
A: Brave and Serper have excellent quality. SearxNG is very good for a free aggregator.

---

## 🎉 You're All Set!

With Brave + Serper + SearxNG configured, you have:

✅ 4,500+ high-quality searches/month
✅ Unlimited fallback via SearxNG
✅ Automatic failover
✅ $0/month cost
✅ Privacy-focused

**Start searching!**
