# Workflow: Viral Faceless YouTube Automation

## Overview

This document provides an overview of the 'Viral Faceless YouTube Automation' workflow.

## Workflow Steps (Nodes)

| Step Name | Type |
|-----------|------|
| Schedule Trigger | n8n-nodes-base.scheduleTrigger |
| OpenAI Generate Script | n8n-nodes-base.httpRequest |
| Parse Script Response | n8n-nodes-base.code |
| OpenAI TTS Voiceover | n8n-nodes-base.httpRequest |
| Pexels Get Stock Footage | n8n-nodes-base.httpRequest |
| Extract Video URL | n8n-nodes-base.code |
| DALLE Generate Thumbnail | n8n-nodes-base.httpRequest |
| Parse Thumbnail Response | n8n-nodes-base.code |
| Generate Metadata | n8n-nodes-base.code |
| Set Topic | n8n-nodes-base.set |
| Merge All Data | n8n-nodes-base.set |
| Final Output | n8n-nodes-base.code |

## Raw JSON

```json
{
  "name": "Viral Faceless YouTube Automation",
  "nodes": [
    {
      "parameters": {
        "rule": {
          "interval": [
            {}
          ]
        }
      },
      "id": "ac761154-1482-4f4a-84cc-43be010902d8",
      "name": "Schedule Trigger",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1.2,
      "position": [
        -864,
        208
      ]
    },
    {
      "parameters": {
        "method": "POST",
        "url": "https://api.openai.com/v1/chat/completions",
        "authentication": "predefinedCredentialType",
        "nodeCredentialType": "openAiApi",
        "sendBody": true,
        "specifyBody": "json",
        "jsonBody": "={\"model\": \"gpt-4\", \"messages\": [{\"role\": \"user\", \"content\": \"Create a viral YouTube video script about \" + $json.topic + \". Include: Hook (first 5 seconds), Main content (engaging facts), Call to action. Make it 60-90 seconds long, engaging and perfect for faceless video content.\"}]}",
        "options": {}
      },
      "id": "6d2831be-b96d-44cf-b036-a4596e02408f",
      "name": "OpenAI Generate Script",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [
        -448,
        208
      ],
      "credentials": {
        "openAiApi": {
          "id": "bkRA3W9ocQWZug4N",
          "name": "OpenAi account"
        }
      }
    },
    {
      "parameters": {
        "jsCode": "const response = $input.item.json.choices[0].message.content;\nreturn { json: { script: response, topic: $input.item.json.topic } };"
      },
      "id": "449236d9-1a89-4eeb-baea-b16ac642c91c",
      "name": "Parse Script Response",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        -224,
        208
      ]
    },
    {
      "parameters": {
        "method": "POST",
        "url": "https://api.openai.com/v1/audio/speech",
        "authentication": "predefinedCredentialType",
        "nodeCredentialType": "openAiApi",
        "sendBody": true,
        "specifyBody": "json",
        "jsonBody": "={\"model\": \"tts-1\", \"input\": $json.script, \"voice\": \"onyx\"}",
        "options": {
          "response": {
            "response": {
              "responseFormat": "file"
            }
          }
        }
      },
      "id": "55b505b5-c449-4fac-b768-6ecf9d904079",
      "name": "OpenAI TTS Voiceover",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [
        0,
        208
      ]
    },
    {
      "parameters": {
        "url": "https://api.pexels.com/videos/search",
        "authentication": "genericCredentialType",
        "genericAuthType": "httpHeaderAuth",
        "sendQuery": true,
        "queryParameters": {
          "parameters": [
            {
              "name": "query",
              "value": "={{$json.topic}}"
            },
            {
              "name": "per_page",
              "value": "5"
            },
            {
              "name": "orientation",
              "value": "portrait"
            }
          ]
        },
        "options": {}
      },
      "id": "f7910111-a860-487d-b7a9-18cb3be7d0ea",
      "name": "Pexels Get Stock Footage",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [
        0,
        400
      ]
    },
    {
      "parameters": {
        "jsCode": "if (!$input.item.json.videos || $input.item.json.videos.length === 0) {\n  throw new Error('No videos found');\n}\n\nconst videoUrl = $input.item.json.videos[0].video_files[0].link;\n\nreturn {\n  json: {\n    videoUrl: videoUrl,\n    topic: $input.item.json.topic\n  }\n};"
      },
      "id": "de4317c5-c5a3-4183-8c1e-245118c1ade6",
      "name": "Extract Video URL",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        224,
        400
      ]
    },
    {
      "parameters": {
        "method": "POST",
        "url": "https://api.openai.com/v1/images/generations",
        "authentication": "predefinedCredentialType",
        "nodeCredentialType": "openAiApi",
        "sendBody": true,
        "specifyBody": "json",
        "jsonBody": "={\"model\": \"dall-e-3\", \"prompt\": \"Create a YouTube thumbnail for a video about \" + $json.topic + \". Style: Bold text, eye-catching colors, high contrast, professional design, viral aesthetic\", \"size\": \"1024x1024\", \"quality\": \"standard\"}",
        "options": {}
      },
      "id": "9ec58d1d-0ebe-4dc3-be7e-536ad4446b73",
      "name": "DALLE Generate Thumbnail",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [
        0,
        0
      ]
    },
    {
      "parameters": {
        "jsCode": "const thumbnailUrl = $input.item.json.data[0].url;\nreturn { json: { thumbnailUrl: thumbnailUrl, topic: $input.item.json.topic } };"
      },
      "id": "521e9193-fd5b-49b6-ab54-bc66e06ccdf6",
      "name": "Parse Thumbnail Response",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        224,
        0
      ]
    },
    {
      "parameters": {
        "jsCode": "const script = $input.item.json.script || '';\nconst topic = $input.item.json.topic || 'Amazing Facts';\n\nconst title = topic + ' - You Won\\'t Believe This! \ud83e\udd2f';\n\nconst description = script.substring(0, 200) + '...\\n\\n\ud83d\udd14 Subscribe for more viral content!\\n\\n#' + topic.replace(/ /g, '') + ' #viral #trending #shorts';\n\nconst tags = topic + ',viral,trending,shorts,facts,amazing,youtube';\n\nreturn {\n  json: {\n    videoTitle: title,\n    description: description,\n    tags: tags,\n    script: script,\n    topic: topic\n  }\n};"
      },
      "id": "8837dac8-954a-44a7-a8cc-6cc27f47c03d",
      "name": "Generate Metadata",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        224,
        208
      ]
    },
    {
      "parameters": {
        "options": {}
      },
      "id": "7eceb7c7-497b-4730-88d1-95ac95061ad5",
      "name": "Set Topic",
      "type": "n8n-nodes-base.set",
      "typeVersion": 3.3,
      "position": [
        -656,
        208
      ]
    },
    {
      "parameters": {
        "assignments": {
          "assignments": [
            {
              "id": "merge-data",
              "name": "finalData",
              "value": "={\"videoTitle\": $('Generate Metadata').item.json.videoTitle, \"description\": $('Generate Metadata').item.json.description, \"tags\": $('Generate Metadata').item.json.tags, \"thumbnailUrl\": $('Parse Thumbnail Response').item.json.thumbnailUrl, \"audioFile\": $('OpenAI TTS Voiceover').item.json, \"videoUrl\": $('Extract Video URL').item.json.videoUrl}",
              "type": "object"
            }
          ]
        },
        "options": {}
      },
      "id": "794a80b4-a66d-4246-9927-0d178b0bdd3e",
      "name": "Merge All Data",
      "type": "n8n-nodes-base.set",
      "typeVersion": 3.3,
      "position": [
        448,
        208
      ]
    },
    {
      "parameters": {
        "jsCode": "return {\n  json: {\n    message: 'Workflow complete! Video ready for upload.',\n    title: $input.item.json.finalData.videoTitle,\n    description: $input.item.json.finalData.description,\n    thumbnailUrl: $input.item.json.finalData.thumbnailUrl,\n    videoUrl: $input.item.json.finalData.videoUrl,\n    status: 'ready'\n  }\n};"
      },
      "id": "59182e09-44c3-470b-b1b7-6b37db190a5c",
      "name": "Final Output",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        672,
        208
      ]
    }
  ],
  "connections": {
    "Schedule Trigger": {
      "main": [
        [
          {
            "node": "Set Topic",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Set Topic": {
      "main": [
        [
          {
            "node": "OpenAI Generate Script",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "OpenAI Generate Script": {
      "main": [
        [
          {
            "node": "Parse Script Response",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Parse Script Response": {
      "main": [
        [
          {
            "node": "OpenAI TTS Voiceover",
            "type": "main",
            "index": 0
          },
          {
            "node": "Pexels Get Stock Footage",
            "type": "main",
            "index": 0
          },
          {
            "node": "DALLE Generate Thumbnail",
            "type": "main",
            "index": 0
          },
          {
            "node": "Generate Metadata",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "OpenAI TTS Voiceover": {
      "main": [
        [
          {
            "node": "Merge All Data",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Pexels Get Stock Footage": {
      "main": [
        [
          {
            "node": "Extract Video URL",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Extract Video URL": {
      "main": [
        [
          {
            "node": "Merge All Data",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "DALLE Generate Thumbnail": {
      "main": [
        [
          {
            "node": "Parse Thumbnail Response",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Parse Thumbnail Response": {
      "main": [
        [
          {
            "node": "Merge All Data",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Generate Metadata": {
      "main": [
        [
          {
            "node": "Merge All Data",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Merge All Data": {
      "main": [
        [
          {
            "node": "Final Output",
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
