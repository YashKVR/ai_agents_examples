# Prompt Styles

## Alpaca Style Prompt
```
### Instructions: <SYSTEM_PROMPT>\n
### Input: <USER_QUERY>
### Response: \n
```

## ChatML Style Prompt
The style we have been using in OpenAi code is chatml style
```
{
    "role": "system" | "user" | "assistant"
    "content": "string"
}
```

## INST Style Prompt
Also called Instruction Style Prompting. Used by Llama 2 models
```
[INST] What is the time now? [/INST]
```
