# Workflow: VR Realtor - Schedule VR Tour Automation

## Overview

This document provides an overview of the 'VR Realtor - Schedule VR Tour Automation' workflow.

## Workflow Steps (Nodes)

| Step Name | Type |
|-----------|------|
| Webhook - Form Submission | n8n-nodes-base.webhook |
| Validate Data | n8n-nodes-base.function |
| Check CRM - Existing Lead? | n8n-nodes-base.airtable |
| IF - New Lead? | n8n-nodes-base.if |
| Google Calendar - Check Availability | n8n-nodes-base.googleCalendar |
| Generate VR Session | n8n-nodes-base.function |
| Create Calendar Event | n8n-nodes-base.googleCalendar |
| Send Confirmation Email | n8n-nodes-base.gmail |
| Send SMS Confirmation | n8n-nodes-base.twilio |
| Create CRM Record (New Lead) | n8n-nodes-base.airtable |
| Update CRM Record (Returning Lead) | n8n-nodes-base.airtable |
| Notify Team on Slack | n8n-nodes-base.slack |
| Schedule 1-Hour Reminder | n8n-nodes-base.schedule |
| Send Reminder SMS | n8n-nodes-base.twilio |
| Webhook Response | n8n-nodes-base.respondToWebhook |

## Raw JSON

