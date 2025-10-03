# Workflow: AI Phone Agent - Onboarding & Appointments

## Overview

This document provides an overview of the 'AI Phone Agent - Onboarding & Appointments' workflow.

## Workflow Steps (Nodes)

| Step Name | Type |
|-----------|------|
| TTS - Continue | n8n-nodes-base.googleCloudTextToSpeech |
| Webhook - Incoming Call | n8n-nodes-base.webhook |
| TTS - Greeting | n8n-nodes-base.googleCloudTextToSpeech |
| STT - Capture Name | n8n-nodes-base.googleCloudSpeechToText |
| Set Customer Name | n8n-nodes-base.set |
| AI Agent - Name Response | @n8n/n8n-nodes-langchain.agent |
| TTS - Name Response | n8n-nodes-base.googleCloudTextToSpeech |
| STT - Customer Need | n8n-nodes-base.googleCloudSpeechToText |
| Set Customer Need | n8n-nodes-base.set |
| AI Agent - Qualification | @n8n/n8n-nodes-langchain.agent |
| TTS - Qualification | n8n-nodes-base.googleCloudTextToSpeech |
| STT - Qualification Response | n8n-nodes-base.googleCloudSpeechToText |
| IF - Wants Appointment? | n8n-nodes-base.if |
| Get Available Slots | n8n-nodes-base.googleCalendar |
| Calculate Available Slots | n8n-nodes-base.code |
| AI Agent - Offer Slots | @n8n/n8n-nodes-langchain.agent |
| TTS - Offer Slots | n8n-nodes-base.googleCloudTextToSpeech |
| STT - Slot Choice | n8n-nodes-base.googleCloudSpeechToText |
| AI Agent - Parse Choice | @n8n/n8n-nodes-langchain.agent |
| Create Calendar Event | n8n-nodes-base.googleCalendar |
| Save to Database | n8n-nodes-base.postgres |
| TTS - Confirmation | n8n-nodes-base.googleCloudTextToSpeech |
| Send SMS Confirmation | n8n-nodes-base.twilio |
| AI Agent - Continue Conversation | @n8n/n8n-nodes-langchain.agent |
| Respond to Webhook | n8n-nodes-base.respondToWebhook |
| Log Call | n8n-nodes-base.postgres |
| Notify Team (Slack) | n8n-nodes-base.slack |
| TTS - Continue1 | n8n-nodes-base.googleCloudTextToSpeech |

## Raw JSON

