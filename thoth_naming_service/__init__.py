import os


__version__ = '0.3.0'
__description__ = 'Thoth: Naming Service, ask me if you want to find things...'
__git_commit_id__ = os.getenv('OPENSHIFT_BUILD_COMMIT', '')


def _get_api_token() -> str:
    """Get token to Kubernetes master."""
    try:
        with open('/var/run/secrets/kubernetes.io/serviceaccount/token', 'r') as token_file:
            return token_file.read()
    except FileNotFoundError as exc:
        raise FileNotFoundError("Unable to get service account token, please check that service has "
                                "service account assigned with exposed token") from exc
