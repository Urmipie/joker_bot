from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class VkMessage:
    def __init__(self, text: str, buttons: list, one_time=False, inline=False):
        self.text = text
        if not self.text:
            self.text = 'Варианты:'
        self.keyboard = VkKeyboard(one_time=one_time, inline=inline)
        self.description = '\n'.join(map(lambda x: str(x[0]) + ') ' + x[1].capitalize(), enumerate(buttons)))
        buttons = buttons.copy()
        self.keyboard.add_button(label=buttons.pop(0), color=VkKeyboardColor.PRIMARY)
        for button in buttons:
            self.keyboard.add_line()
            self.keyboard.add_button(label=button, color=VkKeyboardColor.PRIMARY)

    def get(self, keyboard):
        if keyboard and self.keyboard:
            return dict(message=self.text, keyboard=self.keyboard.get_keyboard())
        else:
            return dict(message=self.text + '\n' + self.description)
