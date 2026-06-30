#!/usr/bin/env bash
# deploy-mcp.sh — Care Pal Lab 5: deploy the mock appointments MCP server (admin, once).
# Pushes mcp-appointments/ to Azure Container Apps with PUBLIC, NO-AUTH ingress, then prints
# the /mcp URL to paste into the Foundry agent's MCP tool. Synthetic data only.
#
# Prereqs: Azure CLI (`az login`), a subscription with Container Apps quota. Builds from source
# (no local Docker needed) via `az containerapp up`.
#
# Usage: ./deploy-mcp.sh    (override with env: RESOURCE_GROUP, APP_NAME, ENVIRONMENT, LOCATION)
set -euo pipefail

RESOURCE_GROUP="${RESOURCE_GROUP:-rg-carepal-mcp}"
APP_NAME="${APP_NAME:-carepal-appointments}"
ENVIRONMENT="${ENVIRONMENT:-carepal-mcp-env}"
LOCATION="${LOCATION:-southeastasia}"
HERE="$(cd "$(dirname "$0")" && pwd)"

echo "Deploying $APP_NAME to $RESOURCE_GROUP ($LOCATION)..."
az group create -n "$RESOURCE_GROUP" -l "$LOCATION" -o none

az containerapp up \
  --name "$APP_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --environment "$ENVIRONMENT" \
  --location "$LOCATION" \
  --source "$HERE" \
  --ingress external \
  --target-port 8000 \
  --env-vars PORT=8000

FQDN=$(az containerapp show -n "$APP_NAME" -g "$RESOURCE_GROUP" --query "properties.configuration.ingress.fqdn" -o tsv)
echo ""
echo "MCP endpoint (share with participants):"
echo "  https://$FQDN/mcp"
echo "Auth: None. Approval: set book_appointment to require approval in Foundry."
