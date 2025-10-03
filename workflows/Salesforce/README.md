# Workflow: Salesforce

## Overview

This document provides an overview of the 'Salesforce' workflow.

## Workflow Steps (Nodes)

| Step Name | Type |
|-----------|------|
| Start | n8n-nodes-base.start |
| Chatbot Webhook | n8n-nodes-base.webhook |
| Chatbot Intent Processing | n8n-nodes-base.code |
| Switch | n8n-nodes-base.switch |
| Fetch Amazon Search Results1 | n8n-nodes-base.salesforce |
| Fetch Amazon Search Results2 | n8n-nodes-base.salesforce |
| Extract Product Listings1 | n8n-nodes-base.salesforce |
| Extract Product Listings2 | n8n-nodes-base.salesforce |
| Process Product Data1 | n8n-nodes-base.code |
| Process Product Data2 | n8n-nodes-base.code |
| Grok Chat Model1 | n8n-nodes-base.openAi |
| Grok Chat Model2 | n8n-nodes-base.openAi |
| Normalize Chat Input | n8n-nodes-base.code |
| Voice Message Received | n8n-nodes-base.webhook |
| Structured Output Parser1 | n8n-nodes-base.code |
| Structured Output Parser2 | n8n-nodes-base.code |
| Basic LLM Chain1 | n8n-nodes-base.salesforce |
| Basic LLM Chain2 | n8n-nodes-base.salesforce |
| Low Stock Alert Agent | n8n-nodes-base.code |
| IF (Forecast Success) | n8n-nodes-base.if |
| Format Low Stock Email for Chat | n8n-nodes-base.code |
| Respond to Webhook | n8n-nodes-base.respondToWebhook |
| Low Stock Email Alert | n8n-nodes-base.emailSend |
| Sales Data Preparation | n8n-nodes-base.code |
| Merge With Forecast | n8n-nodes-base.httpRequest |
| Enhance Forecast | n8n-nodes-base.code |
| Preprocess Detail | n8n-nodes-base.code |
| Prepare for Model | n8n-nodes-base.code |
| Train and Predict | n8n-nodes-base.code |
| Forecast Sales | n8n-nodes-base.code |
| Format for Visualization | n8n-nodes-base.code |
| Write Forecast to Google Sheets | n8n-nodes-base.googleSheets |
| Generate Forecast Email HTML | n8n-nodes-base.code |
| Send Forecast Email | n8n-nodes-base.emailSend |
| Send to Dashboard | n8n-nodes-base.httpRequest |
| Generate Sample Data | n8n-nodes-base.httpRequest |
| AI Response Check | n8n-nodes-base.code |
| Parse AI Response | n8n-nodes-base.code |
| Email Market Report | n8n-nodes-base.emailSend |
| Save Market Analysis | n8n-nodes-base.googleDocs |
| Generate Market Email Body | n8n-nodes-base.code |
| Error Message (if forecast) | n8n-nodes-base.if |
| Handle Error | n8n-nodes-base.code |
| When clicking ‘Execute workflow’ | n8n-nodes-base.manualTrigger |
| MCP Server Trigger | @n8n/n8n-nodes-langchain.mcpTrigger |

## Raw JSON

