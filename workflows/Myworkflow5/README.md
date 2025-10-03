# Workflow: My workflow 5

## Overview

This document provides an overview of the 'My workflow 5' workflow.

## Workflow Steps (Nodes)

| Step Name | Type |
|-----------|------|
| Webhook Trigger - Enrollment | n8n-nodes-base.webhook |
| Process Enrollment Data | n8n-nodes-base.set |
| Save Enrollment to DB | n8n-nodes-base.httpRequest |
| Send Welcome Email | n8n-nodes-base.sendEmail |
| Schedule Daily Module Check | n8n-nodes-base.cron |
| Get All Active Enrollments | n8n-nodes-base.httpRequest |
| Iterate Over Enrollments | n8n-nodes-base.splitInBatches |
| Check Module Unlock Condition | n8n-nodes-base.if |
| Unlock Day 2 Modules | n8n-nodes-base.set |
| Unlock Day 3 Modules | n8n-nodes-base.set |
| Update Enrollment in DB | n8n-nodes-base.httpRequest |
| Send Module Unlocked Email | n8n-nodes-base.sendEmail |
| Webhook Trigger - Assignment Submission | n8n-nodes-base.webhook |
| Process Submission Data | n8n-nodes-base.set |
| Call AI for Feedback (ChatGPT) | n8n-nodes-base.httpRequest |
| Extract AI Feedback | n8n-nodes-base.set |
| Save Feedback to DB | n8n-nodes-base.httpRequest |
| Send Feedback Email | n8n-nodes-base.sendEmail |

## Raw JSON

