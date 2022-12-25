from django.core.management import BaseCommand

from bot.models import TgUser
from bot.tg import tg_client, TgClient
from bot.tg.bot import TgBot
from bot.tg.dc import Message


class Command(BaseCommand):
    help = "Команда для запуска telegram бота"
    tg_client = TgClient('5675446457:AAF_OxnucNhYTRbPQJneo2eGv5k2futQdmk')

    def handle_univerified_user(self, msg: Message, tg_user: TgUser):
        code = '123'
        tg_user.verification_code = code
        tg_user.save()
        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=f' {code}'
        )

    def handle_user(self, msg: Message):
        tg_user = TgUser.objects.filter(tg_user_id=msg.from_.id)
        if tg_user:
            self.tg_client.send_message(chat_id=msg.chat.id, text='Здравствуйте!')
        else:
            self.tg_client.send_message(chat_id=msg.chat.id, text='Уже был!')

    def handle(self, *args, **options):
        offset = 0
        while True:
            res = tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                print(item.message)
