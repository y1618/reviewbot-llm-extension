import json
import logging
import requests
from reviewbot.tools.base import BaseTool


class LLMTool(BaseTool):
    name = 'LLM Code Review'
    version = '1.0'
    description = 'Performs code reviews using local LLMs via OpenWebUI or llamacpp'
    
    options = [
        {
            'name': 'backend',
            'field_type': 'django.forms.ChoiceField',
            'default': 'openwebui',
            'field_options': {
                'choices': [
                    ('openwebui', 'OpenWebUI HTTP API'),
                    ('llamacpp', 'llamacpp Remote Server'),
                ],
                'help_text': 'Choose the LLM backend to use for code reviews',
            },
        },
        {
            'name': 'openwebui_url',
            'field_type': 'django.forms.CharField',
            'default': 'http://localhost:3000',
            'field_options': {
                'help_text': 'OpenWebUI server URL (used when backend is openwebui)',
            },
        },
        {
            'name': 'openwebui_api_key',
            'field_type': 'django.forms.CharField',
            'default': '',
            'field_options': {
                'help_text': 'OpenWebUI API key (optional)',
                'required': False,
            },
        },
        {
            'name': 'model_name',
            'field_type': 'django.forms.CharField',
            'default': 'llama2',
            'field_options': {
                'help_text': 'Model name for OpenWebUI or llamacpp server',
            },
        },
        {
            'name': 'llamacpp_url',
            'field_type': 'django.forms.CharField',
            'default': 'http://localhost:8080',
            'field_options': {
                'help_text': 'llamacpp server URL (used when backend is llamacpp)',
            },
        },
        {
            'name': 'llamacpp_api_key',
            'field_type': 'django.forms.CharField',
            'default': '',
            'field_options': {
                'help_text': 'llamacpp server API key (optional)',
                'required': False,
            },
        },
        {
            'name': 'max_tokens',
            'field_type': 'django.forms.IntegerField',
            'default': 1000,
            'field_options': {
                'help_text': 'Maximum tokens for LLM response',
            },
        },
        {
            'name': 'custom_instructions',
            'field_type': 'django.forms.CharField',
            'default': '',
            'field_options': {
                'widget': 'django.forms.Textarea',
                'help_text': 'Custom coding rules and instructions for the LLM review (optional)',
                'required': False,
            },
        },
        {
            'name': 'temperature',
            'field_type': 'django.forms.FloatField',
            'default': 0.1,
            'field_options': {
                'help_text': 'Temperature for LLM response (0.0-1.0, lower = more focused)',
            },
        },
    ]
    
    file_patterns = ['*.py', '*.js', '*.ts', '*.java', '*.cpp', '*.c', '*.h', '*.go', '*.rs', '*.rb', '*.php']

    def handle_file(self, f, path, base_commit_id=None):
        """Process a file and generate LLM-based code review comments."""
        backend = self.settings.get('backend', 'openwebui')
        
        try:
            content = f.read().decode('utf-8')
        except UnicodeDecodeError:
            logging.warning(f"Could not decode file {path}, skipping LLM review")
            return
            
        if len(content.strip()) == 0:
            return
            
        prompt = self._generate_review_prompt(content, path)
        
        try:
            if backend == 'openwebui':
                response = self._call_openwebui(prompt)
            elif backend == 'llamacpp':
                response = self._call_llamacpp(prompt)
            else:
                logging.error(f"Unknown backend: {backend}")
                return
                
            self._process_llm_response(response, f, path)
            
        except Exception as e:
            logging.error(f"LLM review failed for {path}: {str(e)}")
    
    def _generate_review_prompt(self, content, path):
        """Generate a comprehensive code review prompt."""
        file_extension = path.split('.')[-1] if '.' in path else 'unknown'
        custom_instructions = self.settings.get('custom_instructions', '').strip()
        
        base_prompt = f"""Please review the following {file_extension} code file and provide constructive feedback.
Focus on:
- Code quality and best practices
- Potential bugs or security issues
- Performance considerations
- Readability and maintainability
- Adherence to coding standards"""

        if custom_instructions:
            base_prompt += f"""

Additional project-specific requirements:
{custom_instructions}"""

        return f"""{base_prompt}

File: {path}

Code:
```{file_extension}
{content}
```

Please provide your review in JSON format with the following structure:
{{
    "comments": [
        {{
            "line": <line_number>,
            "message": "<review_comment>",
            "severity": "info"
        }}
    ],
    "summary": "<overall_summary>"
}}

Important: Only include specific, actionable feedback. If the code looks good, you can return an empty comments array."""

    def _call_openwebui(self, prompt):
        """Call OpenWebUI API for code review."""
        url = self.settings.get('openwebui_url', 'http://localhost:3000')
        api_key = self.settings.get('openwebui_api_key', '')
        model_name = self.settings.get('model_name', 'llama2')
        max_tokens = self.settings.get('max_tokens', 1000)
        temperature = self.settings.get('temperature', 0.1)
        
        headers = {'Content-Type': 'application/json'}
        if api_key:
            headers['Authorization'] = f'Bearer {api_key}'
            
        payload = {
            'model': model_name,
            'messages': [
                {'role': 'user', 'content': prompt}
            ],
            'max_tokens': max_tokens,
            'temperature': temperature,
        }
        
        try:
            response = requests.post(
                f"{url}/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            
            data = response.json()
            return data['choices'][0]['message']['content']
            
        except requests.exceptions.RequestException as e:
            payload = {
                'model': model_name,
                'messages': [
                    {'role': 'user', 'content': prompt}
                ],
                'stream': False,
            }
            
            response = requests.post(
                f"{url}/api/chat",
                headers=headers,
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            
            data = response.json()
            return data['message']['content']

    def _call_llamacpp(self, prompt):
        """Call remote llamacpp server for code review."""
        url = self.settings.get('llamacpp_url', 'http://localhost:8080')
        api_key = self.settings.get('llamacpp_api_key', '')
        model_name = self.settings.get('model_name', 'llama2')
        max_tokens = self.settings.get('max_tokens', 1000)
        temperature = self.settings.get('temperature', 0.1)
        
        headers = {'Content-Type': 'application/json'}
        if api_key:
            headers['Authorization'] = f'Bearer {api_key}'
            
        payload = {
            'model': model_name,
            'messages': [
                {'role': 'user', 'content': prompt}
            ],
            'max_tokens': max_tokens,
            'temperature': temperature,
        }
        
        try:
            response = requests.post(
                f"{url}/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            
            data = response.json()
            return data['choices'][0]['message']['content']
            
        except requests.exceptions.RequestException:
            payload = {
                'prompt': prompt,
                'n_predict': max_tokens,
                'temperature': temperature,
                'stop': ['</s>', '\n\n'],
            }
            
            response = requests.post(
                f"{url}/completion",
                headers=headers,
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            
            data = response.json()
            return data.get('content', '')
    
    def _process_llm_response(self, response, f, path):
        """Parse LLM response and add review comments."""
        try:
            data = json.loads(response)
            comments = data.get('comments', [])
            
            for comment in comments:
                line_num = comment.get('line', 1)
                message = comment.get('message', '')
                
                if message and line_num > 0:
                    f.comment(message, line_num)
                    
            summary = data.get('summary', '')
            if summary and not comments:
                f.comment(f"LLM Code Review Summary:\n{summary}", 1)
                    
        except json.JSONDecodeError:
            if response.strip():
                f.comment(f"LLM Code Review:\n{response}", 1)
