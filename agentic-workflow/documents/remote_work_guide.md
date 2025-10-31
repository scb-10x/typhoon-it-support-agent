# Remote Work IT Guide

## Introduction

This guide provides IT best practices and procedures for employees working remotely. Following these guidelines ensures secure and productive remote work.

---

## 1. Initial Remote Work Setup

### Before You Start Working Remotely

**Hardware Checklist:**
- [ ] Company laptop with charger
- [ ] VPN credentials configured
- [ ] Headset with microphone
- [ ] Webcam (if laptop doesn't have one)
- [ ] Mouse and keyboard (optional but recommended)
- [ ] Stable internet connection (minimum 10 Mbps)

**Software Checklist:**
- [ ] VPN client installed (Cisco AnyConnect)
- [ ] Microsoft Teams installed and configured
- [ ] Outlook configured with company email
- [ ] OneDrive for Business syncing
- [ ] All required business applications installed
- [ ] Antivirus and security software up to date

**Network Requirements:**
- Download speed: Minimum 10 Mbps (25 Mbps recommended)
- Upload speed: Minimum 5 Mbps (10 Mbps recommended)
- Stable connection with low latency
- WiFi router WPA2/WPA3 encryption enabled

---

## 2. VPN Connection

### Why VPN is Mandatory

VPN (Virtual Private Network) creates a secure, encrypted tunnel between your device and company network. **NEVER access company resources without VPN when working remotely.**

### Connecting to VPN

**Step-by-Step Instructions:**

1. **Launch VPN Client**
   - Open Cisco AnyConnect
   - Or find it in system tray (Windows) / menu bar (Mac)

2. **Enter VPN Gateway**
   - Server address: `vpn.company.com`
   - This should be pre-configured

3. **Login Credentials**
   - Username: Your company username
   - Password: Your company password
   - MFA Code: From Authenticator app

4. **Connection Status**
   - Wait for "Connected" status
   - Lock icon should appear in system tray
   - You'll see notification: "VPN Connection Established"

5. **Verify Connection**
   - Check VPN client shows "Connected"
   - Test access to internal resources
   - Access should work normally

### VPN Troubleshooting

**Problem: Cannot Connect to VPN**
- Check internet connection first
- Verify credentials are correct
- Ensure MFA device is accessible
- Try different VPN server if available
- Restart VPN client
- Restart computer if needed

**Problem: VPN Keeps Disconnecting**
- Check internet stability
- Move closer to WiFi router
- Try wired connection if possible
- Update VPN client
- Contact IT if problem persists

**Problem: Slow Connection on VPN**
- Expected slight slowdown
- Close unnecessary applications
- Try different VPN server
- Check internet speed (speedtest.net)
- Restart router

**Problem: Authentication Fails**
- Verify password hasn't expired
- Check MFA device time sync
- Reset MFA if needed
- Contact IT helpdesk

### VPN Best Practices

**DO's:**
- ✅ Connect to VPN before accessing any company resources
- ✅ Keep VPN connected throughout work session
- ✅ Verify connection status periodically
- ✅ Use VPN on any public WiFi
- ✅ Report connection issues promptly

**DON'Ts:**
- ❌ Disconnect VPN to speed up personal browsing
- ❌ Share VPN credentials
- ❌ Use personal VPN simultaneously
- ❌ Access company data without VPN
- ❌ Bypass VPN for convenience

---

## 3. Secure Home Network Setup

### WiFi Security

**Essential Settings:**

1. **Change Default Router Password**
   - Access router admin panel
   - Change default admin password
   - Use strong, unique password

2. **Enable Strong Encryption**
   - Use WPA3 (or WPA2 minimum)
   - Never use WEP or open network
   - Disable WPS (WiFi Protected Setup)

3. **Change Default SSID**
   - Don't broadcast router model
   - Use non-identifying name
   - Example: Use "HomeNetwork" not "SmithFamily"

4. **Hide SSID (Optional)**
   - Prevents casual discovery
   - Not foolproof but adds layer

5. **Enable Router Firewall**
   - Should be on by default
   - Verify in router settings
   - Keep firmware updated

6. **Guest Network**
   - Create separate guest network
   - For visitors and IoT devices
   - Isolate from main network

### Network Best Practices

**Recommended:**
- Use wired Ethernet for desktop
- Place router in central location
- Keep router firmware updated
- Restart router weekly
- Use quality router (not ISP provided if possible)

**Security Tips:**
- Don't share WiFi password widely
- Change password every 6 months
- Monitor connected devices regularly
- Disable remote management
- Use strong router admin password

---

## 4. Secure Communication

### Video Conferencing

**Microsoft Teams Best Practices:**

**Before Meeting:**
- Test camera and microphone
- Choose quiet, private location
- Check lighting (face should be visible)
- Close unnecessary applications
- Ensure stable internet connection

**During Meeting:**
- Mute when not speaking
- Use headset to prevent echo
- Enable video when appropriate
- Be mindful of background
- Use blur or virtual background if needed

**Screen Sharing:**
- Close sensitive information before sharing
- Share specific window, not entire screen
- Close email and messaging apps
- Check notifications are muted
- Stop sharing when done

**Meeting Security:**
- Don't share meeting links publicly
- Use waiting room for external meetings
- Verify participants before starting
- Lock meeting once everyone joined
- Record with consent only

### Email Security While Remote

**Be Extra Vigilant:**
- Phishing attempts increase with remote work
- Verify sender before clicking links
- Don't download unexpected attachments
- Check email domain carefully
- When in doubt, call to verify

**Sending Sensitive Information:**
- Encrypt confidential emails
- Use secure file sharing (OneDrive)
- Don't email passwords
- Set expiration on shared links
- Verify recipient before sending

### Instant Messaging

**Teams Chat Guidelines:**
- Use Teams for work communication
- Avoid sharing sensitive data in chat
- Use voice/video for complex discussions
- Set status appropriately (Available, Busy, Away)
- Respond within reasonable timeframe

**What NOT to Share:**
- Passwords
- Credit card numbers
- Social Security numbers
- Confidential client data
- Personally identifiable information

---

## 5. Data Management for Remote Work

### Cloud Storage

**Approved Services:**
- OneDrive for Business
- SharePoint
- Microsoft Teams file storage
- Company approved cloud services

**File Organization:**
- Save work files to OneDrive
- Use SharePoint for team collaboration
- Organize with clear folder structure
- Use descriptive file names
- Enable AutoSave in Office apps

### File Sync

**OneDrive for Business:**
- Install desktop app
- Configure sync folders
- Verify sync status regularly
- Check for sync errors
- Files available offline

**Best Practices:**
- Don't save to local Documents folder
- Use OneDrive for all work files
- Verify sync before logging off
- Don't sync personal files
- Monitor storage quota

### Backup

**What's Automatically Backed Up:**
- OneDrive files (automatic)
- Outlook email (on server)
- Teams conversations (on server)
- SharePoint documents (automatic)

**What You Should Backup:**
- Browser bookmarks
- Application settings
- Local databases (if applicable)
- PST files (if using local archive)

**Backup Best Practices:**
- Verify OneDrive sync working
- Don't rely on local backups only
- Test restore periodically
- Keep important files in cloud
- Report backup issues immediately

---

## 6. Physical Security at Home

### Workspace Security

**Location:**
- Private area if possible
- Away from windows/public view
- Separate from personal space
- Good lighting
- Ergonomic setup

**Device Security:**
- Lock screen when stepping away (Windows + L)
- Auto-lock after 5 minutes
- Don't leave laptop unattended
- Store laptop securely when not in use
- Cable lock for added security

**Visual Privacy:**
- Privacy screen filter recommended
- Position screen away from windows
- Be aware of video call backgrounds
- Don't work in public areas of home when handling sensitive data

### Visitors and Family

**Best Practices:**
- Don't let others use work laptop
- Lock screen during family activities
- Store work devices out of reach
- Don't share passwords with family
- Separate work and personal devices
- Educate family on work equipment boundaries

**During Video Calls:**
- Warn family when on calls
- Use virtual background if needed
- Mute microphone when not speaking
- Be aware of background noise
- Close door for confidential meetings

---

## 7. Home Office Equipment

### Standard Setup

**Basic Requirements:**
- Reliable internet connection
- Desk and chair
- Good lighting
- Quiet workspace
- Power backup (UPS recommended)

**Ergonomics:**
- Monitor at eye level
- Chair with back support
- Keyboard and mouse at comfortable height
- Take regular breaks
- Stand and stretch hourly

### Equipment Requests

**What You Can Request:**
- Second monitor
- Ergonomic keyboard/mouse
- Laptop stand
- Headset
- Webcam
- Docking station

**How to Request:**
1. Go to IT Portal
2. Select "Hardware Request"
3. Choose "Remote Work Equipment"
4. Explain need and justification
5. Submit request

**Approval Time:**
- Standard equipment: 1-2 weeks
- Special equipment: 2-4 weeks
- Emergency requests: 2-3 days

---

## 8. Internet Connectivity

### Minimum Requirements

**Speed Requirements:**
- Download: 10 Mbps minimum, 25 Mbps recommended
- Upload: 5 Mbps minimum, 10 Mbps recommended
- Latency: Under 100ms
- Stable connection without frequent drops

**Test Your Connection:**
1. Disconnect VPN
2. Go to speedtest.net
3. Run speed test
4. Screenshot results if slow
5. Contact IT if below minimum

### Improving Connection

**Quick Fixes:**
- Restart router
- Move closer to router
- Use wired Ethernet
- Close bandwidth-heavy apps
- Limit other devices on network

**Long-term Solutions:**
- Upgrade internet plan
- Replace old router
- Install WiFi extender
- Wire Ethernet to office
- Consider backup connection

### Backup Internet

**Recommended:**
- Mobile hotspot as backup
- Tethering from smartphone
- Secondary ISP (if available)
- Know nearby locations with WiFi

**When to Use Backup:**
- Primary connection down
- During primary ISP maintenance
- Emergency work situations
- Natural disasters

---

## 9. Troubleshooting Common Remote Work Issues

### Cannot Access Company Resources

**Symptoms:**
- Can't open email
- Network drives not accessible
- Internal websites don't load
- Applications won't connect

**Solution:**
1. Check VPN connection (most common cause)
2. Disconnect and reconnect VPN
3. Check internet connection
4. Restart VPN client
5. Restart computer
6. Contact IT if persists

### Slow Performance

**Symptoms:**
- Applications slow to respond
- Files take long to open
- Video calls lag
- Everything feels sluggish

**Troubleshooting:**
1. **Check Internet Speed**: Run speedtest.net
2. **Check VPN**: Try different server
3. **Close Apps**: Reduce open applications
4. **Restart Computer**: Clear memory
5. **Check Task Manager**: Look for CPU/Memory hogs
6. **Update Software**: Ensure all updates installed

### Video/Audio Issues in Calls

**Camera Not Working:**
- Check VPN isn't blocking
- Verify camera permissions
- Close other apps using camera
- Restart Teams
- Test in Camera app
- Update drivers

**Microphone Issues:**
- Check mute status (in app and on device)
- Verify correct microphone selected
- Check permissions
- Test in Sound settings
- Use headset instead of built-in

**Echo or Feedback:**
- Use headset
- Mute when not speaking
- Move away from speakers
- Check other participants aren't causing it

### Files Not Syncing

**OneDrive Sync Issues:**
1. Check OneDrive icon status
2. Click icon > View sync problems
3. Pause and resume sync
4. Check storage quota
5. Verify file names (no special characters)
6. Check file size (under 100GB per file)
7. Restart OneDrive
8. Contact IT if persists

---

## 10. Productivity Tips

### Time Management

**Work Schedule:**
- Set regular work hours
- Take scheduled breaks
- Use calendar blocks
- Set boundaries with family
- Start and end at consistent times

**Communication:**
- Set Teams status appropriately
- Respond to messages promptly
- Over-communicate progress
- Schedule regular check-ins
- Be visible and available

### Tools and Techniques

**Stay Organized:**
- Use To-Do lists (Microsoft To Do)
- Calendar for all commitments
- OneNote for meeting notes
- Focus time blocks
- Minimize distractions

**Collaboration:**
- Use Teams for quick questions
- Email for formal communication
- Video calls for complex discussions
- Screen share when explaining
- Document decisions in writing

---

## 11. When to Contact IT

### Urgent Issues (Call Immediately)

- Complete internet outage preventing work
- Laptop completely non-functional
- Security incident (phishing, malware, breach)
- Lost or stolen equipment
- Critical application failure

**Emergency Contact:**
- Phone: +66-XX-XXX-XXXX (24/7)
- Email: emergency@company.com

### Standard Issues (Create Ticket)

- VPN connectivity problems
- Software installation requests
- Performance issues
- Email problems
- File access issues
- Equipment requests

**Standard Contact:**
- Portal: https://itportal.company.com
- Phone: ext. 1234
- Email: helpdesk@company.com
- Hours: Mon-Fri 8:00-18:00

### Information to Provide

When contacting IT:
- Your name and employee ID
- Description of problem
- Error messages (screenshot if possible)
- Steps you've already tried
- When problem started
- Impact on work

---

## 12. Remote Work Security Checklist

### Daily Checklist

- [ ] Connected to VPN before starting work
- [ ] Laptop locked when stepping away
- [ ] No sensitive information visible to others
- [ ] Using company approved applications only
- [ ] Files saved to OneDrive/SharePoint
- [ ] Teams status updated appropriately

### Weekly Checklist

- [ ] Windows updates installed
- [ ] Antivirus scan completed
- [ ] OneDrive sync verified
- [ ] Restart computer at least once
- [ ] Test backup internet connection
- [ ] Clean up old files

### Monthly Checklist

- [ ] Change passwords if needed
- [ ] Review installed applications
- [ ] Check security settings
- [ ] Verify VPN client updated
- [ ] Review remote access permissions
- [ ] Complete security training if required

---

## Resources

### Self-Service Portal
- **URL**: https://itportal.company.com
- **Available 24/7**
- Knowledge base, FAQs, guides

### IT Helpdesk
- **Email**: helpdesk@company.com
- **Phone**: ext. 1234 / +66-2-XXX-XXXX
- **Hours**: Mon-Fri 8:00-18:00
- **Emergency**: +66-XX-XXX-XXXX (24/7)

### Remote Work Tools
- **VPN**: Cisco AnyConnect
- **Communication**: Microsoft Teams
- **Email**: Outlook
- **File Storage**: OneDrive for Business
- **Collaboration**: SharePoint

### Additional Guides
- Troubleshooting Guide
- Security Awareness Guide
- Software Installation Guide
- VPN Detailed Guide
- Teams User Guide

---

*Last Updated: October 2025*
*Version: 1.0*

