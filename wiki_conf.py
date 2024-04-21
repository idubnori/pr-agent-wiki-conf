import os
import toml
import json

ei_key = 'extra_instructions'
ei_sections = ['pr_reviewer', 'pr_description', 'pr_code_suggestions', 'pr_add_docs', 'pr_update_changelog', 'pr_test', 'pr_improve_component']

repository_name = os.getenv('GITHUB_REPOSITORY')

def get_conf():
  try:
      # Load Config file
      with open("wiki_temp/${{ inputs.page-name }}", encoding="UTF-8") as f:
        toml_content = f.read()

        # Parse TOML content
        start = toml_content.find("```") + 3
        end = toml_content.rfind("```")
        toml_content = toml_content[start:end]

        parsed_toml = toml.loads(toml_content)
        return parsed_toml

  except Exception as e:
      print(f"Error: {e}")
      return {}

def concat_env_value(parsed_toml):
  common_instructions = os.getenv('common_instructions')
  for key in ei_sections:
    additional_instructions = os.getenv(f"{key}.{ei_key}", None).strip() + '\n' + common_instructions
    if key in parsed_toml:
      if ei_key in parsed_toml[key]:
        parsed_toml[key][ei_key] = (parsed_toml[key][ei_key]).strip() + '\n' + additional_instructions
      else:
        parsed_toml[key][ei_key] = additional_instructions
    else:
      parsed_toml[key] = {ei_key: additional_instructions}

  return parsed_toml

def set_to_env(parsed_toml):
  github_env = os.getenv('GITHUB_ENV')
  with open(github_env, "a") as outputfile:
    for key in ei_sections:
      print(f"{key}.{ei_key}<<EOF",file=outputfile)
      print(f"{parsed_toml[key][ei_key]}",file=outputfile)
      print(f"EOF",file=outputfile)

if __name__ == "__main__":
  toml_conf = get_conf()
  added_toml_conf = concat_env_value(toml_conf)
  set_to_env(added_toml_conf)