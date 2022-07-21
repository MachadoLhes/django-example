def parse_stock(stock_line):
    stock_split = stock_line.lower().split('\n')

    keys = stock_split[0].replace('\r','').split(',')
    values = stock_split[1].replace('\r','').split(',')

    stock = dict(zip(keys, values))

    return stock