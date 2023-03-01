from instagrapi.utils import dumps


class BloksMixin:
    bloks_versioning_id = "0ee04a4a6556c5bb584487d649442209a3ae880ae5c6380b16235b870fcc4052"

    def bloks_action_raw(self, action: str, data: dict, with_signature = True):
        """Performing actions for bloks

        Parameters
        ----------
        action: str
            Action, example "com.instagram.challenge.navigation.take_challenge"
        data: dict
            Additional data

        Returns
        -------
        bool
        """
        result = self.private_request(
            f"bloks/apps/{action}/", data, with_signature=with_signature
        )

        return result
        # return result["status"] == "ok"

    def bloks_action(self, action: str, data: dict, with_signature = True) -> bool:
        """Performing actions for bloks

        Parameters
        ----------
        action: str
            Action, example "com.instagram.challenge.navigation.take_challenge"
        data: dict
            Additional data

        Returns
        -------
        bool
        """
        result = self.private_request(
            f"bloks/apps/{action}/", self.with_default_data(data), with_signature=with_signature
        )
        return result
        # return result["status"] == "ok"

    def bloks_change_password(self, password: str, challenge_context: dict) -> bool:
        """
        Change password for challenge

        Parameters
        ----------
        passwrd: str
            New password

        Returns
        -------
        bool
        """
        assert (
            self.bloks_versioning_id
        ), "Client.bloks_versioning_id is empty (hash is expected)"
        enc_password = self.password_encrypt(password)
        data = {
            "bk_client_context": dumps(
                {"bloks_version": self.bloks_versioning_id, "styles_id": "instagram"}
            ),
            "challenge_context": challenge_context,
            "bloks_versioning_id": self.bloks_versioning_id,
            "enc_new_password1": enc_password,
            "enc_new_password2": enc_password,
        }
        return self.bloks_action(
            "com.instagram.challenge.navigation.take_challenge", data
        )
