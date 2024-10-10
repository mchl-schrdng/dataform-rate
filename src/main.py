import argparse
import logging
from parser import get_all_models
from evaluator import evaluate_models
from reporter import report_violations

def main():
    parser = argparse.ArgumentParser(description='Dataform Rate Tool')
    parser.add_argument('--model-path', type=str, default='../models/**/*.sqlx',
                        help='Glob pattern to find .sqlx model files')
    parser.add_argument('--max-lines', type=int, default=200,
                        help='Maximum allowed number of SQL lines')
    parser.add_argument('--output-format', type=str, default='console',
                        choices=['console', 'json'],
                        help='Format of the output report')
    parser.add_argument('--log-level', type=str, default='INFO',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                        help='Logging level')
    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.log_level.upper()))
    logging.debug("Starting Dataform Rate Tool...")

    models = get_all_models(model_path=args.model_path)
    if not models:
        print("No models found. Please check the model path and ensure .sqlx files are present.")
        return
    violations = evaluate_models(models, max_lines=args.max_lines)
    report_violations(violations, output_format=args.output_format)

if __name__ == '__main__':
    main()