```json
{
  "name": "VR Realtor - Schedule VR Tour Automation",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "vr-tour-booking",
        "responseMode": "responseNode",
        "options": {}
      },
      "id": "c7e16f89-703d-4ffa-a94b-d2142d52a09c",
      "name": "Webhook - Form Submission",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [
        -1776,
        48
      ],
      "webhookId": "vr-tour-webhook"
    },
    {
      "parameters": {
        "functionCode": "// Validate email and phone formats\nconst email = $input.item.json.body.email;\nconst phone = $input.item.json.body.phone;\nconst name = $input.item.json.body.name;\nconst propertyId = $input.item.json.body.propertyId;\nconst preferredDate = $input.item.json.body.preferredDate;\n\n// Email validation\nconst emailRegex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;\nconst isValidEmail = emailRegex.test(email);\n\n// Phone validation (accepts various formats)\nconst phoneRegex = /^[\\d\\s\\-\\+\\(\\)]{10,}$/;\nconst isValidPhone = phoneRegex.test(phone);\n\nif (!isValidEmail) {\n  throw new Error(`Invalid email format: ${email}`);\n}\n\nif (!isValidPhone) {\n  throw new Error(`Invalid phone format: ${phone}`);\n}\n\nif (!name || !propertyId) {\n  throw new Error('Missing required fields: name or propertyId');\n}\n\n// Return cleaned data\nreturn {\n  email: email.toLowerCase().trim(),\n  phone: phone.replace(/\\D/g, ''), // Remove non-digits\n  name: name.trim(),\n  propertyId,\n  preferredDate: preferredDate || new Date().toISOString(),\n  timestamp: new Date().toISOString()\n};"
      },
      "id": "632c41b5-2976-45d6-8cc5-11e79d295d6d",
      "name": "Validate Data",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "position": [
        -1584,
        48
      ]
    },
    {
      "parameters": {
        "operation": "search",
        "application": "appXXXXXXXXXXXXXX",
        "table": "tblLeads"
      },
      "id": "61c880d2-b663-4bf9-8e2e-e99aa856a636",
      "name": "Check CRM - Existing Lead?",
      "type": "n8n-nodes-base.airtable",
      "typeVersion": 1,
      "position": [
        -1376,
        48
      ]
    },
    {
      "parameters": {
        "conditions": {
          "number": [
            {
              "value1": "={{$json[\"records\"].length}}",
              "operation": "equal"
            }
          ]
        }
      },
      "id": "d9e19a3a-41cf-4782-92f8-551a73f2fde4",
      "name": "IF - New Lead?",
      "type": "n8n-nodes-base.if",
      "typeVersion": 1,
      "position": [
        -1184,
        48
      ]
    },
    {
      "parameters": {
        "calendar": "primary",
        "start": "={{$node['Validate Data'].json['preferredDate']}}",
        "end": "={{new Date(new Date($node['Validate Data'].json['preferredDate']).getTime() + 60*60*1000).toISOString()}}",
        "additionalFields": {}
      },
      "id": "8d12bf66-2e37-44c4-a0b8-132d5c7b907f",
      "name": "Google Calendar - Check Availability",
      "type": "n8n-nodes-base.googleCalendar",
      "typeVersion": 1,
      "position": [
        -976,
        -48
      ]
    },
    {
      "parameters": {
        "functionCode": "// Generate unique VR session ID and link\nconst crypto = require('crypto');\nconst sessionId = crypto.randomBytes(16).toString('hex');\nconst propertyId = $node['Validate Data'].json.propertyId;\nconst name = $node['Validate Data'].json.name;\nconst email = $node['Validate Data'].json.email;\n\n// Create VR link\nconst vrLink = `https://yourvr.com/tour/${propertyId}?session=${sessionId}`;\nconst accessCode = Math.floor(100000 + Math.random() * 900000).toString();\n\n// Calculate expiration (24 hours from now)\nconst expiresAt = new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString();\n\n// Determine time slot based on calendar availability\nconst calendarEvents = $node['Google Calendar - Check Availability'].json;\nlet proposedTime = new Date($node['Validate Data'].json.preferredDate);\n\n// If time slot is taken, suggest next available\nif (calendarEvents && calendarEvents.length > 0) {\n  proposedTime = new Date(proposedTime.getTime() + 2 * 60 * 60 * 1000); // Add 2 hours\n}\n\nreturn {\n  sessionId,\n  vrLink,\n  accessCode,\n  expiresAt,\n  propertyId,\n  name,\n  email,\n  phone: $node['Validate Data'].json.phone,\n  scheduledTime: proposedTime.toISOString(),\n  meetingTitle: `VR Property Tour - ${propertyId} - ${name}`\n};"
      },
      "id": "09dd3352-1632-477a-95aa-35183d1a39e3",
      "name": "Generate VR Session",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "position": [
        -784,
        -48
      ]
    },
    {
      "parameters": {
        "calendar": "primary",
        "start": "={{$json['scheduledTime']}}",
        "end": "={{new Date(new Date($json['scheduledTime']).getTime() + 60*60*1000).toISOString()}}",
        "additionalFields": {}
      },
      "id": "ec541d27-9cf8-4062-a46d-f24d3916d735",
      "name": "Create Calendar Event",
      "type": "n8n-nodes-base.googleCalendar",
      "typeVersion": 1,
      "position": [
        -576,
        -48
      ]
    },
    {
      "parameters": {
        "subject": "Your VR Property Tour is Confirmed! \ud83c\udfe1",
        "message": "<!DOCTYPE html>\n<html>\n<head>\n  <style>\n    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }\n    .container { max-width: 600px; margin: 0 auto; padding: 20px; }\n    .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }\n    .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }\n    .button { display: inline-block; background: #667eea; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }\n    .info-box { background: white; padding: 20px; border-left: 4px solid #667eea; margin: 20px 0; }\n    .footer { text-align: center; margin-top: 30px; color: #666; font-size: 12px; }\n  </style>\n</head>\n<body>\n  <div class=\"container\">\n    <div class=\"header\">\n      <h1>\ud83c\udf89 Your VR Tour is Confirmed!</h1>\n    </div>\n    <div class=\"content\">\n      <p>Hi {{$node['Generate VR Session'].json['name']}},</p>\n      <p>Great news! Your virtual reality property tour has been scheduled.</p>\n      \n      <div class=\"info-box\">\n        <strong>\ud83d\udcc5 Scheduled Time:</strong><br>\n        {{new Date($node['Generate VR Session'].json['scheduledTime']).toLocaleString()}}<br><br>\n        <strong>\ud83c\udfe0 Property ID:</strong> {{$node['Generate VR Session'].json['propertyId']}}<br>\n        <strong>\ud83d\udd10 Access Code:</strong> <span style=\"font-size: 24px; font-weight: bold; color: #667eea;\">{{$node['Generate VR Session'].json['accessCode']}}</span>\n      </div>\n      \n      <center>\n        <a href=\"{{$node['Generate VR Session'].json['vrLink']}}\" class=\"button\">\ud83d\ude80 Start Your VR Tour</a>\n      </center>\n      \n      <p><strong>Important Notes:</strong></p>\n      <ul>\n        <li>Your VR session link is active for 24 hours</li>\n        <li>You'll receive an SMS reminder 1 hour before your tour</li>\n        <li>Make sure you have a VR headset or use desktop mode</li>\n        <li>Contact us if you need to reschedule</li>\n      </ul>\n      \n      <div class=\"footer\">\n        <p>Questions? Reply to this email or call us at (555) 123-4567</p>\n        <p>&copy; 2025 VR Realty. All rights reserved.</p>\n      </div>\n    </div>\n  </div>\n</body>\n</html>",
        "additionalFields": {}
      },
      "id": "ee6af3e7-c3bb-431a-86ee-986ef98089e0",
      "name": "Send Confirmation Email",
      "type": "n8n-nodes-base.gmail",
      "typeVersion": 1,
      "position": [
        -384,
        -160
      ]
    },
    {
      "parameters": {
        "message": "Hi {{$node['Generate VR Session'].json['name']}}! Your VR property tour is confirmed for {{new Date($node['Generate VR Session'].json['scheduledTime']).toLocaleString()}}. Access code: {{$node['Generate VR Session'].json['accessCode']}}. Link in your email. See you soon! \ud83c\udfe1",
        "options": {}
      },
      "id": "c3944cf0-843f-4d68-b3f3-09ad00a35714",
      "name": "Send SMS Confirmation",
      "type": "n8n-nodes-base.twilio",
      "typeVersion": 1,
      "position": [
        -384,
        -48
      ]
    },
    {
      "parameters": {
        "operation": "create",
        "application": "appXXXXXXXXXXXXXX",
        "table": "tblLeads"
      },
      "id": "971a1693-47a0-4aa7-8390-c0b894899d2e",
      "name": "Create CRM Record (New Lead)",
      "type": "n8n-nodes-base.airtable",
      "typeVersion": 1,
      "position": [
        -384,
        48
      ]
    },
    {
      "parameters": {
        "operation": "update",
        "application": "appXXXXXXXXXXXXXX",
        "table": "tblLeads",
        "id": "={{$node['Check CRM - Existing Lead?'].json['records'][0]['id']}}",
        "options": {}
      },
      "id": "dcc12e28-5c22-4dba-92b5-e6878bfc8bf1",
      "name": "Update CRM Record (Returning Lead)",
      "type": "n8n-nodes-base.airtable",
      "typeVersion": 1,
      "position": [
        -384,
        160
      ]
    },
    {
      "parameters": {
        "channel": "#realtor-alerts",
        "text": "\ud83c\udfaf New VR Tour Scheduled!\n\n*Client:* {{$node['Generate VR Session'].json['name']}}\n*Email:* {{$node['Generate VR Session'].json['email']}}\n*Phone:* {{$node['Generate VR Session'].json['phone']}}\n*Property:* {{$node['Generate VR Session'].json['propertyId']}}\n*Time:* {{new Date($node['Generate VR Session'].json['scheduledTime']).toLocaleString()}}\n*Lead Type:* {{$node['IF - New Lead?'].json ? 'New Lead' : 'Returning Client'}}\n\n<{{$node['Generate VR Session'].json['vrLink']}}|View VR Session>",
        "otherOptions": {},
        "attachments": []
      },
      "id": "612b68a4-8f8a-43e7-aa7f-64b1b10081c2",
      "name": "Notify Team on Slack",
      "type": "n8n-nodes-base.slack",
      "typeVersion": 1,
      "position": [
        -176,
        -48
      ]
    },
    {
      "parameters": {},
      "id": "b343babe-832c-40d6-b07c-1d8df8ac12e2",
      "name": "Schedule 1-Hour Reminder",
      "type": "n8n-nodes-base.schedule",
      "typeVersion": 1,
      "position": [
        32,
        -160
      ]
    },
    {
      "parameters": {
        "message": "\u23f0 Reminder: Your VR property tour starts in 1 hour! Access code: {{$node['Generate VR Session'].json['accessCode']}}. Link: {{$node['Generate VR Session'].json['vrLink']}} See you soon!",
        "options": {}
      },
      "id": "dfa6095e-1317-40c9-b9d9-424a8a30304e",
      "name": "Send Reminder SMS",
      "type": "n8n-nodes-base.twilio",
      "typeVersion": 1,
      "position": [
        224,
        -160
      ]
    },
    {
      "parameters": {
        "respondWith": "json",
        "responseBody": "={\n  \"success\": true,\n  \"message\": \"Your VR tour has been scheduled successfully!\",\n  \"data\": {\n    \"scheduledTime\": \"{{$node['Generate VR Session'].json['scheduledTime']}}\",\n    \"confirmationSent\": true,\n    \"sessionId\": \"{{$node['Generate VR Session'].json['sessionId']}}\"\n  }\n}",
        "options": {}
      },
      "id": "deec15e5-842a-4235-9c83-c86667187469",
      "name": "Webhook Response",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1,
      "position": [
        32,
        48
      ]
    }
  ],
  "connections": {
    "Webhook - Form Submission": {
      "main": [
        [
          {
            "node": "Validate Data",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Validate Data": {
      "main": [
        [
          {
            "node": "Check CRM - Existing Lead?",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Check CRM - Existing Lead?": {
      "main": [
        [
          {
            "node": "IF - New Lead?",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "IF - New Lead?": {
      "main": [
        [
          {
            "node": "Google Calendar - Check Availability",
            "type": "main",
            "index": 0
          }
        ],
        [
          {
            "node": "Google Calendar - Check Availability",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Google Calendar - Check Availability": {
      "main": [
        [
          {
            "node": "Generate VR Session",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Generate VR Session": {
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
            "node": "Send Confirmation Email",
            "type": "main",
            "index": 0
          },
          {
            "node": "Send SMS Confirmation",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Send Confirmation Email": {
      "main": [
        [
          {
            "node": "Create CRM Record (New Lead)",
            "type": "main",
            "index": 0
          },
          {
            "node": "Update CRM Record (Returning Lead)",
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
            "node": "Notify Team on Slack",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Create CRM Record (New Lead)": {
      "main": [
        [
          {
            "node": "Notify Team on Slack",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Update CRM Record (Returning Lead)": {
      "main": [
        [
          {
            "node": "Notify Team on Slack",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Notify Team on Slack": {
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
  "meta": {
    "templateCredsSetupCompleted": true
  }
}
```
