# Workflow: My workflow 6

## Overview

This document provides an overview of the 'My workflow 6' workflow.

## Workflow Steps (Nodes)

| Step Name | Type |
|-----------|------|
| Manual Trigger | n8n-nodes-base.manualTrigger |
| TikTok Trend Analysis | n8n-nodes-base.httpRequest |
| OpenAI Script Generation | n8n-nodes-base.openAi |
| HeyGen Video Generation | n8n-nodes-base.httpRequest |
| Status Monitoring | n8n-nodes-base.function |
| Notification | n8n-nodes-base.httpRequest |

## Raw JSON

```json
{
  "name": "My workflow 6",
  "nodes": [
    {
      "parameters": {},
      "id": "42b0a686-a798-4f44-ad0f-14b4f0932d10",
      "name": "Manual Trigger",
      "type": "n8n-nodes-base.manualTrigger",
      "typeVersion": 1,
      "position": [
        208,
        112
      ]
    },
    {
      "parameters": {
        "authentication": "headerAuth",
        "url": "https://api.tiktok.com/v1/trends/search",
        "options": {},
        "headerParametersUi": {
          "parameter": [
            {
              "name": "Authorization",
              "value": "Bearer YOUR_TIKTOK_API_KEY"
            }
          ]
        },
        "queryParametersUi": {
          "parameter": [
            {
              "name": "query",
              "value": "={{$json[\"product\"]}}"
            }
          ]
        }
      },
      "id": "83ff2f21-104f-4a22-836a-8ee32def4fd0",
      "name": "TikTok Trend Analysis",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 2,
      "position": [
        448,
        112
      ]
    },
    {
      "parameters": {
        "resource": "completion",
        "requestOptions": {}
      },
      "id": "9481e983-4d9d-4b0d-9316-15820de41e5f",
      "name": "OpenAI Script Generation",
      "type": "n8n-nodes-base.openAi",
      "typeVersion": 1,
      "position": [
        688,
        112
      ]
    },
    {
      "parameters": {
        "authentication": "headerAuth",
        "url": "https://api.heygen.com/v1/video/generate",
        "options": {},
        "headerParametersUi": {
          "parameter": [
            {
              "name": "X-Api-Key",
              "value": "YOUR_HEYGEN_API_KEY"
            }
          ]
        }
      },
      "id": "a8769b86-a8e4-4099-a544-0547fb135d47",
      "name": "HeyGen Video Generation",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 2,
      "position": [
        928,
        112
      ]
    },
    {
      "parameters": {
        "functionCode": "let retry = 0;\nconst maxRetries = 20;\nconst interval = 30000; // 30 seconds\nlet videoReady = false;\nlet videoUrl = '';\ndo {\n  const response = await this.helpers.request({\n    method: 'GET',\n    url: `https://api.heygen.com/v1/video/status?id=${$json[\"id\"]}`,\n    headers: {\n      'X-Api-Key': 'YOUR_HEYGEN_API_KEY'\n    }\n  });\n  if (response.status === 'completed') {\n    videoReady = true;\n    videoUrl = response.video_url;\n    break;\n  }\n  retry++;\n  if (retry < maxRetries) await new Promise(r => setTimeout(r, interval));\n} while (!videoReady && retry < maxRetries);\nreturn [{videoUrl, status: videoReady ? 'ready' : 'timeout'}];"
      },
      "id": "f7aa1ca2-9329-44cb-a639-ae0b587bc0aa",
      "name": "Status Monitoring",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "position": [
        1168,
        112
      ]
    },
    {
      "parameters": {
        "url": "YOUR_WEBHOOK_OR_NOTIFICATION_URL",
        "options": {}
      },
      "id": "54c15e12-9be6-4b69-8bb4-9ec83fc09ccf",
      "name": "Notification",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 2,
      "position": [
        1408,
        112
      ]
    }
  ],
  "connections": {
    "Manual Trigger": {
      "main": [
        [
          {
            "node": "TikTok Trend Analysis",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "TikTok Trend Analysis": {
      "main": [
        [
          {
            "node": "OpenAI Script Generation",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "OpenAI Script Generation": {
      "main": [
        [
          {
            "node": "HeyGen Video Generation",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "HeyGen Video Generation": {
      "main": [
        [
          {
            "node": "Status Monitoring",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Status Monitoring": {
      "main": [
        [
          {
            "node": "Notification",
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
