<#
  deploy-mcp.ps1 — Care Pal Lab 5: deploy the mock appointments MCP server (admin, once).

  Pushes mcp-appointments/ to Azure Container Apps with PUBLIC, NO-AUTH ingress, then prints
  the /mcp URL to paste into the Foundry agent's MCP tool. Synthetic data only.

  Prereqs: Azure CLI (`az login`), the containerapp extension (auto-installed), a subscription
  with Container Apps quota. Builds from source (no local Docker needed) via `az containerapp up`.

  Usage:
    ./deploy-mcp.ps1                                  # defaults below
    ./deploy-mcp.ps1 -ResourceGroup rg-carepal -Location southeastasia
#>
param(
  [string]$ResourceGroup = "rg-carepal-mcp",
  [string]$AppName       = "carepal-appointments",
  [string]$Environment   = "carepal-mcp-env",
  [string]$Location      = "southeastasia"
)

$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "Deploying $AppName to $ResourceGroup ($Location)..." -ForegroundColor Cyan
az group create -n $ResourceGroup -l $Location -o none

az containerapp up `
  --name $AppName `
  --resource-group $ResourceGroup `
  --environment $Environment `
  --location $Location `
  --source $here `
  --ingress external `
  --target-port 8000 `
  --env-vars PORT=8000

$fqdn = az containerapp show -n $AppName -g $ResourceGroup --query "properties.configuration.ingress.fqdn" -o tsv
$url  = "https://$fqdn/mcp"
Write-Host ""
Write-Host "MCP endpoint (share with participants):" -ForegroundColor Green
Write-Host "  $url" -ForegroundColor Yellow
Write-Host "Auth: None. Approval: set book_appointment to require approval in Foundry."
