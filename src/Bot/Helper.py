class Helper:
    @staticmethod
    def is_bot_tagged(message_text):
        return str(bot_client.user.id) in message_text

    @staticmethod
    def is_bot_command(message_text):
        return message_text in list(command_list.values())
