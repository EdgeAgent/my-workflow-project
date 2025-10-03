# Workflow: WhatsApp Orders to CRM/Invoice

## Overview

This document provides an overview of the 'WhatsApp Orders to CRM/Invoice' workflow.

## Workflow Steps (Nodes)

| Step Name | Type |
|-----------|------|
| WhatsApp Webhook | n8n-nodes-base.webhook |
| Filter Text Messages | n8n-nodes-base.if |
| Parse Order Data | n8n-nodes-base.code |
| Create/Update CRM Contact | n8n-nodes-base.hubspot |
| Create Deal/Opportunity | n8n-nodes-base.hubspot |
| Create Invoice | n8n-nodes-base.quickbooks |
| Send WhatsApp Confirmation | n8n-nodes-base.httpRequest |
| Webhook Response | n8n-nodes-base.respondToWebhook |

## Raw JSON

```json
{
  "name": "WhatsApp Orders to CRM/Invoice",
  "nodes": [
    {
      "parameters": {
        "path": "whatsapp-webhook",
        "responseMode": "responseNode",
        "options": {}
      },
      "id": "e269aa02-fe30-420b-b110-84cd7fe3b064",
      "name": "WhatsApp Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [
        -608,
        208
      ],
      "webhookId": "3b405d7e-8c36-4af2-a4e0-76ef014b7ccf"
    },
    {
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{$json.body.entry[0].changes[0].value.messages[0].type}}",
              "operation": "equals",
              "value2": "text"
            }
          ]
        }
      },
      "id": "16f79016-01b0-4295-a81e-b066240cff86",
      "name": "Filter Text Messages",
      "type": "n8n-nodes-base.if",
      "typeVersion": 1,
      "position": [
        -400,
        208
      ]
    },
    {
      "parameters": {
        "jsCode": "// Extract WhatsApp message data\nconst messageData = $input.item.json.body.entry[0].changes[0].value.messages[0];\nconst contactData = $input.item.json.body.entry[0].changes[0].value.contacts[0];\n\n// Parse order from message text\nconst messageText = messageData.text.body;\nconst phone = messageData.from;\nconst customerName = contactData.profile.name;\n\n// Extract order details (customize pattern based on your order format)\n// Example: \"Order: 2x Product A, 1x Product B, Total: $150\"\nconst orderPattern = /Order:(.+?)(?:Total:|$)/i;\nconst totalPattern = /Total:\\s*\\$?(\\d+\\.?\\d*)/i;\n\nlet items = [];\nlet total = 0;\n\nconst orderMatch = messageText.match(orderPattern);\nif (orderMatch) {\n  const itemsText = orderMatch[1];\n  // Parse items like \"2x Product A, 1x Product B\"\n  const itemMatches = itemsText.matchAll(/(\\d+)x\\s*([^,]+)/gi);\n  for (const match of itemMatches) {\n    items.push({\n      quantity: parseInt(match[1]),\n      product: match[2].trim()\n    });\n  }\n}\n\nconst totalMatch = messageText.match(totalPattern);\nif (totalMatch) {\n  total = parseFloat(totalMatch[1]);\n}\n\nreturn {\n  customerName: customerName,\n  phone: phone,\n  orderText: messageText,\n  items: items,\n  total: total,\n  orderDate: new Date().toISOString(),\n  source: 'WhatsApp'\n};"
      },
      "id": "ad0ddb9b-83e9-444f-a6c7-c91827becdcf",
      "name": "Parse Order Data",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        -208,
        112
      ]
    },
    {
      "parameters": {
        "resource": "contact",
        "operation": "create"
      },
      "id": "4a5e4e4d-00b5-44d4-a318-b8ebd26ca798",
      "name": "Create/Update CRM Contact",
      "type": "n8n-nodes-base.hubspot",
      "typeVersion": 1,
      "position": [
        0,
        0
      ],
      "notes": "Replace with your CRM (HubSpot, Salesforce, Pipedrive, etc.)"
    },
    {
      "parameters": {
        "additionalFields": {
          "amount": "={{$json.total}}",
          "dealName": "WhatsApp Order - {{$json.customerName}}"
        }
      },
      "id": "e4819026-b52a-4307-8938-d90a4bce6978",
      "name": "Create Deal/Opportunity",
      "type": "n8n-nodes-base.hubspot",
      "typeVersion": 1,
      "position": [
        208,
        0
      ]
    },
    {
      "parameters": {
        "operation": "create",
        "additionalFields": {}
      },
      "id": "77761269-980c-4ae3-9498-95140afd2b7e",
      "name": "Create Invoice",
      "type": "n8n-nodes-base.quickbooks",
      "typeVersion": 1,
      "position": [
        0,
        208
      ],
      "notes": "Replace with your invoicing system (QuickBooks, Stripe, Wave, etc.)"
    },
    {
      "parameters": {
        "method": "POST",
        "url": "https://graph.facebook.com/v18.0/YOUR_PHONE_NUMBER_ID/messages",
        "authentication": "predefinedCredentialType",
        "nodeCredentialType": "whatsAppApi",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            {
              "name": "messaging_product",
              "value": "whatsapp"
            },
            {
              "name": "to",
              "value": "={{$json.phone}}"
            },
            {
              "name": "type",
              "value": "text"
            },
            {
              "name": "text",
              "value": "={\"body\": \"Thank you for your order! We've received: {{$json.orderText}}. Your order has been processed and you'll receive confirmation shortly.\"}"
            }
          ]
        },
        "options": {}
      },
      "id": "986f331f-ae05-4e9b-9da6-f8f25cb57c8b",
      "name": "Send WhatsApp Confirmation",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.1,
      "position": [
        208,
        208
      ]
    },
    {
      "parameters": {
        "respondWith": "json",
        "responseBody": "={\"status\": \"success\", \"message\": \"Order processed\"}",
        "options": {
          "responseCode": 200
        }
      },
      "id": "7ef11418-0ce0-4e0e-8624-40abc22d4cff",
      "name": "Webhook Response",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1,
      "position": [
        400,
        208
      ]
    }
  ],
  "connections": {
    "WhatsApp Webhook": {
      "main": [
        [
          {
            "node": "Filter Text Messages",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Filter Text Messages": {
      "main": [
        [
          {
            "node": "Parse Order Data",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Parse Order Data": {
      "main": [
        [
          {
            "node": "Create/Update CRM Contact",
            "type": "main",
            "index": 0
          },
          {
            "node": "Create Invoice",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Create/Update CRM Contact": {
      "main": [
        [
          {
            "node": "Create Deal/Opportunity",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Create Deal/Opportunity": {
      "main": [
        [
          {
            "node": "Send WhatsApp Confirmation",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Create Invoice": {
      "main": [
        [
          {
            "node": "Send WhatsApp Confirmation",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Send WhatsApp Confirmation": {
      "main": [
        [
          {
            "node": "Webhook Response",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "settings": {
    "executionOrder": "v1"
  },
  "staticData": null,
  "pinData": {},
  "triggerCount": 0,
  "meta": null
}
```
