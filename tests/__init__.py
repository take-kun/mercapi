from vcr import VCR

my_vcr = VCR(
    cassette_library_dir='cassettes',
    path_transformer=VCR.ensure_suffix('.yml'),
)
