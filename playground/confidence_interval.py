import numpy as np
from scipy import stats

bert_times = [203.39, 210.91, 205.3, 206.9, 208.02]
natasha_times = [1224.29, 1230.79, 1187.21, 1053.67, 1085.78]

def calculate_confidence_interval(execution_times: list, label: str):
    """Вычисление доверительного интервала."""
    confidence: float = 0.95
    n = len(execution_times)
    mean_time: float = np.mean(execution_times)
    std_dev: float = np.std(execution_times, ddof=1)
    t_critical = stats.t.ppf((1 + confidence) / 2, n - 1)
    margin_of_error = t_critical * (std_dev / np.sqrt(n))
    confidence_interval = (mean_time - margin_of_error, mean_time + margin_of_error)
    print(f'For method: {label}')
    print(f'Mean: {mean_time}')
    print(f'Std dev: {std_dev}')
    print(f'Confidence interval: {confidence_interval}')
    print('---------------------------')
    
calculate_confidence_interval(bert_times, label='BERT')
calculate_confidence_interval(natasha_times, label='Natasha')
    