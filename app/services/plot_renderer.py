import matplotlib.pyplot as plt


def plot_rates_evolution(rate_list, bank_name, coin_name):
    rate_sell = [r.rate_sell for r in rate_list]
    rate_buy = [r.rate_buy for r in rate_list]
    rate_date = [r.date for r in rate_list]

    # date_start = min(rate_date)
    # date_end = max(rate_date)

    path = f'static/plot/rates_{bank_name}_{coin_name}.png'

    plt.title(f'Evolutia ratelor {bank_name} pentru {coin_name}')  # noqa
    plt.grid(b=None, which='major', axis='both')

    plt.xticks(rotation=90)
    plt.yticks(rotation=0)

    plt.xlabel('Data')
    plt.ylabel('Pretul in MDL')  # noqa

    plt.plot(rate_date, rate_buy, 'r', label='Cumparare')  # noqa

    for a, b in zip(rate_buy, rate_date):
        plt.annotate(str(a), xy=(a, b))

    plt.plot(rate_date, rate_sell, 'b', label='Vinzare')  # noqa

    for a, b in zip(rate_sell, rate_date):
        plt.annotate(str(a), xy=(a, b))

    plt.legend()

    plt.savefig(path)
    plt.close()

    return path
