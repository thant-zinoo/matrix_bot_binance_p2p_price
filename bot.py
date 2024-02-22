import simplematrixbotlib as botlib
import os
import binance

config = botlib.Config()
config.emoji_verify = True
config.ignore_unverified_devices = True

creds = botlib.Creds(
    os.getenv("MATRIX_URL"), os.getenv("MATRIX_USER"), os.getenv("MATRIX_PASS")
)
bot = botlib.Bot(creds, config)
PREFIX = "!"


@bot.listener.on_message_event
async def echo(room, message):
    match = botlib.MessageMatch(room, message, bot, PREFIX)
    if match.prefix():
        # if match.is_not_from_this_bot() and match.prefix():

        if match.command("binance"):
            try:
                await bot.api.send_text_message(room.room_id, "Getting Binance Data...")
                header_rows = """<table>
                                    <tr>
                                        <th>Type</th>
                                        <th>User</th>
                                        <th>Rate</th>
                                        <th>Amount</th>
                                        <th>Method</th>
                                    </tr>"""
                footer_rows = "</table>"
                binance_buy_data = binance.get_binance_data("BUY")
                binance_sell_data = binance.get_binance_data("SELL")
                result_html = header_rows
                for sell_data in binance_sell_data.get("data"):
                    result_html = result_html + binance.format_binance_api(sell_data)
                for buy_data in binance_buy_data.get("data"):
                    result_html = result_html + binance.format_binance_api(buy_data)
                result_html = result_html + footer_rows
                await bot.api.send_markdown_message(room.room_id, result_html)
            except Exception as e:
                print(e)
                await bot.api.send_text_message(room.room_id, "An error occurs")


bot.run()
