import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook


def get_stock(url, target):
    res = requests.get(url)

    soup = BeautifulSoup(res.text, 'html.parser')

    stock = soup.select('p.stock')[0].text

    if stock == '尚有庫存':
        send_message(f'{target} {stock}')
    else:
        if debug:
            send_message(f'{target} {stock}')

def send_message(content):
    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/1109279748795936848/-baQ0pzmy5h3n4vPZa59pL_NUzWinCagMOYDC8ziCgsEs1tP8JXt-aHESUL2ntWc_RqC',
                        content=content,
                        username='拍立得底片進貨通知')
    webhook.execute()

if __name__ == '__main__':
    debug = False

    products = [
        ('https://myfuji.com.tw/product/instax-instantfilm-whiteframe/', '白邊底片 10張'),
        ('https://myfuji.com.tw/product/instax-mini-film-2packs/', '白邊底片 20張(2包)')
    ]

    for url, target in products:
        get_stock(url, target)