```json
{
  "name": "My workflow 5",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "enrollment",
        "options": {}
      },
      "id": "1860d599-536b-4600-81f1-b758b3d66507",
      "name": "Webhook Trigger - Enrollment",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [
        48,
        -144
      ],
      "webhookId": "538ff9f5-e2d0-496a-a453-5275bc9f3d4c"
    },
    {
      "parameters": {
        "options": {}
      },
      "id": "f05beb22-d38d-40d6-a929-c2a04dbdcbdf",
      "name": "Process Enrollment Data",
      "type": "n8n-nodes-base.set",
      "typeVersion": 1,
      "position": [
        288,
        -144
      ]
    },
    {
      "parameters": {
        "requestMethod": "POST",
        "url": "https://your-lms-api.com/enrollments",
        "options": {}
      },
      "id": "eb3f1c13-15e0-4084-bbc3-0416c4c98a54",
      "name": "Save Enrollment to DB",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 1,
      "position": [
        528,
        -144
      ]
    },
    {
      "parameters": {},
      "id": "18957db4-d1b3-4525-abc7-2fee3f0440d2",
      "name": "Send Welcome Email",
      "type": "n8n-nodes-base.sendEmail",
      "typeVersion": 1,
      "position": [
        768,
        -144
      ],
      "credentials": {}
    },
    {
      "parameters": {},
      "id": "bde9cbe1-e606-4d34-86c6-8a6a39a0ee08",
      "name": "Schedule Daily Module Check",
      "type": "n8n-nodes-base.cron",
      "typeVersion": 1,
      "position": [
        48,
        64
      ]
    },
    {
      "parameters": {
        "url": "https://your-lms-api.com/enrollments/active",
        "options": {}
      },
      "id": "43646786-a256-4f74-a4cf-619a9fd41350",
      "name": "Get All Active Enrollments",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 1,
      "position": [
        288,
        64
      ]
    },
    {
      "parameters": {
        "batchSize": 1,
        "options": {}
      },
      "id": "1078733c-ab11-4a36-931b-43098d0e8a8c",
      "name": "Iterate Over Enrollments",
      "type": "n8n-nodes-base.splitInBatches",
      "typeVersion": 1,
      "position": [
        528,
        64
      ]
    },
    {
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{$json.currentDay}}",
              "operation": "<=",
              "value2": "3"
            }
          ]
        }
      },
      "id": "89a208aa-894c-45d8-9828-ed7f8abeeccc",
      "name": "Check Module Unlock Condition",
      "type": "n8n-nodes-base.if",
      "typeVersion": 1,
      "position": [
        768,
        64
      ]
    },
    {
      "parameters": {
        "options": {}
      },
      "id": "634f4eca-78e1-4465-8bdb-026b502b4ef3",
      "name": "Unlock Day 2 Modules",
      "type": "n8n-nodes-base.set",
      "typeVersion": 1,
      "position": [
        1008,
        16
      ]
    },
    {
      "parameters": {
        "options": {}
      },
      "id": "e40fe597-b151-4695-b0ee-1196235ca15f",
      "name": "Unlock Day 3 Modules",
      "type": "n8n-nodes-base.set",
      "typeVersion": 1,
      "position": [
        1008,
        112
      ]
    },
    {
      "parameters": {
        "requestMethod": "PUT",
        "url": "https://your-lms-api.com/enrollments/{{$json.studentId}}",
        "options": {}
      },
      "id": "d4e5ef92-8b7f-42aa-997b-b9447c9c965c",
      "name": "Update Enrollment in DB",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 1,
      "position": [
        1248,
        64
      ]
    },
    {
      "parameters": {},
      "id": "a0d67627-f83e-42e0-a624-cf647913a795",
      "name": "Send Module Unlocked Email",
      "type": "n8n-nodes-base.sendEmail",
      "typeVersion": 1,
      "position": [
        1488,
        64
      ],
      "credentials": {}
    },
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "assignment-submission",
        "options": {}
      },
      "id": "7b8b0141-1509-46a9-81a2-fe1fb6cdb90c",
      "name": "Webhook Trigger - Assignment Submission",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [
        48,
        256
      ],
      "webhookId": "57a761e5-eb6c-4ad5-8d1f-375b351f558c"
    },
    {
      "parameters": {
        "options": {}
      },
      "id": "912d2c4f-d041-4f57-b559-1623d10addd1",
      "name": "Process Submission Data",
      "type": "n8n-nodes-base.set",
      "typeVersion": 1,
      "position": [
        288,
        256
      ]
    },
    {
      "parameters": {
        "requestMethod": "POST",
        "url": "https://api.openai.com/v1/chat/completions",
        "options": {}
      },
      "id": "62ed1ff8-5555-4bd9-bce0-15b815c7f729",
      "name": "Call AI for Feedback (ChatGPT)",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 1,
      "position": [
        528,
        256
      ]
    },
    {
      "parameters": {
        "options": {}
      },
      "id": "3b1e79e9-3586-42a7-8357-d1acf004d03a",
      "name": "Extract AI Feedback",
      "type": "n8n-nodes-base.set",
      "typeVersion": 1,
      "position": [
        768,
        256
      ]
    },
    {
      "parameters": {
        "requestMethod": "POST",
        "url": "https://your-lms-api.com/assignments/feedback",
        "options": {}
      },
      "id": "493ab847-99a9-4c58-8220-b31a4642625f",
      "name": "Save Feedback to DB",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 1,
      "position": [
        1008,
        256
      ]
    },
    {
      "parameters": {},
      "id": "d9916872-24f4-4373-bf6d-9ef775228950",
      "name": "Send Feedback Email",
      "type": "n8n-nodes-base.sendEmail",
      "typeVersion": 1,
      "position": [
        1248,
        256
      ],
      "credentials": {}
    }
  ],
  "connections": {
    "Iterate Over Enrollments": {
      "main": [
        [
          {
            "node": "Check Module Unlock Condition",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Get All Active Enrollments": {
      "main": [
        [
          {
            "node": "Iterate Over Enrollments",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Process Enrollment Data": {
      "main": [
        [
          {
            "node": "Save Enrollment to DB",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Webhook Trigger - Enrollment": {
      "main": [
        [
          {
            "node": "Process Enrollment Data",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Schedule Daily Module Check": {
      "main": [
        [
          {
            "node": "Get All Active Enrollments",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Webhook Trigger - Assignment Submission": {
      "main": [
        [
          {
            "node": "Process Submission Data",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Process Submission Data": {
      "main": [
        [
          {
            "node": "Call AI for Feedback (ChatGPT)",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Call AI for Feedback (ChatGPT)": {
      "main": [
        [
          {
            "node": "Extract AI Feedback",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Extract AI Feedback": {
      "main": [
        [
          {
            "node": "Save Feedback to DB",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Unlock Day 3 Modules": {
      "main": [
        [
          {
            "node": "Update Enrollment in DB",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Unlock Day 2 Modules": {
      "main": [
        [
          {
            "node": "Update Enrollment in DB",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Check Module Unlock Condition": {
      "main": [
        [
          {
            "node": "Unlock Day 2 Modules",
            "type": "main",
            "index": 0
          }
        ],
        [
          {
            "node": "Unlock Day 3 Modules",
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
