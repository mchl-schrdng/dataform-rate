def report_violations(violations, output_format='console'):
    if not violations:
        print('All models passed the best practice checks!')
        return

    if output_format == 'console':
        print('Best Practice Violations:')
        for v in violations:
            print(f"[{v['severity']}] {v['model']} ({v['file_path']}): {v['message']}")
    elif output_format == 'json':
        import json
        print(json.dumps(violations, indent=2))
    else:
        print(f"Unsupported output format: {output_format}")