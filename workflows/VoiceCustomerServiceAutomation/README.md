# Workflow: Voice Customer Service Automation

## Overview

This document provides an overview of the 'Voice Customer Service Automation' workflow.

## Workflow Steps (Nodes)

| Step Name | Type |
|-----------|------|
| Webhook Trigger | n8n-nodes-base.webhook |
| Speech to Text | n8n-nodes-base.httpRequest |
| Extract Data | n8n-nodes-base.code |
| Order Query | n8n-nodes-base.if |
| Refund Request | n8n-nodes-base.if |
| Tech Support | n8n-nodes-base.if |
| Get Order Info | n8n-nodes-base.postgres |
| Get Support History | n8n-nodes-base.postgres |
| Build Context | n8n-nodes-base.code |
| Generate AI Response | @n8n/n8n-nodes-langchain.lmChatOpenAi |
| Format Response | n8n-nodes-base.code |
| Text to Speech | n8n-nodes-base.httpRequest |
| Log Conversation | n8n-nodes-base.postgres |
| Check Escalation | n8n-nodes-base.if |
| Send Escalation Email | n8n-nodes-base.emailSend |
| Send Response | n8n-nodes-base.respondToWebhook |

## Raw JSON

```json
{
  "name": "Voice Customer Service Automation",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "voice-inquiry",
        "responseMode": "responseNode",
        "options": {}
      },
      "id": "1918b389-7631-4363-9119-219d495b8428",
      "name": "Webhook Trigger",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1.1,
      "position": [
        -208,
        80
      ],
      "webhookId": "voice-cs-webhook"
    },
    {
      "parameters": {
        "url": "https://api.openai.com/v1/audio/transcriptions",
        "authentication": "predefinedCredentialType",
        "nodeCredentialType": "openAiApi",
        "sendBody": true,
        "specifyBody": "formData",
        "options": {}
      },
      "id": "a06e71e5-c1d7-4a8b-bb46-8baa4a7b7818",
      "name": "Speech to Text",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [
        16,
        80
      ],
      "executeOnce": false
    },
    {
      "parameters": {
        "jsCode": "const transcript = $input.first().json.text;\nconst phoneNumber = $('Webhook Trigger').first().json.body.phoneNumber || 'unknown';\n\nreturn {\n  transcript: transcript,\n  phoneNumber: phoneNumber,\n  timestamp: new Date().toISOString()\n};"
      },
      "id": "4ec2bbd1-4f70-4899-bab9-f667e831c34b",
      "name": "Extract Data",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        240,
        80
      ]
    },
    {
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{ $json.transcript.toLowerCase() }}",
              "operation": "regex",
              "value2": "order|track|shipping|delivery|package|status"
            }
          ]
        },
        "options": {}
      },
      "id": "ae7780f8-e26e-48bf-b65f-6ebfdb6a0e73",
      "name": "Order Query",
      "type": "n8n-nodes-base.if",
      "typeVersion": 2,
      "position": [
        448,
        -32
      ]
    },
    {
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{ $json.transcript.toLowerCase() }}",
              "operation": "regex",
              "value2": "refund|return|money back|cancel"
            }
          ]
        },
        "options": {}
      },
      "id": "dba86cd4-f875-43bf-be4e-4b75856c8a5d",
      "name": "Refund Request",
      "type": "n8n-nodes-base.if",
      "typeVersion": 2,
      "position": [
        448,
        128
      ]
    },
    {
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{ $json.transcript.toLowerCase() }}",
              "operation": "regex",
              "value2": "help|support|issue|problem|not working|broken"
            }
          ]
        },
        "options": {}
      },
      "id": "c1742c80-139a-4981-8f3a-cb970d1f6cc0",
      "name": "Tech Support",
      "type": "n8n-nodes-base.if",
      "typeVersion": 2,
      "position": [
        448,
        272
      ]
    },
    {
      "parameters": {
        "operation": "executeQuery",
        "query": "=SELECT order_id, status, tracking_number, estimated_delivery, product_name, order_date\nFROM orders \nWHERE customer_phone = '{{ $json.phoneNumber }}'\nORDER BY order_date DESC \nLIMIT 1",
        "options": {}
      },
      "id": "6f647230-ea6f-4dc8-97f9-ac940ded8547",
      "name": "Get Order Info",
      "type": "n8n-nodes-base.postgres",
      "typeVersion": 2.4,
      "position": [
        672,
        -32
      ]
    },
    {
      "parameters": {
        "operation": "executeQuery",
        "query": "=SELECT ticket_id, issue_type, status, created_at, resolution\nFROM support_tickets \nWHERE customer_phone = '{{ $json.phoneNumber }}'\nORDER BY created_at DESC \nLIMIT 3",
        "options": {}
      },
      "id": "854d8a00-3116-4d35-aa41-245f90bd9c65",
      "name": "Get Support History",
      "type": "n8n-nodes-base.postgres",
      "typeVersion": 2.4,
      "position": [
        672,
        272
      ]
    },
    {
      "parameters": {
        "jsCode": "// Gather all context from previous nodes\nconst transcript = $('Extract Data').first().json.transcript;\nconst phoneNumber = $('Extract Data').first().json.phoneNumber;\n\n// Try to get order info\nlet orderContext = '';\ntry {\n  const orderData = $('Get Order Info').first().json;\n  if (orderData && orderData.order_id) {\n    orderContext = `\\nOrder Information:\\n- Order ID: ${orderData.order_id}\\n- Status: ${orderData.status}\\n- Product: ${orderData.product_name}\\n- Tracking: ${orderData.tracking_number || 'N/A'}\\n- Estimated Delivery: ${orderData.estimated_delivery || 'N/A'}`;\n  }\n} catch (e) {\n  orderContext = '\\nNo order information found.';\n}\n\n// Try to get support history\nlet supportContext = '';\ntry {\n  const supportData = $('Get Support History').all();\n  if (supportData && supportData.length > 0) {\n    supportContext = '\\n\\nPrevious Support Tickets:\\n';\n    supportData.forEach((ticket, i) => {\n      supportContext += `${i + 1}. ${ticket.json.issue_type} - ${ticket.json.status} (${ticket.json.created_at})\\n`;\n    });\n  }\n} catch (e) {\n  supportContext = '\\nNo support history found.';\n}\n\nreturn {\n  transcript: transcript,\n  phoneNumber: phoneNumber,\n  context: orderContext + supportContext,\n  timestamp: new Date().toISOString()\n};"
      },
      "id": "6d35096c-b0e3-4d99-aba5-286e03c14922",
      "name": "Build Context",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        896,
        128
      ]
    },
    {
      "parameters": {
        "model": "gpt-4-turbo-preview",
        "options": {
          "maxTokens": 500,
          "temperature": 0.7
        }
      },
      "id": "3d56d901-045a-4b51-a2ad-ed916ca2ec77",
      "name": "Generate AI Response",
      "type": "@n8n/n8n-nodes-langchain.lmChatOpenAi",
      "typeVersion": 1,
      "position": [
        464,
        480
      ]
    },
    {
      "parameters": {
        "jsCode": "const response = $input.first().json.text || $input.first().json.content;\nconst buildContext = $('Build Context').first().json;\n\nreturn {\n  transcript: buildContext.transcript,\n  aiResponse: response,\n  phoneNumber: buildContext.phoneNumber,\n  timestamp: buildContext.timestamp,\n  needsEscalation: /escalate|human|agent|representative|speak to someone/i.test(response)\n};"
      },
      "id": "aebc172f-dfc5-4e71-a4c3-7864557ec2f9",
      "name": "Format Response",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        -480,
        416
      ]
    },
    {
      "parameters": {
        "url": "https://api.openai.com/v1/audio/speech",
        "authentication": "predefinedCredentialType",
        "nodeCredentialType": "openAiApi",
        "sendBody": true,
        "specifyBody": "json",
        "jsonBody": "={\n  \"model\": \"tts-1\",\n  \"input\": \"{{ $json.aiResponse }}\",\n  \"voice\": \"nova\",\n  \"response_format\": \"mp3\"\n}",
        "options": {
          "response": {
            "response": {
              "responseFormat": "file"
            }
          }
        }
      },
      "id": "9bdaf8d0-56e6-4e1a-98c3-bd897634544b",
      "name": "Text to Speech",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [
        -256,
        320
      ]
    },
    {
      "parameters": {
        "schema": "public",
        "table": "conversation_logs",
        "columns": {
          "mappingMode": "defineBelow",
          "value": {
            "customer_phone": "={{ $('Format Response').first().json.phoneNumber }}",
            "transcript": "={{ $('Format Response').first().json.transcript }}",
            "ai_response": "={{ $('Format Response').first().json.aiResponse }}",
            "needs_escalation": "={{ $('Format Response').first().json.needsEscalation }}",
            "created_at": "={{ $('Format Response').first().json.timestamp }}"
          }
        },
        "options": {}
      },
      "id": "1a8f7220-4b02-466d-b8a6-81d87d814cc2",
      "name": "Log Conversation",
      "type": "n8n-nodes-base.postgres",
      "typeVersion": 2.4,
      "position": [
        -32,
        320
      ]
    },
    {
      "parameters": {
        "conditions": {
          "boolean": [
            {
              "value1": "={{ $('Format Response').first().json.needsEscalation }}",
              "value2": true
            }
          ]
        },
        "options": {}
      },
      "id": "acd7d937-8ca1-419c-9091-675dbc3ad4fa",
      "name": "Check Escalation",
      "type": "n8n-nodes-base.if",
      "typeVersion": 2,
      "position": [
        -32,
        512
      ]
    },
    {
      "parameters": {
        "fromEmail": "noreply@yourcompany.com",
        "toEmail": "support@yourcompany.com",
        "subject": "=Customer Service Escalation - {{ $('Format Response').first().json.phoneNumber }}",
        "options": {}
      },
      "id": "49cbd51b-fc03-4920-afa8-5a99de5024ee",
      "name": "Send Escalation Email",
      "type": "n8n-nodes-base.emailSend",
      "typeVersion": 2.1,
      "position": [
        192,
        512
      ],
      "webhookId": "832203ec-fd64-444c-b30e-37d21a9619c1"
    },
    {
      "parameters": {
        "respondWith": "json",
        "responseBody": "={\n  \"success\": true,\n  \"transcript\": \"{{ $('Format Response').first().json.transcript }}\",\n  \"response\": \"{{ $('Format Response').first().json.aiResponse }}\",\n  \"audioUrl\": \"{{ $json.binary.data }}\",\n  \"needsEscalation\": {{ $('Format Response').first().json.needsEscalation }},\n  \"timestamp\": \"{{ $('Format Response').first().json.timestamp }}\"\n}",
        "options": {}
      },
      "id": "52905156-a863-4413-bca0-d59189243eab",
      "name": "Send Response",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1.1,
      "position": [
        192,
        320
      ]
    }
  ],
  "connections": {
    "Webhook Trigger": {
      "main": [
        [
          {
            "node": "Speech to Text",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Speech to Text": {
      "main": [
        [
          {
            "node": "Extract Data",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Extract Data": {
      "main": [
        [
          {
            "node": "Order Query",
            "type": "main",
            "index": 0
          },
          {
            "node": "Refund Request",
            "type": "main",
            "index": 0
          },
          {
            "node": "Tech Support",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Order Query": {
      "main": [
        [
          {
            "node": "Get Order Info",
            "type": "main",
            "index": 0
          }
        ],
        [
          {
            "node": "Build Context",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Refund Request": {
      "main": [
        [
          {
            "node": "Get Order Info",
            "type": "main",
            "index": 0
          }
        ],
        [
          {
            "node": "Build Context",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Tech Support": {
      "main": [
        [
          {
            "node": "Get Support History",
            "type": "main",
            "index": 0
          }
        ],
        [
          {
            "node": "Build Context",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Get Order Info": {
      "main": [
        [
          {
            "node": "Build Context",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Get Support History": {
      "main": [
        [
          {
            "node": "Build Context",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Format Response": {
      "main": [
        [
          {
            "node": "Text to Speech",
            "type": "main",
            "index": 0
          },
          {
            "node": "Check Escalation",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Text to Speech": {
      "main": [
        [
          {
            "node": "Log Conversation",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Log Conversation": {
      "main": [
        [
          {
            "node": "Send Response",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Check Escalation": {
      "main": [
        [
          {
            "node": "Send Escalation Email",
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
