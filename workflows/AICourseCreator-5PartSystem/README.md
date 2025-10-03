# Workflow: AI Course Creator - 5 Part System

## Overview

This document provides an overview of the 'AI Course Creator - 5 Part System' workflow.

## Workflow Steps (Nodes)

| Step Name | Type |
|-----------|------|
| Webhook - Course Topic Input | n8n-nodes-base.webhook |
| Set Course Variables | n8n-nodes-base.set |
| Agent 1 - Course Outline Generator | @n8n/n8n-nodes-langchain.lmChatOpenAi |
| Parse Course Outline | n8n-nodes-base.code |
| Agent 2 - Module Content Creator | @n8n/n8n-nodes-langchain.lmChatOpenAi |
| Agent 3 - Assessment Generator | @n8n/n8n-nodes-langchain.lmChatOpenAi |
| Agent 4 - Exercise Builder | @n8n/n8n-nodes-langchain.lmChatOpenAi |
| Agent 5 - Resource Compiler | @n8n/n8n-nodes-langchain.lmChatOpenAi |
| Aggregate Complete Course | n8n-nodes-base.code |
| Save Course to File | n8n-nodes-base.writeFile |
| Respond to Webhook | n8n-nodes-base.respondToWebhook |

## Raw JSON

```json
{
  "name": "AI Course Creator - 5 Part System",
  "nodes": [
    {
      "parameters": {
        "path": "course-creator",
        "options": {}
      },
      "id": "ab2f7880-c024-4dac-84e1-12b718735824",
      "name": "Webhook - Course Topic Input",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [
        48,
        64
      ],
      "webhookId": "course-creator"
    },
    {
      "parameters": {
        "options": {}
      },
      "id": "1586c630-fc05-43c8-9456-351044efe180",
      "name": "Set Course Variables",
      "type": "n8n-nodes-base.set",
      "typeVersion": 3,
      "position": [
        256,
        64
      ]
    },
    {
      "parameters": {
        "model": "gpt-4",
        "options": {}
      },
      "id": "dbf1a2bb-4cd7-4736-a7d1-3ead8bcda2fc",
      "name": "Agent 1 - Course Outline Generator",
      "type": "@n8n/n8n-nodes-langchain.lmChatOpenAi",
      "typeVersion": 1,
      "position": [
        448,
        64
      ]
    },
    {
      "parameters": {
        "jsCode": "const response = $input.first().json.response;\nlet parsed;\n\ntry {\n  // Try to extract JSON from markdown code blocks\n  const jsonMatch = response.match(/```json\\n([\\s\\S]*?)\\n```/) || response.match(/```\\n([\\s\\S]*?)\\n```/);\n  if (jsonMatch) {\n    parsed = JSON.parse(jsonMatch[1]);\n  } else {\n    parsed = JSON.parse(response);\n  }\n} catch (e) {\n  parsed = { rawResponse: response };\n}\n\nreturn { json: parsed };"
      },
      "id": "fd8f76a1-7b5d-4647-99b3-a77ae1bdef47",
      "name": "Parse Course Outline",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        656,
        64
      ]
    },
    {
      "parameters": {
        "model": "gpt-4",
        "options": {}
      },
      "id": "76f17e7d-fc88-449c-a207-246aabb66e7b",
      "name": "Agent 2 - Module Content Creator",
      "type": "@n8n/n8n-nodes-langchain.lmChatOpenAi",
      "typeVersion": 1,
      "position": [
        848,
        64
      ]
    },
    {
      "parameters": {
        "model": "gpt-4",
        "options": {}
      },
      "id": "43f4afdb-f59f-4134-8c50-336e18b84284",
      "name": "Agent 3 - Assessment Generator",
      "type": "@n8n/n8n-nodes-langchain.lmChatOpenAi",
      "typeVersion": 1,
      "position": [
        1056,
        64
      ]
    },
    {
      "parameters": {
        "model": "gpt-4",
        "options": {}
      },
      "id": "53aef197-b5eb-4c0c-8c43-b18ffbfcf79b",
      "name": "Agent 4 - Exercise Builder",
      "type": "@n8n/n8n-nodes-langchain.lmChatOpenAi",
      "typeVersion": 1,
      "position": [
        1248,
        64
      ]
    },
    {
      "parameters": {
        "model": "gpt-4",
        "options": {}
      },
      "id": "e835184b-a6e6-4d3a-908e-3e367ea39b69",
      "name": "Agent 5 - Resource Compiler",
      "type": "@n8n/n8n-nodes-langchain.lmChatOpenAi",
      "typeVersion": 1,
      "position": [
        1456,
        64
      ]
    },
    {
      "parameters": {
        "jsCode": "// Aggregate all course data\nconst outline = $('Parse Course Outline').first().json;\nconst moduleContent = $('Agent 2 - Module Content Creator').all();\nconst assessments = $('Agent 3 - Assessment Generator').all();\nconst exercises = $('Agent 4 - Exercise Builder').all();\nconst resources = $('Agent 5 - Resource Compiler').all();\n\nconst completeCourse = {\n  course_info: {\n    title: outline.title,\n    description: outline.description,\n    objectives: outline.objectives,\n    target_audience: $('Set Course Variables').first().json.targetAudience\n  },\n  modules: outline.modules.map((module, idx) => ({\n    number: module.number,\n    title: module.title,\n    description: module.description,\n    content: moduleContent[idx]?.json || {},\n    assessment: assessments[idx]?.json || {},\n    exercises: exercises[idx]?.json || {},\n    resources: resources[idx]?.json || {}\n  })),\n  generated_at: new Date().toISOString()\n};\n\nreturn { json: completeCourse };"
      },
      "id": "fb35a1b2-96ec-49ee-b8a1-9c5f0a005229",
      "name": "Aggregate Complete Course",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        1648,
        64
      ]
    },
    {
      "parameters": {},
      "id": "9164b05c-3099-4518-8a9a-7c781b0aa6f1",
      "name": "Save Course to File",
      "type": "n8n-nodes-base.writeFile",
      "typeVersion": 1,
      "position": [
        1856,
        64
      ]
    },
    {
      "parameters": {
        "respondWith": "json",
        "responseBody": "={{ $json }}",
        "options": {
          "responseHeaders": {
            "entries": [
              {
                "name": "Content-Type",
                "value": "application/json"
              }
            ]
          }
        }
      },
      "id": "84007f99-169f-494f-a68f-fa28fdff758e",
      "name": "Respond to Webhook",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1,
      "position": [
        2048,
        64
      ]
    }
  ],
  "connections": {
    "Webhook - Course Topic Input": {
      "main": [
        [
          {
            "node": "Set Course Variables",
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