```json
{
  "name": "AI Phone Agent - Onboarding & Appointments",
  "nodes": [
    {
      "parameters": {},
      "id": "193b893e-1d5f-4315-830c-d9e3d5e469c3",
      "name": "TTS - Continue",
      "type": "n8n-nodes-base.googleCloudTextToSpeech",
      "typeVersion": 1,
      "position": [
        -3104,
        4480
      ]
    },
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "incoming-call",
        "responseMode": "responseNode",
        "options": {}
      },
      "id": "ae5ffa93-8d27-4597-83c0-9786cf348a2c",
      "name": "Webhook - Incoming Call",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [
        -3296,
        3920
      ],
      "webhookId": "incoming-call-webhook"
    },
    {
      "parameters": {},
      "id": "6a743be9-fa1c-40cf-8122-45572b50d322",
      "name": "TTS - Greeting",
      "type": "n8n-nodes-base.googleCloudTextToSpeech",
      "typeVersion": 1,
      "position": [
        -3104,
        3920
      ]
    },
    {
      "parameters": {},
      "id": "d4e5489a-8cb8-4fce-bc11-cedb01ae8f81",
      "name": "STT - Capture Name",
      "type": "n8n-nodes-base.googleCloudSpeechToText",
      "typeVersion": 1,
      "position": [
        -2896,
        3920
      ]
    },
    {
      "parameters": {
        "options": {}
      },
      "id": "09b5306b-a6bd-492c-840b-52ab39a39602",
      "name": "Set Customer Name",
      "type": "n8n-nodes-base.set",
      "typeVersion": 1,
      "position": [
        -2704,
        3920
      ]
    },
    {
      "parameters": {
        "text": "=Customer said: {{ $json.transcript }}. Extract just their first name and respond warmly saying 'Great! Nice to meet you [NAME]. I'd like to help you get started with our service. Can you tell me what brings you here today?'",
        "options": {
          "systemMessage": "You are a friendly, professional phone agent for onboarding and appointment booking. Keep responses concise and conversational, suitable for phone calls (2-3 sentences max). Be warm but efficient."
        }
      },
      "id": "fd24cd57-d6e7-4801-87a5-7669a8c0728c",
      "name": "AI Agent - Name Response",
      "type": "@n8n/n8n-nodes-langchain.agent",
      "typeVersion": 1.1,
      "position": [
        -2496,
        3920
      ]
    },
    {
      "parameters": {},
      "id": "69626087-c5c1-4c2e-94f5-c93f99b04df2",
      "name": "TTS - Name Response",
      "type": "n8n-nodes-base.googleCloudTextToSpeech",
      "typeVersion": 1,
      "position": [
        -2304,
        3920
      ]
    },
    {
      "parameters": {},
      "id": "221b038c-c4ca-4bf1-bfed-a5347dab52ae",
      "name": "STT - Customer Need",
      "type": "n8n-nodes-base.googleCloudSpeechToText",
      "typeVersion": 1,
      "position": [
        -2096,
        3920
      ]
    },
    {
      "parameters": {
        "options": {}
      },
      "id": "1d14d471-38a0-4bf8-a5be-27ab0aa407bd",
      "name": "Set Customer Need",
      "type": "n8n-nodes-base.set",
      "typeVersion": 1,
      "position": [
        -1904,
        3920
      ]
    },
    {
      "parameters": {
        "text": "=Customer said: {{ $json.transcript }}. Customer name: {{ $node['Set Customer Name'].json.customer_name }}. Analyze their need and ask 2-3 qualifying questions to understand their requirements better. Be conversational and empathetic.",
        "options": {
          "systemMessage": "You are gathering information for onboAI phone agent. Ask relevant questions based on what the customer needs. Keep it natural and friendly. After getting enough info, offer to book an appointment."
        }
      },
      "id": "e2bdd873-605a-4e3d-972d-edf8c634d252",
      "name": "AI Agent - Qualification",
      "type": "@n8n/n8n-nodes-langchain.agent",
      "typeVersion": 1.1,
      "position": [
        -1696,
        3920
      ]
    },
    {
      "parameters": {},
      "id": "e5d2e741-5cfa-412a-85e5-1b303328327f",
      "name": "TTS - Qualification",
      "type": "n8n-nodes-base.googleCloudTextToSpeech",
      "typeVersion": 1,
      "position": [
        -1504,
        3920
      ]
    },
    {
      "parameters": {},
      "id": "ee2138e5-0f05-4cbc-b33c-e8f64a8b1db1",
      "name": "STT - Qualification Response",
      "type": "n8n-nodes-base.googleCloudSpeechToText",
      "typeVersion": 1,
      "position": [
        -1296,
        3920
      ]
    },
    {
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{ $json.transcript.toLowerCase() }}",
              "operation": "contains",
              "value2": "appointment"
            },
            {
              "value1": "={{ $json.transcript.toLowerCase() }}",
              "operation": "contains",
              "value2": "book"
            },
            {
              "value1": "={{ $json.transcript.toLowerCase() }}",
              "operation": "contains",
              "value2": "schedule"
            }
          ]
        },
        "combineOperation": "any"
      },
      "id": "5ed232e9-6017-4a8e-abc6-a4ebd2972ac5",
      "name": "IF - Wants Appointment?",
      "type": "n8n-nodes-base.if",
      "typeVersion": 1,
      "position": [
        -1104,
        3920
      ]
    },
    {
      "parameters": {
        "operation": "get",
        "calendar": {
          "__rl": true,
          "mode": "list",
          "value": ""
        },
        "options": {}
      },
      "id": "f52dec0e-97b3-4eb2-8227-a6242860c929",
      "name": "Get Available Slots",
      "type": "n8n-nodes-base.googleCalendar",
      "typeVersion": 1,
      "position": [
        -896,
        3808
      ]
    },
    {
      "parameters": {
        "jsCode": "const events = $input.all();\nconst businessHours = {\n  start: 9,\n  end: 17\n};\n\nconst workDays = [1, 2, 3, 4, 5];\nconst slots = [];\nconst now = new Date();\n\nfor (let i = 1; i <= 14; i++) {\n  const date = new Date(now);\n  date.setDate(date.getDate() + i);\n  \n  if (!workDays.includes(date.getDay())) continue;\n  \n  for (let hour = businessHours.start; hour < businessHours.end; hour++) {\n    const slotStart = new Date(date);\n    slotStart.setHours(hour, 0, 0, 0);\n    \n    const slotEnd = new Date(slotStart);\n    slotEnd.setHours(hour + 1);\n    \n    const isBooked = events.some(event => {\n      const eventStart = new Date(event.json.start.dateTime);\n      const eventEnd = new Date(event.json.end.dateTime);\n      return slotStart < eventEnd && slotEnd > eventStart;\n    });\n    \n    if (!isBooked) {\n      slots.push({\n        json: {\n          date: slotStart.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' }),\n          time: slotStart.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' }),\n          datetime: slotStart.toISOString()\n        }\n      });\n    }\n  }\n  \n  if (slots.length >= 5) break;\n}\n\nreturn slots.slice(0, 5);"
      },
      "id": "7b5925fa-7f01-4fc0-abc3-3f143c821fce",
      "name": "Calculate Available Slots",
      "type": "n8n-nodes-base.code",
      "typeVersion": 1,
      "position": [
        -704,
        3808
      ]
    },
    {
      "parameters": {
        "text": "=Available slots: {{ $json.map(slot => slot.date + ' at ' + slot.time).join(', ') }}. Customer name: {{ $node['Set Customer Name'].json.customer_name }}. Offer these appointment times in a natural, conversational way. Ask which works best for them.",
        "options": {
          "systemMessage": "You are booking an appointment. Present the available times clearly and ask the customer to choose one. Be helpful and accommodating."
        }
      },
      "id": "4b551597-a03f-400b-96b3-b9ed6ce89dd8",
      "name": "AI Agent - Offer Slots",
      "type": "@n8n/n8n-nodes-langchain.agent",
      "typeVersion": 1.1,
      "position": [
        -496,
        3808
      ]
    },
    {
      "parameters": {},
      "id": "89a73a76-ac5d-4f24-b975-df27912aed1c",
      "name": "TTS - Offer Slots",
      "type": "n8n-nodes-base.googleCloudTextToSpeech",
      "typeVersion": 1,
      "position": [
        -304,
        3808
      ]
    },
    {
      "parameters": {},
      "id": "5cb80dfa-92fe-4fa2-910f-0a7de6013d75",
      "name": "STT - Slot Choice",
      "type": "n8n-nodes-base.googleCloudSpeechToText",
      "typeVersion": 1,
      "position": [
        -96,
        3808
      ]
    },
    {
      "parameters": {
        "text": "=Customer said: {{ $json.transcript }}. Available slots were: {{ $node['Calculate Available Slots'].json.map(slot => slot.date + ' at ' + slot.time).join(', ') }}. Determine which slot they chose and return ONLY the exact date and time in format: 'YYYY-MM-DDTHH:mm:ss'",
        "options": {
          "systemMessage": "Extract the chosen appointment time from customer's response. Match it to one of the available slots. Return only the ISO datetime string, nothing else."
        }
      },
      "id": "1fee6b9e-e0bb-4cfe-ad89-a85b59a53d17",
      "name": "AI Agent - Parse Choice",
      "type": "@n8n/n8n-nodes-langchain.agent",
      "typeVersion": 1.1,
      "position": [
        112,
        3808
      ]
    },
    {
      "parameters": {
        "calendar": {
          "__rl": true,
          "mode": "list",
          "value": ""
        },
        "start": "={{ $json.response }}",
        "end": "={{ $now.plus({hours: 1}).toISO() }}",
        "additionalFields": {}
      },
      "id": "762a0120-b7f2-4b6f-8100-3699df4714d1",
      "name": "Create Calendar Event",
      "type": "n8n-nodes-base.googleCalendar",
      "typeVersion": 1,
      "position": [
        304,
        3808
      ]
    },
    {
      "parameters": {
        "operation": "create",
        "additionalFields": {}
      },
      "id": "7124304e-e9c3-40db-b721-e7e55ec9d80e",
      "name": "Save to Database",
      "type": "n8n-nodes-base.postgres",
      "typeVersion": 1,
      "position": [
        512,
        3808
      ]
    },
    {
      "parameters": {},
      "id": "aed91d76-8464-47a9-82c3-f1e017d62443",
      "name": "TTS - Confirmation",
      "type": "n8n-nodes-base.googleCloudTextToSpeech",
      "typeVersion": 1,
      "position": [
        704,
        3808
      ]
    },
    {
      "parameters": {
        "to": "={{ $node['Webhook - Incoming Call'].json.from }}",
        "message": "=Thank you for calling! Your appointment is confirmed for {{ $node['AI Agent - Parse Choice'].json.response }}. We look forward to seeing you!",
        "options": {}
      },
      "id": "7a616bb9-2d73-41e4-b24d-7e736af81ba3",
      "name": "Send SMS Confirmation",
      "type": "n8n-nodes-base.twilio",
      "typeVersion": 1,
      "position": [
        912,
        3808
      ]
    },
    {
      "parameters": {
        "text": "=Customer said: {{ $json.transcript }}. Continue the conversation naturally. Gather more information or loop back to asking if they want to schedule an appointment.",
        "options": {
          "systemMessage": "Continue the onboarding conversation. Be helpful and guide the customer toward booking an appointment when appropriate."
        }
      },
      "id": "380e18d1-c574-4425-86a7-4dbf6b732eed",
      "name": "AI Agent - Continue Conversation",
      "type": "@n8n/n8n-nodes-langchain.agent",
      "typeVersion": 1.1,
      "position": [
        -896,
        4016
      ]
    },
    {
      "parameters": {
        "respondWith": "allIncomingItems",
        "options": {}
      },
      "id": "00aedab0-54df-488a-9e29-3de2bf11d1d2",
      "name": "Respond to Webhook",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1,
      "position": [
        1104,
        3920
      ]
    },
    {
      "parameters": {
        "operation": "create",
        "additionalFields": {}
      },
      "id": "bf0d0be2-f4b9-45b6-87e4-c8c1282a925e",
      "name": "Log Call",
      "type": "n8n-nodes-base.postgres",
      "typeVersion": 1,
      "position": [
        912,
        4016
      ]
    },
    {
      "parameters": {
        "authentication": "oAuth2",
        "operation": "sendMessage"
      },
      "id": "dda80406-ac82-4c0a-a578-7a5f4d4ba69b",
      "name": "Notify Team (Slack)",
      "type": "n8n-nodes-base.slack",
      "typeVersion": 1,
      "position": [
        704,
        4016
      ]
    },
    {
      "parameters": {},
      "id": "3dba2c12-0d23-4211-88c5-fb6b51f780df",
      "name": "TTS - Continue1",
      "type": "n8n-nodes-base.googleCloudTextToSpeech",
      "typeVersion": 1,
      "position": [
        -704,
        4016
      ]
    }
  ],
  "connections": {
    "Set Customer Name": {
      "main": [
        [
          {
            "node": "AI Agent - Name Response",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Set Customer Need": {
      "main": [
        [
          {
            "node": "AI Agent - Qualification",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "IF - Wants Appointment?": {
      "main": [
        [
          {
            "node": "Get Available Slots",
            "type": "main",
            "index": 0
          }
        ],
        [
          {
            "node": "AI Agent - Continue Conversation",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Get Available Slots": {
      "main": [
        [
          {
            "node": "Calculate Available Slots",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Calculate Available Slots": {
      "main": [
        [
          {
            "node": "AI Agent - Offer Slots",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "AI Agent - Parse Choice": {
      "main": [
        [
          {
            "node": "Create Calendar Event",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Create Calendar Event": {
      "main": [
        [
          {
            "node": "Save to Database",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Send SMS Confirmation": {
      "main": [
        [
          {
            "node": "Notify Team (Slack)",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Notify Team (Slack)": {
      "main": [
        [
          {
            "node": "Log Call",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Log Call": {
      "main": [
        [
          {
            "node": "Respond to Webhook",
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
  "meta": {
    "templateCredsSetupCompleted": true
  }
}
```
