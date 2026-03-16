from app.core.data_controller import ControlCombiner
from app.services.googleCloud.dependencies import GoogleServiceAccountApiController
from app.services.tafs.controller import TafsController

tafs_ctrl = TafsController()
gmail_api = GoogleServiceAccountApiController()


class CoreControlCombiner(ControlCombiner):
    def __init__(self, tafs, gmail=None):
        (
            self.tafs_ctrl,
            self.gmail_api,
        ) = (
            tafs,
            gmail_api,
        )


ctrl = CoreControlCombiner(tafs=tafs_ctrl, gmail=gmail_api)
