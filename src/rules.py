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
            message=f"Columns lack descriptions: {', '.join(missing_descriptions)}.",
            severity='ERROR'
        )

def has_partitioning(model):
    bigquery = model.get('bigquery', {})
    partition_by = bigquery.get('partitionBy')
    if not partition_by:
        return RuleViolation(
            message="BigQuery configuration missing 'partitionBy' field.",
            severity='WARNING'
        )
    if partition_by not in model.get('columns', {}):
        return RuleViolation(
            message=f"Partition column '{partition_by}' is not defined in columns.",
            severity='ERROR'
        )

def has_required_labels(model):
    bigquery = model.get('bigquery', {})
    labels = bigquery.get('labels', {})
    required_labels = ['cost_center'] 
    missing_labels = [label for label in required_labels if not labels.get(label)]
    if missing_labels:
        return RuleViolation(
            message=f"BigQuery labels missing: {', '.join(missing_labels)}.",
            severity='WARNING'  
        )

def avoid_select_star(model):
    sql_code = model.get('sql_code', '').lower()
    if 'select *' in sql_code:
        return RuleViolation(
            message="SQL query uses SELECT *, which is discouraged.",
            severity='WARNING' 
        )

def sql_line_limit(model, max_lines=200):
    sql_code = model.get('sql_code', '')
    line_count = sql_code.count('\n') + 1
    if line_count > max_lines:
        return RuleViolation(
            message=f"SQL code exceeds {max_lines} lines.",
            severity='WARNING' 
        )

def comprehensive_description(model):
    description = model.get('description', '')
    if len(description) < 50: 
        return RuleViolation(
            message="Model description is too short; consider providing more details.",
            severity='WARNING'  
        )
    
RULES = [
    has_mandatory_metadata,
    naming_conventions,
    columns_have_descriptions,
    has_partitioning,
    has_required_labels,
    avoid_select_star,
    sql_line_limit,
    comprehensive_description
]