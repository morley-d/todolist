from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from goals.models import Goal, Category, Board


class BotGoal:
    def __init__(self, tg_user: TgUser, msg: Message, tg_client: TgClient):
        self.tg_user = tg_user
        self.msg = msg
        self.tg_client = tg_client

    def get_goal(self, first: bool = False, tg: bool = False) -> None:
        goals = Goal.objects.filter(user=self.tg_user.user, category__is_deleted=False)
        if first and tg:
            goals.filter(category__title__contains='tg').order_by('-created').first()
        if not first and not tg:
            goals = goals
        if first and not tg:
            goals.first()
        if not first and tg:
            goals.filter(category__title__contains='tg').order_by('-created')

        if goals.count() > 0:
            for goal in goals:
                self.tg_client.send_message(
                    chat_id=self.msg.chat.id,
                    text=f'Заголовок: {goal.title}\n'
                         f'Описание: {goal.description if goal.due_date else "Не указано"}\n'
                         f'Дата выполнения: {goal.due_date if goal.due_date else "Не указана"}\n'
                         f'Статус: {goal.get_priority_display()}\n'
                         f'Приоритет: {goal.get_priority_display()}\n'
                         f'Категория: {goal.category.title}'
                )

    def check_user(self) -> None:
        self.tg_user.set_verification_code()
        self.tg_user.save(update_fields=['verification_code'])
        self.tg_client.send_message(
            chat_id=self.msg.chat.id, text=f'Подтвердите, пожалуйста, свой аккаунт. '
                                           f'Для подтверждения необходимо ввести код: '
                                           f'{self.tg_user.verification_code} на сайте: skotenkov.tk'
        )

    def create_goal(self) -> None:
        line_break = '\n'
        categories = Category.objects.filter(user=self.tg_user.user)
        if '/create' == self.msg.text and categories.count() > 0:
            self.tg_client.send_message(
                chat_id=self.msg.chat.id,
                text=f"Выберите категорию из списка или введите новую\n"
                     f"(Введите: 'create_cat Название категории' или 'cat Название категории'):\n"
                     f"{(f'{line_break}'.join(category.title for category in categories))}"
            )
        elif '/create' == self.msg.text and categories.count() == 0:
            self.tg_client.send_message(
                chat_id=self.msg.chat.id,
                text=f"Категорий нет создайте новую\n"
                     f"(Введите: 'create_cat Название категории')"
            )
        elif 'create_cat' in self.msg.text:
            text = self.msg.text.replace('create_cat', 'tg')
            board = Board.objects.filter(title='Telegram board').first()
            category = Category(
                title=text,
                user=self.tg_user.user,
                board_id=board.id
            )
            category.save()
            self.tg_client.send_message(
                chat_id=self.msg.chat.id,
                text=f"Категория сохранена, для того что добавить цель\n"
                     f"(Введите: 'create_goal Название цели')"
            )

        elif 'create_goal' in self.msg.text:
            text = self.msg.text.replace('create_goal', 'tg')
            category = Category.objects.filter(
                title__contains='tg',
                user_id=self.tg_user.user.id
            ).first()
            goal = Goal(
                title=text,
                user=self.tg_user.user,
                category=category
            )
            goal.save()

            self.get_goal(first=True, tg=True)
