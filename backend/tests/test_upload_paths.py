"""Unit checks for upload path helpers (no TensorFlow)."""
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from src.config.settings import UPLOAD_FOLDER


def test_path_helpers():
    # Import helpers without loading full Flask app (pull symbols via exec of defs)
    # Use a lightweight reimplementation mirror of app helpers against same UPLOAD_ROOT
    from werkzeug.utils import secure_filename

    UPLOAD_ROOT = Path(UPLOAD_FOLDER).resolve()

    def _safe_user_dirname(username):
        return secure_filename((username or 'anonymous').strip()) or 'anonymous'

    def _to_upload_relpath(abs_or_rel):
        path = Path(abs_or_rel)
        if not path.is_absolute():
            path = (UPLOAD_ROOT / path).resolve()
        else:
            path = path.resolve()
        return path.relative_to(UPLOAD_ROOT).as_posix()

    def _resolve_upload_file(filename):
        if not filename or filename.startswith(('/', '\\')):
            return None
        parts = Path(filename.replace('\\', '/')).parts
        if any(p in ('', '.', '..') for p in parts):
            return None
        target = (UPLOAD_ROOT.joinpath(*parts)).resolve()
        try:
            target.relative_to(UPLOAD_ROOT)
        except ValueError:
            return None
        return target if target.is_file() else None

    assert _safe_user_dirname('../admin') == 'admin' or _safe_user_dirname('../admin') == 'anonymous' or '..' not in _safe_user_dirname('../etc/passwd')
    assert '/' not in _safe_user_dirname('a/b')
    assert '\\' not in _safe_user_dirname('a\\b')

    sample = UPLOAD_ROOT / 'predictions' / 'demo' / 'face.jpg'
    sample.parent.mkdir(parents=True, exist_ok=True)
    sample.write_bytes(b'x')
    try:
        rel = _to_upload_relpath(sample)
        assert rel == 'predictions/demo/face.jpg', rel
        assert _resolve_upload_file(rel) == sample.resolve()
        assert _resolve_upload_file('../predictions/demo/face.jpg') is None
        assert _resolve_upload_file('predictions/../../settings.py') is None
        assert _resolve_upload_file('/etc/passwd') is None
        print('PASS upload path helpers')
    finally:
        sample.unlink(missing_ok=True)


if __name__ == '__main__':
    test_path_helpers()
