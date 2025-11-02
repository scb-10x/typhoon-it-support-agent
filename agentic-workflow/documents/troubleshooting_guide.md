# IT Troubleshooting Guide

## Common Issues and Solutions

### 1. Cannot Login to Computer

#### Symptoms
- "Invalid username or password" error
- Account locked message
- Computer not recognizing credentials

#### Solutions

**Step 1: Verify Credentials**
- Ensure Caps Lock is OFF
- Check keyboard language (should be English for login)
- Verify username format: DOMAIN\\username

**Step 2: Account Lock**
- After 5 failed attempts, account locks for 30 minutes
- Contact IT helpdesk to unlock immediately
- Or wait 30 minutes and try again

**Step 3: Password Expired**
- If password expired, use password reset portal
- From another device, go to https://itportal.company.com
- Follow password reset procedure

**Step 4: Computer Not Connected to Domain**
- Check network cable connection
- Verify WiFi is connected
- Try restarting computer while connected to network

#### When to Escalate
- After trying all steps above
- If seeing "Trust relationship failed" error
- If getting cryptic system errors

---

### 2. Slow Computer Performance

#### Symptoms
- Computer takes long time to start
- Applications freeze or respond slowly
- System feels sluggish overall

#### Solutions

**Quick Fixes:**
1. **Restart Computer**: Clears memory and temporary files
2. **Close Unnecessary Programs**: Check Task Manager (Ctrl+Shift+Esc)
3. **Clear Browser Cache**: Settings > Clear browsing data
4. **Check Disk Space**: Ensure at least 20% free space on C: drive

**Intermediate Fixes:**

**Check CPU Usage**
1. Open Task Manager (Ctrl+Shift+Esc)
2. Click "CPU" column to sort by usage
3. If any process uses >50% consistently, note the name
4. Common culprits: Antivirus during scan, Windows Updates, Chrome with many tabs

**Check Memory (RAM) Usage**
1. In Task Manager, check Memory column
2. If usage >90%, close some applications
3. Common memory hogs: Chrome, Outlook, Excel with large files

**Check Disk Usage**
1. In Task Manager > Performance > Disk
2. If disk usage constantly at 100%, could be:
   - Windows Search indexing (wait to complete)
   - Antivirus scan (wait to complete)
   - Windows Update (wait to complete)
   - Failing hard drive (escalate to IT)

**Advanced Fixes:**
1. **Run Disk Cleanup**: Search "Disk Cleanup" in Start Menu
2. **Disable Startup Programs**: Task Manager > Startup tab
3. **Update Drivers**: Windows Update or Device Manager
4. **Check for Malware**: Run full antivirus scan

#### When to Escalate
- Performance issues persist after restarts and cleanup
- Disk constantly at 100% usage
- Suspect hardware failure (strange noises, overheating)
- System crashes or blue screens

---

### 3. No Internet Connection

#### Symptoms
- Cannot access websites
- Email won't send/receive
- "No internet access" message
- Yellow warning on network icon

#### Solutions

**Step 1: Basic Checks**
1. Check if WiFi is turned on (physical switch on laptop)
2. Verify connected to correct network "CompanySecure"
3. Check if other devices have internet (phone, colleagues)

**Step 2: Restart Network**
1. Disconnect WiFi and reconnect
2. Or unplug/replug network cable
3. Restart computer if issue persists

**Step 3: Network Troubleshooting**

**Windows:**
1. Right-click network icon > Troubleshoot problems
2. Follow automated troubleshooter
3. If suggests "Reset network adapter", do it

**Manual Network Reset (Windows):**
1. Open Command Prompt as Administrator
2. Run these commands:
   ```
   ipconfig /release
   ipconfig /renew
   ipconfig /flushdns
   ```
3. Restart computer

**Mac:**
1. System Preferences > Network
2. Select WiFi > Advanced
3. Remove network and re-add it

**Step 4: Check IP Configuration**
1. Open Command Prompt/Terminal
2. Type: `ipconfig` (Windows) or `ifconfig` (Mac)
3. Should see IP starting with 10.x.x.x or 192.168.x.x
4. If IP is 169.254.x.x, not getting IP from DHCP (escalate)

