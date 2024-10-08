from loguru import logger

# Configure logger for custom formatting (no color)
logger.remove()
logger.add(lambda msg: print(msg, end=""), format="{message}", colorize=False)

def report_violations(violations, output_format='console'):
    if not violations:
        logger.info("✅ All models passed the best practice checks!")
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

    # Strong delimiters
    delimiter = "=" * 60
    file_separator = "-" * 60

    if output_format == 'console':
        # Console output
        logger.info(delimiter)
        logger.info("Summary")
        logger.info(delimiter)

        # Summary section
        logger.info(f"❌ Total Errors: {total_errors}")
        logger.info(f"⚠️ Total Warnings: {total_warnings}")
        logger.info(f"📂 Total Files Checked: {total_files}")
        logger.info(f"✅ Files Without Issues: {files_without_issues}")
        logger.info(delimiter)

        # Detailed report by file
        logger.info("Detailed Errors")
        logger.info(delimiter)

        for file_path, issues in violations_by_file.items():
            logger.info(f"📄 File: {file_path}")

            if issues['errors']:
                logger.info("  Errors:")
                for error in issues['errors']:
                    logger.info(f"    ❌ [{error['severity']}] {error['message']}")

            if issues['warnings']:
                logger.info("  Warnings:")
                for warning in issues['warnings']:
                    logger.info(f"    ⚠️ [{warning['severity']}] {warning['message']}")

            # Add file separator after each file's details
            logger.info(file_separator)

        logger.info("Completed validation")
    
    elif output_format == 'json':
        # JSON output
        import json
        result = {
            "summary": {
                "total_errors": total_errors,
                "total_warnings": total_warnings,
                "total_files": total_files,
                "files_without_issues": files_without_issues
            },
            "violations_by_file": violations_by_file
        }
        logger.info(json.dumps(result, indent=2))
    
    else:
        logger.error(f"Unsupported output format: {output_format}")