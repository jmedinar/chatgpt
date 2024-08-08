#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import requests

def run_module():
    # Define module arguments
    module_args = dict(
        api_key=dict(type='str', required=True, no_log=True),
        prompt=dict(type='str', required=True),
        engine=dict(type='str', default='gpt-4'),
        max_tokens=dict(type='int', default=150),
        temperature=dict(type='float', default=0.7),
        top_p=dict(type='float', default=1.0),
        frequency_penalty=dict(type='float', default=0.0),
        presence_penalty=dict(type='float', default=0.0)
    )

    # Instantiate the Ansible module object
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # Extract the parameters
    api_key = module.params['api_key']
    prompt = module.params['prompt']
    engine = module.params['engine']
    max_tokens = module.params['max_tokens']
    temperature = module.params['temperature']
    top_p = module.params['top_p']
    frequency_penalty = module.params['frequency_penalty']
    presence_penalty = module.params['presence_penalty']

    # Prepare the API request
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    data = {
        "model": engine,
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p,
        "frequency_penalty": frequency_penalty,
        "presence_penalty": presence_penalty
    }

    url = "https://api.openai.com/v1/completions"

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        module.exit_json(changed=False, response=result)
    except requests.exceptions.RequestException as e:
        module.fail_json(msg=f"API request failed: {str(e)}")

def main():
    run_module()

if __name__ == '__main__':
    main()

