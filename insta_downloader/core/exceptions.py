import logging

logger = logging.getLogger(__name__)


class PrivateAccountException(Exception):
    def __init__(self, lang=None):
        self.message = "private_account_ig"
        super().__init__(self.message)
