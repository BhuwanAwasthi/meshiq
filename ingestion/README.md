# MeshIQ — Live Teams Transcript Ingestion (Power Automate)

Goal: when a Teams meeting ends and its transcript is ready, automatically pull
the transcript and feed it into the existing MeshIQ pipeline — no manual upload.

Built entirely in Power Automate + Graph (no Azure Function, since the agents
are only reachable from Power Automate in this setup).

## Two subscription strategies (build the fallback — it's more reliable)

### Primary: getAllTranscripts
Resource: communications/onlineMeetings/getAllTranscripts, changeType=created.
- Can include resource data (the transcript metadata) in the payload.
- HARD CONSTRAINT: the notification is only sent if you subscribe BEFORE the
  meeting's transcription starts. Subscriptions are also short-lived for this
  resource, so they need regular renewal (lifecycle notifications).
- Known issue: many report webhook validation succeeding but payloads never
  arriving. If you see that, switch to the fallback.

### Fallback (RECOMMENDED): callRecords
Resource: communications/callRecords, changeType=created.
- A callRecord is created shortly AFTER a meeting ends — more reliable + mature.
- The payload contains the meeting/call info. You then call Graph to fetch the
  transcript for that meeting.
- This "notify, then fetch" pattern is the resilient industry workaround.

## Flow design (callRecords path)

1. **Subscription setup (one-time):** an admin flow (or Graph Explorer / Postman)
   POSTs subscription_callrecords.json to https://graph.microsoft.com/v1.0/subscriptions.
   Use the Entra app you registered in Phase 0 (it has the meeting/transcript
   Application permissions). Renew before expiry.

2. **Validation handshake:** Graph first calls your notificationUrl with a
   ?validationToken=... query param. The flow must return 200 with that token as
   text/plain. In Power Automate: a parallel branch on the HTTP trigger — if
   validationToken is present, Response action returns it verbatim.

3. **On a callRecord notification:**
   - Verify clientState matches your secret (security).
   - Extract the meeting/call id from the payload.
   - GET the transcript list for that meeting via Graph:
     /users/{organizerId}/onlineMeetings/{meetingId}/transcripts
     (or the callRecord sessions to resolve the meeting).
   - GET the transcript content:
     /users/{organizerId}/onlineMeetings/{meetingId}/transcripts/{id}/content
     with ?$format=text/vtt  (VTT) — then strip timestamps to plain text.

4. **Hand off to the existing pipeline:**
   - Either drop the cleaned transcript text into the transcripts container /
     trigger source the orchestration flow already listens to, OR call the
     orchestration flow directly (child flow) passing the transcript string.
   - Everything downstream (router -> evaluator -> Dataverse -> Teams approval)
     is UNCHANGED.

## Permissions (already set in Phase 0)
OnlineMeetingTranscript.Read.All, OnlineMeetingRecording.Read.All,
OnlineMeetings.Read.All (Application), admin-consented. callRecords needs
CallRecords.Read.All (Application). Add + consent that one if missing.

## Application access policy (required!)
Reading meeting transcripts with an app identity also requires a Teams
application access policy granting the app access to the organizer's meetings.
Run once in Teams PowerShell:
  New-CsApplicationAccessPolicy -Identity MeshIQ-Policy -AppIds "<app-client-id>" -Description "MeshIQ"
  Grant-CsApplicationAccessPolicy -PolicyName MeshIQ-Policy -Global
(or -Identity <organizer-user> instead of -Global for a single test user)

## Demo strategy
- Keep the MANUAL upload trigger as the guaranteed on-camera path.
- Show the live path as the "and it also picks up automatically" moment: start a
  short Teams meeting with transcription on, end it, and let the flow run. If the
  tenant is flaky, narrate the architecture and show the flow run history instead.

## VTT -> plain text
Transcript content comes as WEBVTT (timestamps + speaker + line). In the flow,
after fetching, use a Compose with a replace/split to drop the timecode lines,
or just pass the VTT to the router — the agents handle light formatting fine.
