import datetime
import os
from pathlib import Path

from reports_generation.scripts import (config_provider, csv_aggregator, chart_generator,
                                        summary_aggregator, results_archivator, judgement)


def main():
    results_dir = __get_results_dir()

    config = config_provider.get_config()
    agg_csv = csv_aggregator.aggregate(config, results_dir)
    agg, scenario_status = summary_aggregator.aggregate(config, results_dir)
    chart_generator_config = config_provider.get_chart_generator_config(config, agg_csv)
    chart_generator.perform_chart_creation(chart_generator_config, results_dir, scenario_status)
    results_archivator.archive_results(config, results_dir)

    if config['judge']:
        baseline_result_dir = next((run for run in config['runs'] if run['runType'] == 'baseline'))['fullPath']
        tested_result_dir = next((run for run in config['runs'] if run['runType'] == 'experiment'))['fullPath']
        judgement.judge_results(baseline_result_dir=baseline_result_dir,
                                tested_result_dir=tested_result_dir)


def __get_results_dir() -> Path:
    path = (Path(__file__).absolute().parents[1] / "results" / "reports" /
            datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    path.mkdir(parents=True, exist_ok=True)
    return path


if __name__ == "__main__":
    main()