**Step 5: VPN Issues**
- If VPN connected, try disconnecting and reconnecting
- If VPN won't connect, try different VPN server
- Clear VPN cache/credentials and re-enter

#### When to Escalate
- No other devices can connect (possible network outage)
- Getting 169.254.x.x IP address
- VPN connection consistently fails
- Physical network port appears damaged

---

### 4. Cannot Access Shared Drive/Network Folder

#### Symptoms
- "Network path not found"
- "You do not have permission"
- Drive mapping fails
- Can't see files in network folder

#### Solutions

**Step 1: Verify Network Connection**
- Ensure connected to company network or VPN
- Shared drives only accessible from internal network

**Step 2: Check Drive Path**
- Correct format: \\\\fileserver.company.com\\department
- Common mistake: using / instead of \\

**Step 3: Re-map Network Drive**

**Windows:**
1. Open File Explorer
2. Right-click "This PC" > "Map network drive"
3. Choose drive letter (e.g., Z:)
4. Enter path: \\\\fileserver.company.com\\[department]
5. Check "Reconnect at sign-in"
6. Check "Connect using different credentials" if needed
7. Click Finish and enter credentials

**Mac:**
1. Finder > Go > Connect to Server
2. Enter: smb://fileserver.company.com/[department]
3. Click Connect
4. Enter credentials when prompted

**Step 4: Verify Permissions**
- Contact department admin to verify access
- May need approval for certain folders
- Wait 15 minutes after approval for propagation

**Step 5: Clear Cached Credentials**

**Windows:**
1. Control Panel > Credential Manager
2. Windows Credentials > Remove old fileserver credentials
3. Try connecting again with fresh credentials

#### When to Escalate
- Error persists after re-mapping
- Need access to folder (permission request)
- Server appears completely unreachable

---

### 5. Email Issues

#### Common Email Problems

**5.1 Cannot Send Emails**

**Symptoms:**
- Emails stuck in Outbox
- "Cannot send" error message
- Sent emails not appearing in Sent folder

**Solutions:**
1. **Check Internet Connection**: Verify you're online
2. **Check Attachment Size**: Must be under 25MB
3. **Verify Recipient Address**: Check for typos
4. **Clear Outbox**:
   - Delete problematic email from Outbox
   - Compose new email
5. **Restart Outlook**: Close completely and reopen
6. **Check Quota**: If mailbox full, delete old emails

**5.2 Not Receiving Emails**

**Symptoms:**
- Expected emails not arriving
- Colleagues confirm they sent emails
- Delay in receiving emails

**Solutions:**
1. **Check Spam/Junk Folder**: Email might be filtered
2. **Check Mailbox Quota**: If full, new emails bounce
3. **Check Email Rules**: May be auto-moving emails
4. **Verify Forwarding**: Check if auto-forward is enabled
5. **Check Mail Server Status**: Ask colleagues if they have issues

**5.3 Outlook Keeps Asking for Password**

**Solutions:**
1. **Update Password in Credential Manager**:
   - Control Panel > Credential Manager
   - Update Office credentials
2. **Clear Cached Credentials**: Remove all Office-related credentials
3. **Recreate Outlook Profile**: May need IT assistance

#### When to Escalate
- Mailbox quota cannot be increased (request archive)
- Outlook corruption suspected
- Missing important emails
- Account might be compromised

---

### 6. Printer Issues

#### 6.1 Cannot Print

**Symptoms:**
- Print job sent but nothing prints
- Printer offline
- Document stuck in print queue

**Solutions:**

**Step 1: Basic Checks**
1. Verify printer is powered on
2. Check if printer has paper
3. Check for error messages on printer display
4. Ensure printer cable connected (if wired)

**Step 2: Check Printer Status**
1. Windows: Settings > Devices > Printers
2. Right-click printer > "See what's printing"
3. If shows "Offline", right-click > "Use Printer Online"

**Step 3: Clear Print Queue**
1. Open print queue (see Step 2)
2. Click Document > Cancel All Documents
3. Wait for queue to clear
4. Restart Print Spooler service (may need admin rights)

**Step 4: Restart Everything**
1. Cancel all print jobs
2. Turn off printer for 30 seconds
3. Restart computer
4. Turn on printer
5. Try printing again

**Step 5: Reinstall Printer**
1. Remove printer from system
2. Go to: http://printserver.company.com
3. Find your printer
4. Click Install
5. Follow prompts

