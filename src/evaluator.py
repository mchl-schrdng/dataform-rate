from rules import (
    RULES,
    has_mandatory_metadata,
    naming_conventions,
    columns_have_descriptions,
    has_partitioning,
    has_any_labels,
    avoid_select_star,
    sql_line_limit,
    comprehensive_column_descriptions,
    avoid_hardcoded_values
)

def evaluate_models(models, **kwargs):
    violations = []

    for model in models:
        for rule in RULES:
            if rule.__code__.co_argcount > 1:
                violation = rule(model, **kwargs)
            else:
                violation = rule(model)
            if violation:
                violations.append({
                    'model': model['name'],
                    'file_path': model['file_path'],
                    'rule': rule.__name__,
                    'message': violation.message,
                    'severity': violation.severity,
                })
    return violations