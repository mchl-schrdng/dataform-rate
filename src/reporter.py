def report_violations(violations, output_format='console'):
    if not violations:
        print('All models passed the best practice checks!')
        return

    # Organize violations by file
    violations_by_file = {}
    total_errors = 0
    total_warnings = 0

    for v in violations:
        file_path = v['file_path']
        severity = v['severity']

        if file_path not in violations_by_file:
            violations_by_file[file_path] = {'errors': [], 'warnings': []}

        if severity == 'ERROR':
            violations_by_file[file_path]['errors'].append(v)
            total_errors += 1
        elif severity == 'WARNING':
            violations_by_file[file_path]['warnings'].append(v)
            total_warnings += 1

    total_files = len(violations_by_file)
    files_without_issues = total_files - len([f for f in violations_by_file if violations_by_file[f]['errors'] or violations_by_file[f]['warnings']])

    # Summary
    summary = f"Summary:\nTotal Errors: {total_errors}\nTotal Warnings: {total_warnings}\nTotal Files Checked: {total_files}\nFiles Without Issues: {files_without_issues}"
    
    if output_format == 'console':
        print(summary)
        print('\nDetailed Report by File:')

        for file_path, issues in violations_by_file.items():
            print(f"\nFile: {file_path}")
            
            if issues['errors']:
                print("  Errors:")
                for error in issues['errors']:
                    print(f"    - [{error['severity']}] {error['message']}")
            
            if issues['warnings']:
                print("  Warnings:")
                for warning in issues['warnings']:
                    print(f"    - [{warning['severity']}] {warning['message']}")
            if not issues['errors'] and not issues['warnings']:
                print("  No issues found.")
                
    elif output_format == 'json':
        import json
        print(json.dumps({
            'summary': {
                'total_errors': total_errors,
                'total_warnings': total_warnings,
                'total_files': total_files,
                'files_without_issues': files_without_issues
            },
            'violations_by_file': violations_by_file
        }, indent=2))

    else:
        print(f"Unsupported output format: {output_format}")