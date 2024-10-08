import re

class RuleViolation:
    def __init__(self, message, severity='ERROR'):
        self.message = message
        self.severity = severity.upper()

def has_mandatory_metadata(model):
    mandatory_fields = ['name', 'description', 'schema', 'columns', 'tags']
    missing_fields = [field for field in mandatory_fields if not model.get(field)]
    if missing_fields:
        return RuleViolation(
            message=f"Missing mandatory metadata fields: {', '.join(missing_fields)}.",
            severity='ERROR'
        )

def follows_snake_case(name):
    return re.match(r'^[a-z]+(_[a-z]+)*$', name) is not None

def naming_conventions(model):
    violations = []
    if not follows_snake_case(model['name']):
        violations.append("Model name does not follow snake_case convention.")
    
    columns = model.get('columns', {})
    for column in columns.keys():
        if not follows_snake_case(column):
            violations.append(f"Column '{column}' does not follow snake_case convention.")
    
    if violations:
        return RuleViolation(
            message=' '.join(violations),
            severity='WARNING'
        )

def columns_have_descriptions(model):
    columns = model.get('columns', {})
    missing_descriptions = [col for col, desc in columns.items() if not desc.strip()]
    if missing_descriptions:
        return RuleViolation(
            message=f"Columns missing descriptions: {', '.join(missing_descriptions)}.",
            severity='WARNING'
        )

def has_partitioning(model):
    if not model.get('partition_by'):
        return RuleViolation(
            message="Model is missing partitioning information.",
            severity='ERROR'
        )

def has_required_labels(model):
    required_labels = ['env', 'team']
    missing_labels = [label for label in required_labels if label not in model.get('labels', [])]
    if missing_labels:
        return RuleViolation(
            message=f"Missing required labels: {', '.join(missing_labels)}.",
            severity='ERROR'
        )

def avoid_select_star(model):
    if 'SELECT *' in model.get('sql', ''):
        return RuleViolation(
            message="Avoid using SELECT * in SQL queries.",
            severity='WARNING'
        )

def sql_line_limit(model, max_lines=200):
    sql = model.get('sql', '')
    if len(sql.splitlines()) > max_lines:
        return RuleViolation(
            message=f"SQL exceeds {max_lines} lines.",
            severity='ERROR'
        )

def comprehensive_description(model):
    if len(model.get('description', '').split()) < 10:
        return RuleViolation(
            message="Description is too short; provide a more comprehensive description.",
            severity='WARNING'
        )

def avoid_hardcoded_values(model):
    sql = model.get('sql', '')
    if re.search(r'\d+', sql):
        return RuleViolation(
            message="Avoid using hardcoded numeric values in SQL queries.",
            severity='WARNING'
        )

# List of rules to apply
RULES = [
    has_mandatory_metadata,
    naming_conventions,
    columns_have_descriptions,
    has_partitioning,
    has_required_labels,
    avoid_select_star,
    sql_line_limit,
    comprehensive_description,
    avoid_hardcoded_values
]