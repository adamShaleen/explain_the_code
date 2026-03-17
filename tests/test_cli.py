from explainer.cli import build_parser


def test_defaults():
    parser = build_parser()
    args = parser.parse_args()

    assert args.file is None
    assert args.question is None
    assert args.language is None
    assert args.verbose is False


def test_file_argument():
    parser = build_parser()
    args = parser.parse_args(["myfile.py"])
    assert args.file == "myfile.py"


def test_question_flag():
    parser = build_parser()
    args = parser.parse_args(["--question", "What does this do?"])
    assert args.question == "What does this do?"


def test_language_flag():
    parser = build_parser()
    args = parser.parse_args(["--language", "rust"])
    assert args.language == "rust"


def test_verbose_flag():
    parser = build_parser()
    args = parser.parse_args(["--verbose"])
    assert args.verbose is True
