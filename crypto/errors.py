from cryptography.exceptions import InvalidKey
from crypto import rsa
from core.models import PublicKey, NotificationType


def rsa_keys_check(user):
    private_key = None
    try:
        private_key = rsa.read_private_key(username=user.username)
        public_key = PublicKey.objects.get(user=user)

        if private_key is None or public_key is None:
            return NotificationType.PublicKeyError

        if private_key is None and public_key:
            return NotificationType.PrivateKeyError

        if private_key and public_key is None:
            return NotificationType.PublicKeyError

    except PublicKey.DoesNotExist:
        if private_key is None:
            return NotificationType.NoKeypairError
        return NotificationType.PublicKeyError

    except (UnicodeDecodeError, FileNotFoundError):
        return NotificationType.PrivateKeyError

    except (ValueError, TypeError, InvalidKey):
        return NotificationType.KeypairError

    except Exception as e:
        print(e)
        return NotificationType.Error


def error_message(error_type):
    if error_type == NotificationType.Error:
        return ("System is error.",
                "Error unidentified.")
    elif error_type == NotificationType.KeypairError:
        return ("Your private key or public key has been lost.",
                "Your keypair is broken. Create new keypair to send messages.")
    elif error_type == NotificationType.NoKeypairError:
        return ("You haven't had any keypair yet.",
                "Create new keypair to for more secure messaging.")
    elif error_type == NotificationType.PrivateKeyError:
        return ("Your private key has been corrupted.",
                "You won't be able to receive messages. Recreate new keypair now.")
    elif error_type == NotificationType.PublicKeyError:
        return ("Your public key has been corrupted.",
                "Messages will not be sent. Recreate new keypair now.")
