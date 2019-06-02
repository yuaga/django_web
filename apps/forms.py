class FormMixin(object):
    def get_errors(self):
        messages = []
        if hasattr(self, 'errors'):
            errors = self.errors.get_json_data()
            for message_dicts in errors.values():
                for message in message_dicts:
                    messages.append(message['message'])
            return messages[0]
        else:
            return {}