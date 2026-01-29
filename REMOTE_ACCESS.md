# Remote Access Guide

How to use your ResearchAgent from anywhere (phone, tablet, other computers).

## 🎯 Current Setup: Local Only

Your ResearchAgent currently runs **only on your Mac**:
- MCP server connects to Claude Desktop (local app)
- PostgreSQL runs in Docker (localhost)
- Documents stored locally
- No remote access

---

## 📱 4 Ways to Access from Phone

### Option 1: Remote Desktop (Easiest - No Code Changes)

**Access your Mac remotely, use Claude Desktop as normal**

#### Setup (10 minutes):

1. **On Mac - Enable Screen Sharing**:
   ```bash
   # System Settings → General → Sharing → Screen Sharing → ON
   # Or enable via command line:
   sudo /System/Library/CoreServices/RemoteManagement/ARDAgent.app/Contents/Resources/kickstart -activate -configure -access -on -restart -agent -privs -all
   ```

2. **Install Tailscale (Recommended for security)**:
   ```bash
   brew install tailscale
   # Start and login
   sudo tailscale up
   # Get your Mac's Tailscale IP
   tailscale ip -4
   ```

3. **On Phone - Install Remote Desktop App**:
   - iOS: [Jump Desktop](https://apps.apple.com/app/jump-desktop-rdp-vnc/id364876095)
   - iOS: [Screens](https://apps.apple.com/app/screens-vnc-remote-desktop/id655890150)
   - Android: [Jump Desktop](https://play.google.com/store/apps/details?id=com.p5sys.android.jump)

4. **Connect**:
   - Open app on phone
   - Add new connection: Your Mac's IP (or Tailscale IP)
   - Login with Mac credentials
   - Open Claude Desktop
   - Use ResearchAgent normally!

**Pros**:
- ✅ No code changes needed
- ✅ Full Mac access
- ✅ Works immediately
- ✅ Secure with Tailscale

**Cons**:
- ⚠️ Mac must stay on
- ⚠️ Small screen experience
- ⚠️ Needs good internet

---

### Option 2: Cloud Deployment + Claude.ai Web (Advanced)

**Deploy backend to cloud, use Claude.ai website on phone**

This requires converting MCP to REST API and deploying to cloud.

#### Architecture:
```
Phone → Claude.ai Web → MCP Over HTTP → Cloud Backend
                                             ↓
                                    Cloud PostgreSQL
                                             ↓
                                    Cloud Storage (S3)
```

#### Setup (1-2 hours):

**1. Convert MCP to HTTP Server**:

Would need to create `backend/api_server.py`:
```python
from fastapi import FastAPI
from mcp import create_http_server

app = FastAPI()

# Expose MCP tools as REST endpoints
@app.post("/api/search_knowledge_base")
async def search_kb(query: str, top_k: int = 5):
    # Call existing search logic
    pass

@app.post("/api/web_search")
async def web_search(query: str, num_results: int = 5):
    # Call existing web search
    pass

# ... 7 more endpoints
```

**2. Deploy to Cloud**:

Options:
- **Railway** (easiest): https://railway.app
- **Fly.io**: https://fly.io
- **Render**: https://render.com
- **DigitalOcean App Platform**: https://www.digitalocean.com/products/app-platform

Example Railway deployment:
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
cd ~/personal-knowledge-platform
railway init
railway up
```

**3. Use Claude.ai Web with API**:

Currently, Claude.ai web doesn't support custom MCP servers directly. You'd need to:
- Use Claude API directly (requires API key, costs money)
- OR wait for Claude.ai web to support remote MCP servers

**Pros**:
- ✅ Access from any device
- ✅ No Mac needed
- ✅ Always available

**Cons**:
- ⚠️ Requires cloud costs ($10-50/mo)
- ⚠️ Requires code changes (REST API)
- ⚠️ More complex setup
- ⚠️ Documents in cloud (less private)

---

### Option 3: Tailscale + Wake-on-LAN (Best Balance)

**Access your Mac from anywhere, wake it when needed**

#### Setup (30 minutes):

**1. Install Tailscale on Mac**:
```bash
brew install tailscale
sudo tailscale up
```

**2. Enable Wake-on-LAN on Mac**:
```bash
# System Settings → Energy Saver → Wake for network access
sudo systemsetup -setwakeonnetworkaccess on

# Get Mac's Tailscale IP
tailscale ip -4
# Save this IP: e.g., 100.64.1.2
```

**3. Install Tailscale on Phone**:
- iOS: [Tailscale](https://apps.apple.com/app/tailscale/id1470499037)
- Android: [Tailscale](https://play.google.com/store/apps/details?id=com.tailscale.ipn)

**4. Setup Wake Script**:

On Mac, create wake script:
```bash
cat > ~/wake_mac.sh <<'EOF'
#!/bin/bash
# This keeps Mac awake when accessed remotely
caffeinate -d &
EOF
chmod +x ~/wake_mac.sh
```

**5. Connect from Phone**:
- Open Tailscale app on phone → Connect
- Open Jump Desktop → Add Mac using Tailscale IP
- Mac wakes up automatically
- Use Claude Desktop normally

**Pros**:
- ✅ Secure (Tailscale VPN)
- ✅ No code changes
- ✅ Access from anywhere
- ✅ Auto-wake Mac

**Cons**:
- ⚠️ Mac must be plugged in
- ⚠️ Need good home internet

---

### Option 4: Claude Mobile App + Future MCP Support (Wait)

**Use Claude mobile app when it supports MCP**

Currently, Claude mobile app doesn't support MCP servers. This may come in future updates.

**Status**: ❌ Not available yet

**When available**:
- Install Claude mobile app
- Configure remote MCP endpoint
- Use ResearchAgent from phone

---

## 🎯 Recommended Approach

**For immediate use**: **Option 1 or 3**

### Quick Start (Option 1 - Remote Desktop):

**5-Minute Setup**:

1. **Mac setup**:
   ```bash
   brew install tailscale
   sudo tailscale up
   tailscale ip -4  # Save this IP
   ```

2. **Enable Screen Sharing**:
   - System Settings → General → Sharing
   - Turn on "Screen Sharing"

3. **Phone setup**:
   - Install Tailscale app
   - Connect to your Tailscale network
   - Install Jump Desktop or Screens
   - Add connection with Tailscale IP from step 1
   - Connect!

4. **Use Claude Desktop** on your Mac remotely from phone

**Done!** You can now use ResearchAgent from anywhere.

---

## 💰 Cost Comparison

| Option | Monthly Cost | Setup Time | Mac Required |
|--------|--------------|------------|--------------|
| **Remote Desktop** | **$0** | 10 min | Yes (on) |
| **Tailscale + Wake** | **$0** | 30 min | Yes (wake) |
| Cloud Deployment | $10-50 | 2 hours | No |
| Claude Mobile MCP | $0 | N/A | No |

**Best value**: Option 1 or 3 (both free!)

---

## 🔒 Security Best Practices

### For Remote Desktop:

1. **Use Tailscale** (not public internet):
   ```bash
   brew install tailscale
   sudo tailscale up
   ```

2. **Enable Firewall**:
   ```bash
   # System Settings → Network → Firewall → ON
   sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on
   ```

3. **Use Strong Mac Password**:
   - System Settings → Touch ID & Password
   - Change to strong password

4. **Enable FileVault** (disk encryption):
   - System Settings → Privacy & Security → FileVault → ON

### For Cloud Deployment:

1. Use environment variables for secrets
2. Enable HTTPS only
3. Use authentication tokens
4. Restrict API access by IP
5. Encrypt data at rest

---

## 📋 Troubleshooting

### Can't connect from phone

**Check**:
```bash
# On Mac - verify Tailscale is running
tailscale status

# Check Screen Sharing is enabled
sudo /System/Library/CoreServices/RemoteManagement/ARDAgent.app/Contents/Resources/kickstart -status

# Test connection from Mac terminal
ping $(tailscale ip -4)
```

### Mac won't wake

**Enable Wake-on-LAN**:
```bash
sudo systemsetup -setwakeonnetworkaccess on
# Keep Mac plugged into power
```

### Poor performance

**Optimize**:
- Lower screen resolution in remote desktop app
- Use Tailscale for better routing
- Ensure Mac has good internet connection
- Close unnecessary apps on Mac

---

## 🚀 Quick Commands

### Setup Tailscale (Recommended)
```bash
# On Mac
brew install tailscale
sudo tailscale up
tailscale ip -4  # Save this IP

# On phone: Install Tailscale app, login, connect
```

### Enable Screen Sharing
```bash
# On Mac
sudo systemsetup -setremotelogin on
```

### Get Mac IP Address
```bash
# Local IP (WiFi)
ipconfig getifaddr en0

# Tailscale IP (recommended)
tailscale ip -4

# Public IP (not recommended)
curl ifconfig.me
```

---

## 🎉 Summary

**To use ResearchAgent from your phone TODAY**:

1. ✅ Install Tailscale on Mac + Phone (5 min)
2. ✅ Enable Screen Sharing on Mac (1 min)
3. ✅ Install Jump Desktop on Phone (2 min)
4. ✅ Connect from phone to Mac (2 min)
5. ✅ Use Claude Desktop remotely

**Total setup time**: 10 minutes
**Monthly cost**: $0
**Works**: Immediately

**Start here**: https://tailscale.com/download

---

## 📚 Additional Resources

- Tailscale setup: https://tailscale.com/kb/
- Jump Desktop guide: https://jumpdesktop.com/guides/
- Wake-on-LAN guide: https://support.apple.com/guide/mac-help/wake-your-mac-automatically-mchl40376151/mac
- Secure remote access: https://tailscale.com/blog/how-tailscale-works/

---

**Next Step**: Choose an option above and follow the setup guide!
