def test_package_importable():
    import dc_scs

    assert dc_scs.__version__ == "0.1.0"


def test_manifest_helpers_importable():
    from dc_scs.manifest import MANIFEST_FIELDS, append_manifest_row, sha256_file

    assert "sha256" in MANIFEST_FIELDS
    assert callable(sha256_file)
    assert callable(append_manifest_row)