```json
{
  "name": "Salesforce",
  "nodes": [
    {
      "parameters": {},
      "id": "d58fffcf-5599-40d9-a1eb-4ed10953b840",
      "name": "Start",
      "type": "n8n-nodes-base.start",
      "typeVersion": 1,
      "position": [
        -176,
        224
      ]
    },
    {
      "parameters": {
        "path": "chatbot-interaction",
        "options": {}
      },
      "id": "cb47d346-26a3-472b-b447-298bfcd1821d",
      "name": "Chatbot Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [
        -368,
        -128
      ],
      "webhookId": "chatbot-interaction"
    },
    {
      "parameters": {},
      "id": "09186667-e9f6-4db2-9e65-6ac635fab9f3",
      "name": "Chatbot Intent Processing",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        -160,
        -128
      ]
    },
    {
      "parameters": {},
      "id": "a764a202-e19b-42d9-95d1-cedea8dbfaf9",
      "name": "Switch",
      "type": "n8n-nodes-base.switch",
      "typeVersion": 1,
      "position": [
        48,
        -80
      ]
    },
    {
      "parameters": {
        "resource": "search",
        "query": "SELECT Id, Name, QuantityOnHand FROM Product2 WHERE QuantityOnHand < 50"
      },
      "id": "6ca0f8c7-f644-42a6-8fd7-7d4a24787011",
      "name": "Fetch Amazon Search Results1",
      "type": "n8n-nodes-base.salesforce",
      "typeVersion": 1,
      "position": [
        240,
        -192
      ]
    },
    {
      "parameters": {
        "resource": "search",
        "query": "SELECT Id, Name, ListPrice, Market_Trend__c FROM Product2"
      },
      "id": "75fb7811-962b-4412-8d13-1029dfd0ae41",
      "name": "Fetch Amazon Search Results2",
      "type": "n8n-nodes-base.salesforce",
      "typeVersion": 1,
      "position": [
        256,
        512
      ]
    },
    {
      "parameters": {
        "operation": "getAll",
        "returnAll": true,
        "options": {}
      },
      "id": "a6488a88-dcb1-4635-894a-3226ebc0417b",
      "name": "Extract Product Listings1",
      "type": "n8n-nodes-base.salesforce",
      "typeVersion": 1,
      "position": [
        448,
        -272
      ]
    },
    {
      "parameters": {
        "operation": "getAll",
        "returnAll": true,
        "options": {}
      },
      "id": "c4daa3e2-9027-429c-b88d-a6820686b444",
      "name": "Extract Product Listings2",
      "type": "n8n-nodes-base.salesforce",
      "typeVersion": 1,
      "position": [
        448,
        512
      ]
    },
    {
      "parameters": {},
      "id": "0299728b-3654-45e7-8e30-3605bff0332d",
      "name": "Process Product Data1",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        640,
        -368
      ]
    },
    {
      "parameters": {},
      "id": "eb56c351-4d51-407a-bde7-30eda54430bc",
      "name": "Process Product Data2",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        624,
        544
      ]
    },
    {
      "parameters": {
        "prompt": "Analyze the following low stock data and provide recommendations:\n{{$json}}",
        "options": {},
        "requestOptions": {}
      },
      "id": "1e76206b-84e7-4d1f-a7f1-6a52351258ae",
      "name": "Grok Chat Model1",
      "type": "n8n-nodes-base.openAi",
      "typeVersion": 1,
      "position": [
        -160,
        -32
      ]
    },
    {
      "parameters": {
        "prompt": "Analyze market trends for: {{$json}}",
        "options": {},
        "requestOptions": {}
      },
      "id": "19fd5d39-4796-4b6d-aff6-69e9d92f4a12",
      "name": "Grok Chat Model2",
      "type": "n8n-nodes-base.openAi",
      "typeVersion": 1,
      "position": [
        448,
        -32
      ]
    },
    {
      "parameters": {},
      "id": "962c128b-04e7-4242-8f34-861e3fa768b0",
      "name": "Normalize Chat Input",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        -160,
        -240
      ]
    },
    {
      "parameters": {
        "path": "6fa82a3e-242d-47d0-91b4-24811f6e5941",
        "options": {}
      },
      "id": "f78eaec0-ecd5-4fcb-aaf7-6c02d637ea61",
      "name": "Voice Message Received",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [
        -384,
        32
      ],
      "webhookId": "6fa82a3e-242d-47d0-91b4-24811f6e5941"
    },
    {
      "parameters": {},
      "id": "1d04cd7d-fab5-4403-a012-935bbf02dc98",
      "name": "Structured Output Parser1",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        48,
        96
      ]
    },
    {
      "parameters": {},
      "id": "9b372aa9-d596-4c04-9288-865b9fde51b6",
      "name": "Structured Output Parser2",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        640,
        -80
      ]
    },
    {
      "parameters": {
        "resource": "record"
      },
      "id": "9ebfc186-ab1d-4b1d-8610-3eeafb854de8",
      "name": "Basic LLM Chain1",
      "type": "n8n-nodes-base.salesforce",
      "typeVersion": 1,
      "position": [
        48,
        -224
      ]
    },
    {
      "parameters": {
        "resource": "record"
      },
      "id": "b8267861-33d6-4e1e-b9dc-3a3466219690",
      "name": "Basic LLM Chain2",
      "type": "n8n-nodes-base.salesforce",
      "typeVersion": 1,
      "position": [
        640,
        -224
      ]
    },
    {
      "parameters": {},
      "id": "113134c0-5b85-4204-9d98-c16e183d3465",
      "name": "Low Stock Alert Agent",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        240,
        -32
      ]
    },
    {
      "parameters": {
        "conditions": {
          "boolean": [
            {
              "value1": "={{$json.alert}}",
              "value2": true
            }
          ]
        }
      },
      "id": "6b255817-b566-4df1-89bd-f4c024ad5a74",
      "name": "IF (Forecast Success)",
      "type": "n8n-nodes-base.if",
      "typeVersion": 1,
      "position": [
        448,
        96
      ]
    },
    {
      "parameters": {},
      "id": "32fb412d-71f7-4fd1-9299-6cabdbd94ef7",
      "name": "Format Low Stock Email for Chat",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        640,
        64
      ]
    },
    {
      "parameters": {
        "respondWith": "text",
        "responseBody": "={{$json.formattedMessage}}",
        "options": {}
      },
      "id": "7f90e37a-d098-430e-9337-00bf36367d4a",
      "name": "Respond to Webhook",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1,
      "position": [
        448,
        -144
      ]
    },
    {
      "parameters": {
        "operation": "sendEmail"
      },
      "id": "84aad0c6-f51c-497a-81fe-6ecdd812a2e4",
      "name": "Low Stock Email Alert",
      "type": "n8n-nodes-base.emailSend",
      "typeVersion": 2,
      "position": [
        848,
        80
      ],
      "webhookId": "d720da03-e958-4468-b56b-4b49f52af7b8"
    },
    {
      "parameters": {},
      "id": "8ef15cca-af8a-43ab-8478-540eb1577445",
      "name": "Sales Data Preparation",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        48,
        352
      ]
    },
    {
      "parameters": {
        "method": "POST",
        "url": "https://api.external-forecast.com/predict",
        "options": {}
      },
      "id": "25609a97-4ebe-4609-8205-b0205e91e879",
      "name": "Merge With Forecast",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 3,
      "position": [
        256,
        368
      ]
    },
    {
      "parameters": {},
      "id": "5dd842bd-333e-4cfa-8d00-55defa92efd8",
      "name": "Enhance Forecast",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        448,
        368
      ]
    },
    {
      "parameters": {},
      "id": "63f7cb96-aabd-4a36-a6ea-f7533f187a56",
      "name": "Preprocess Detail",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        640,
        368
      ]
    },
    {
      "parameters": {},
      "id": "a2f0d0b2-b409-4e7e-af4e-dbeabecff696",
      "name": "Prepare for Model",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        832,
        368
      ]
    },
    {
      "parameters": {},
      "id": "5f652a46-f2c5-4b62-95d0-c477f5e4d004",
      "name": "Train and Predict",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        1040,
        368
      ]
    },
    {
      "parameters": {},
      "id": "d315734e-f39f-4d68-8c53-bb4a91f41f31",
      "name": "Forecast Sales",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        1248,
        368
      ]
    },
    {
      "parameters": {},
      "id": "2c0f9bf3-235e-4604-b8d1-1bcc995b0d32",
      "name": "Format for Visualization",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        1392,
        176
      ]
    },
    {
      "parameters": {
        "operation": "upload",
        "documentId": {
          "__rl": true,
          "mode": "list",
          "value": ""
        }
      },
      "id": "a1a92611-c71a-4e17-ad52-3ad0288f6934",
      "name": "Write Forecast to Google Sheets",
      "type": "n8n-nodes-base.googleSheets",
      "typeVersion": 3,
      "position": [
        1584,
        -48
      ]
    },
    {
      "parameters": {},
      "id": "37f1dab2-9426-435c-b3c9-60eafa9e706d",
      "name": "Generate Forecast Email HTML",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        1648,
        368
      ]
    },
    {
      "parameters": {
        "operation": "sendEmail"
      },
      "id": "bffb2ef0-7936-4f08-b0f1-596a65e838c1",
      "name": "Send Forecast Email",
      "type": "n8n-nodes-base.emailSend",
      "typeVersion": 2,
      "position": [
        1840,
        368
      ],
      "webhookId": "3669175b-d3fc-46a0-bcb7-8dedf0dd9d3c"
    },
    {
      "parameters": {
        "options": {}
      },
      "id": "1de67322-f88a-4aa4-9d7a-fd0ef3b5b9bc",
      "name": "Send to Dashboard",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 3,
      "position": [
        1840,
        160
      ]
    },
    {
      "parameters": {
        "options": {}
      },
      "id": "b37da585-8c49-4914-aae9-e92ba798093c",
      "name": "Generate Sample Data",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 3,
      "position": [
        240,
        112
      ]
    },
    {
      "parameters": {},
      "id": "aad84cf2-eb3e-4b29-907f-04c636388f05",
      "name": "AI Response Check",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        640,
        192
      ]
    },
    {
      "parameters": {},
      "id": "b1ba4a7f-f22f-4baa-8efc-7c39d57ba4ae",
      "name": "Parse AI Response",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        848,
        -96
      ]
    },
    {
      "parameters": {
        "operation": "sendEmail"
      },
      "id": "4614052b-e21b-4524-bbf6-f542d810914c",
      "name": "Email Market Report",
      "type": "n8n-nodes-base.emailSend",
      "typeVersion": 2,
      "position": [
        1040,
        -256
      ],
      "webhookId": "f7e38ce6-ad18-4e77-84a3-117e8cebf447"
    },
    {
      "parameters": {
        "operation": "appendOrUpdate"
      },
      "id": "337832fb-ca5f-48d3-a87c-012611415b9e",
      "name": "Save Market Analysis",
      "type": "n8n-nodes-base.googleDocs",
      "typeVersion": 2,
      "position": [
        848,
        -256
      ]
    },
    {
      "parameters": {},
      "id": "d811759b-0dbf-4a6d-951f-1ce8b8a95e23",
      "name": "Generate Market Email Body",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        1040,
        -96
      ]
    },
    {
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{$json.alertLevel}}",
              "operation": "equals",
              "value2": "Critical"
            }
          ]
        }
      },
      "id": "a1b4dba8-9113-4e1a-bc06-b4c48b24f6df",
      "name": "Error Message (if forecast)",
      "type": "n8n-nodes-base.if",
      "typeVersion": 1,
      "position": [
        848,
        160
      ]
    },
    {
      "parameters": {},
      "id": "adce4680-ec67-4478-bd0b-508c2ef420fe",
      "name": "Handle Error",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        1040,
        112
      ]
    },
    {
      "parameters": {},
      "type": "n8n-nodes-base.manualTrigger",
      "typeVersion": 1,
      "position": [
        1792,
        -48
      ],
      "id": "d3596d66-7e1e-4e53-99e4-979813e4bb5e",
      "name": "When clicking \u2018Execute workflow\u2019"
    },
    {
      "parameters": {
        "path": "9c340c41-c506-4a09-80bf-266e5e89d419"
      },
      "type": "@n8n/n8n-nodes-langchain.mcpTrigger",
      "typeVersion": 2,
      "position": [
        -288,
        160
      ],
      "id": "38bfcacb-52e6-4ec3-a17c-a4f537548c76",
      "name": "MCP Server Trigger",
      "webhookId": "9c340c41-c506-4a09-80bf-266e5e89d419"
    }
  ],
  "connections": {
    "Start": {
      "main": [
        [
          {
            "node": "Generate Sample Data",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Chatbot Webhook": {
      "main": [
        [
          {
            "node": "Normalize Chat Input",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Normalize Chat Input": {
      "main": [
        [
          {
            "node": "Chatbot Intent Processing",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Chatbot Intent Processing": {
      "main": [
        [
          {
            "node": "Basic LLM Chain1",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Basic LLM Chain1": {
      "main": [
        [
          {
            "node": "Switch",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Switch": {
      "main": [
        [
          {
            "node": "Fetch Amazon Search Results1",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Voice Message Received": {
      "main": [
        [
          {
            "node": "Grok Chat Model1",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Grok Chat Model1": {
      "main": [
        [
          {
            "node": "Structured Output Parser1",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Structured Output Parser1": {
      "main": [
        [
          {
            "node": "Low Stock Alert Agent",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Fetch Amazon Search Results1": {
      "main": [
        [
          {
            "node": "Extract Product Listings1",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Extract Product Listings1": {
      "main": [
        [
          {
            "node": "Process Product Data1",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Process Product Data1": {
      "main": [
        [
          {
            "node": "Basic LLM Chain2",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Basic LLM Chain2": {
      "main": [
        [
          {
            "node": "AI Response Check",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "AI Response Check": {
      "main": [
        [
          {
            "node": "Parse AI Response",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Parse AI Response": {
      "main": [
        [
          {
            "node": "Save Market Analysis",
            "type": "main",
            "index": 0
          },
          {
            "node": "Generate Market Email Body",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Save Market Analysis": {
      "main": [
        [
          {
            "node": "Email Market Report",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Generate Market Email Body": {
      "main": [
        [
          {
            "node": "Grok Chat Model2",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Grok Chat Model2": {
      "main": [
        [
          {
            "node": "Structured Output Parser2",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Structured Output Parser2": {
      "main": [
        [
          {
            "node": "Respond to Webhook",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Low Stock Alert Agent": {
      "main": [
        [
          {
            "node": "IF (Forecast Success)",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "IF (Forecast Success)": {
      "main": [
        [
          {
            "node": "Format Low Stock Email for Chat",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Format Low Stock Email for Chat": {
      "main": [
        [
          {
            "node": "Low Stock Email Alert",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Generate Sample Data": {
      "main": [
        [
          {
            "node": "Merge With Forecast",
            "type": "main",
            "index": 0
          },
          {
            "node": "Fetch Amazon Search Results2",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Fetch Amazon Search Results2": {
      "main": [
        [
          {
            "node": "Extract Product Listings2",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Extract Product Listings2": {
      "main": [
        [
          {
            "node": "Process Product Data2",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Process Product Data2": {
      "main": [
        [
          {
            "node": "Sales Data Preparation",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Sales Data Preparation": {
      "main": [
        [
          {
            "node": "Merge With Forecast",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Merge With Forecast": {
      "main": [
        [
          {
            "node": "Enhance Forecast",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Enhance Forecast": {
      "main": [
        [
          {
            "node": "Preprocess Detail",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Preprocess Detail": {
      "main": [
        [
          {
            "node": "Prepare for Model",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Prepare for Model": {
      "main": [
        [
          {
            "node": "Train and Predict",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Train and Predict": {
      "main": [
        [
          {
            "node": "Forecast Sales",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Forecast Sales": {
      "main": [
        [
          {
            "node": "Format for Visualization",
            "type": "main",
            "index": 0
          },
          {
            "node": "Error Message (if forecast)",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Format for Visualization": {
      "main": [
        [
          {
            "node": "Write Forecast to Google Sheets",
            "type": "main",
            "index": 0
          },
          {
            "node": "Generate Forecast Email HTML",
            "type": "main",
            "index": 0
          },
          {
            "node": "Send to Dashboard",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Generate Forecast Email HTML": {
      "main": [
        [
          {
            "node": "Send Forecast Email",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Error Message (if forecast)": {
      "main": [
        [
          {
            "node": "Handle Error",
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
