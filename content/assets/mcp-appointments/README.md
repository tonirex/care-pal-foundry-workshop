# Mock Appointments — MCP server (Lab 5, Part A)

Gives Care Pal a **real tool** over the open **Model Context Protocol**, with
**human-in-the-loop** approval before anything is "booked". Synthetic data only.

## Tools
| tool | does |
|------|------|
| `list_slots(specialty, week_of="")` | returns 3 synthetic follow-up slots for the matched clinic |
| `book_appointment(slot_id, patient_ref)` | returns a **mock** booking confirmation |

**No authentication.** It's synthetic and meant to be pasted in by 40 people; the admin deploys
it once and shares the link.

## Admin: deploy once, share the link (before the workshop)
Deploy to Azure Container Apps with public, no-auth ingress and copy the printed URL into the guide:
```powershell
az login
./deploy-mcp.ps1                 # or: bash deploy-mcp.sh   (override RG/region via params)
```
Prints: `https://carepal-appointments.<region>.azurecontainerapps.io/mcp`. Builds from source
(no local Docker needed) and stays up for the day. Share that **/mcp** URL with participants.

> **Live demo instance:** `https://carepal-appointments.delightfulpond-b7635e07.southeastasia.azurecontainerapps.io/mcp` (no auth, southeastasia).
> Windows note: the `az containerapp up` log-streamer can crash on a console encoding bug — harmless;
> the ACR build still succeeds. If it does, `az acr build -r <acr> -t carepal-appointments:v1 .` then
> `az containerapp create … --image …:v1 --ingress external --target-port 8000` finishes the job.

## Cost (leave it running)
0.5 vCPU / 1 GiB, min 1 replica (always warm). With the monthly free grant (180k vCPU-s, 360k GiB-s, 2M req) the realistic bill is **~$6 for two weeks** of workshop traffic, ~$15 worst-case fully active. Tear down with `az group delete -n rg-carepal-mcp --yes`.

## Run it locally instead (dev / dry-run)
```powershell
pip install -r requirements.txt
python server.py                 # serves at http://0.0.0.0:8000/mcp
```
Expose it publicly with a tunnel if attaching from the portal — `devtunnel host -p 8000` or VS Code
**Ports → Forward a Port** (Public). The deployed URL is simpler for a room of 40.

## Attach to Care Pal in Foundry
1. Agent → **Tools → MCP** (or SDK `MCPTool(server_label, server_url, require_approval)`), paste the
   shared **/mcp** URL as `server_url`. The portal's MCP form has no "None" auth — leave **Key-based**
   and add one throwaway header (e.g. `x-demo: workshop`); the server ignores it.
2. Approve `book_appointment` per call (**Approve once** at runtime) so a human confirms before booking.
3. Ask: *"Can you arrange my father's heart-failure follow-up next week?"* → approve → confirm a slot.

## Safety
Everything here is synthetic. `book_appointment` never touches a real scheduling system; its
`booking_ref` is prefixed `MOCK-`. Keep the approval gate on — it's the teaching point.