#### 6.2 Print Quality Issues

**Symptoms:**
- Faded prints
- Streaks or lines
- Smudged output
- Wrong colors

**Solutions:**
1. **Check Toner/Ink Levels**: Replace if low
2. **Run Printer Cleaning**: From printer menu or software
3. **Check Paper Type**: Ensure correct paper loaded
4. **Update Printer Driver**: From print server
5. **Call Facilities**: For toner replacement or repairs

#### When to Escalate
- Printer needs new toner (contact facilities)
- Printer making strange noises
- Paper jams cannot be cleared
- Need to add new printer to system

---

### 7. Software Crashes or Won't Open

#### Symptoms
- Application crashes on startup
- "Application not responding"
- Error messages when opening
- Software freezes during use

#### Solutions

**Step 1: Quick Fixes**
1. **Force Close Application**:
   - Windows: Ctrl+Alt+Del > Task Manager > End Task
   - Mac: Cmd+Option+Esc > Force Quit
2. **Restart Computer**: Clears memory and temporary files
3. **Update Software**: Check for available updates

**Step 2: Check System Requirements**
- Verify software compatible with your OS version
- Check if enough disk space available
- Ensure sufficient RAM for application

**Step 3: Repair Installation**

**Windows:**
1. Settings > Apps > Apps & features
2. Find the application
3. Click > Modify > Repair

**Step 4: Reinstall Software**
1. Uninstall application completely
2. Restart computer
3. Download from Software Center
4. Reinstall fresh copy

**Step 5: Check Error Logs**
- Windows: Event Viewer > Application logs
- Note any error codes or messages
- Share with IT if escalating

#### When to Escalate
- Software critical for work and won't function
- Error codes you don't understand
- Reinstall doesn't fix issue
- Need to install new/specialized software

---

### 8. Video Conferencing Issues (Zoom/Teams)

#### 8.1 Camera Not Working

**Symptoms:**
- "No camera detected"
- Black screen where video should be
- Other participants can't see you

**Solutions:**
1. **Check Physical Camera**:
   - Ensure camera lens not covered
   - External camera: check USB connection
   - Laptop: verify camera privacy shutter is open
2. **Check Permissions**:
   - Windows: Settings > Privacy > Camera > Allow apps
   - Mac: System Preferences > Security & Privacy > Camera
3. **Check App Settings**:
   - In Zoom/Teams: Settings > Video
   - Select correct camera from dropdown
4. **Close Other Apps**: Camera can only be used by one app at a time
5. **Restart Application**: Close and reopen Zoom/Teams
6. **Update Drivers**: Windows Update or manufacturer website

#### 8.2 Microphone Not Working

**Solutions:**
1. **Check Mute Status**: Verify not muted in app and on headset
2. **Check Default Device**:
   - Windows: Right-click speaker icon > Sound settings
   - Ensure correct microphone selected
3. **Check Permissions**: Same as camera permissions
4. **Test Microphone**:
   - Windows: Sound settings > Test your microphone
   - Mac: System Preferences > Sound > Input
5. **Check Physical Connection**: Headset properly plugged in

#### 8.3 No Sound/Can't Hear Others

**Solutions:**
1. **Check Speaker Settings**:
   - Verify volume not at 0
   - Check correct output device selected
2. **Check App Audio**:
   - In Zoom/Teams: Settings > Audio
   - Test speaker
3. **Restart Audio**:
   - Leave and rejoin meeting
   - Or click "Test speaker & microphone"

#### When to Escalate
- Hardware appears faulty
- Drivers won't install/update
- Issues persist across all applications
- Need new headset/camera

---

## Emergency Contacts

### Critical Issues (System Down, Data Loss, Security Breach)
- **24/7 Hotline**: +66-XX-XXX-XXXX
- **Email**: emergency@company.com
- **Response Time**: Within 15 minutes

### Standard IT Support
- **Helpdesk**: ext. 1234 or helpdesk@company.com
- **Hours**: Mon-Fri 8:00-18:00
- **Response Time**: Within 2 hours

### Hardware Issues
- **Facilities**: ext. 5678
- **For**: Printer repairs, toner, hardware replacement

---

*This guide is regularly updated. Last update: October 2025*
