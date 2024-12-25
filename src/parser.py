import glob
import re
import json
import logging

def get_all_models(model_path='../definitions/**/*.sqlx'):
    model_files = glob.glob(model_path, recursive=True)
    logging.debug(f"Found model files: {model_files}")
    models = []

    for file_path in model_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            model = parse_model(content, file_path)
            if model:
                models.append(model)
            else:
                logging.warning(f"Failed to parse model in file: {file_path}")
    return models

def parse_model(content, file_path):
    config_start_match = re.search(r'config\s*\{', content)
    if not config_start_match:
        logging.warning(f"No config block found in {file_path}")
        return None

    start_index = config_start_match.end()
    index = start_index
    brace_count = 1

    while brace_count > 0 and index < len(content):
        if content[index] == '{':
            brace_count += 1
        elif content[index] == '}':
            brace_count -= 1
        index += 1

    if brace_count != 0:
        logging.error(f"Unbalanced braces in config block in {file_path}")
        return None

    config_content = content[start_index:index - 1]

    sql_code = content[index:].strip()

    json_str = convert_config_to_json(config_content)

    logging.debug(f"JSON string to be parsed from {file_path}:\n{json_str}")

    try:
        config = json.loads(json_str)
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing config in {file_path}: {e}")
        logging.debug(f"Config content that caused error:\n{json_str}")
        return None

    model = {
        'file_path': file_path,
        'type': config.get('type', ''),   # <--- Add this
        'name': config.get('name', ''),
        'description': config.get('description', ''),
        'columns': config.get('columns', {}),
        'schema': config.get('schema', ''),
        'meta': config.get('meta', {}),
        'tags': config.get('tags', []),
        'bigquery': config.get('bigquery', {}),
        'sql_code': sql_code,
    }

    bigquery = config.get('bigquery', {})
    model['partition_by'] = bigquery.get('partitionBy', '')
    model['labels'] = bigquery.get('labels', {})

    return model

def convert_config_to_json(config_content):
    config_content = re.sub(r'//.*', '', config_content)
    config_content = re.sub(r'/\*[\s\S]*?\*/', '', config_content)
    config_content = re.sub(r'#.*', '', config_content)
    config_content = re.sub(r'(\b[\w\-]+\b)\s*:', r'"\1":', config_content)
    config_content = re.sub(r',\s*(\}|\])', r'\1', config_content)
    config_content = re.sub(r'\s+', ' ', config_content).strip()

    json_str = '{' + config_content + '}'

    return json_str