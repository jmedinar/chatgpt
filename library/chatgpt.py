#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import requests

def run_module():
    module_args = dict(
        query=dict(type='str', required=True),
        api_key=dict(type='str', required=True, no_log=True),
        model=dict(type='str', required=False, default='gpt-3.5-turbo'),
        max_tokens=dict(type='int', required=False, default=150)
    )

    result = dict(
        changed=False,
        response=dict()
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    query = module.params['query']
    api_key = module.params['api_key']
    model = module.params['model']
    max_tokens = module.params['max_tokens']

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    data = {
        'model': model,
        'messages': [{'role': 'user', 'content': query}],
        'max_tokens': max_tokens
    }

    try:
        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
        response.raise_for_status()
        response_data = response.json()
        result['response'] = response_data['choices'][0]['message']['content']
        result['changed'] = True
    except requests.exceptions.RequestException as e:
        module.fail_json(msg=f"API request failed: {e}")

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()

