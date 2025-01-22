import argparse
import sys
from src.compress import compress
from src.rescale import process_images_resize
from src.extension import new_format
from src.color import apply_filter_to_images
from src.addtext import add_text_to_image, get_available_fonts
from src.utils import display_msg
from src.variables import msg_allowed, available_filters


def cli():
    parser = argparse.ArgumentParser(
        description="Image Tools CLI: A comprehensive command-line tool for editing images.",
        epilog="For more information, consult the documentation or use the specific command's --help flag.",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Reduce command
    reduce_parser = subparsers.add_parser(
        "reduce",
        help="Reduce the file size of the image(s).",
        description=(
            "This command reduces the size of image files to a specified maximum size "
            "(512KB, 1024KB, or 2048KB). You can allow resizing and force quality reduction if necessary."
        ),
    )
    reduce_parser.add_argument("path", help="Path to the directory containing images.")
    reduce_parser.add_argument(
        "--max-size",
        choices=["512KB", "1024KB", "2048KB"],
        required=True,
        help="Maximum size for the image(s): 512KB, 1024KB, or 2048KB.",
    )
    reduce_parser.add_argument(
        "--can-resize",
        action="store_true",
        help="Allow resizing images to smaller dimensions if required.",
    )
    reduce_parser.add_argument(
        "--force",
        action="store_true",
        help="Force size reduction by compromising on image quality if needed.",
    )

    # Resize command
    resize_parser = subparsers.add_parser(
        "resize",
        help="Resize or scale the image(s).",
        description=(
            "This command resizes image(s) to new dimensions or scales them by a percentage. "
            "Use 'fixed' mode for exact dimensions or 'scale' mode for proportional resizing."
        ),
    )
    resize_parser.add_argument("path", help="Path to the directory containing images.")
    resize_parser.add_argument(
        "--mode",
        choices=["fixed", "scale"],
        required=True,
        help="Resize mode: 'fixed' for specific dimensions or 'scale' for percentage resizing.",
    )
    resize_parser.add_argument(
        "--dimensions",
        nargs=2,
        type=int,
        metavar=("WIDTH", "HEIGHT"),
        help="New dimensions for the image(s) (required for 'fixed' mode). Example: --dimensions 1920 1080",
    )
    resize_parser.add_argument(
        "--scale",
        type=int,
        help="Scaling percentage for the image(s) (required for 'scale' mode). Example: --scale 50",
    )

    # Format conversion command
    format_parser = subparsers.add_parser(
        "convert",
        help="Convert the format of the image(s).",
        description=(
            "This command converts image(s) to a specified format (JPEG, PNG, BMP). "
            "Optionally, you can rename the files during conversion."
        ),
    )
    format_parser.add_argument("path", help="Path to the directory containing images.")
    format_parser.add_argument(
        "--format",
        choices=["JPEG", "PNG", "BMP"],
        required=True,
        help="Target format for the image(s).",
    )
    format_parser.add_argument(
        "--rename",
        action="store_true",
        help="Rename the files during format conversion.",
    )
    format_parser.add_argument(
        "--base-name",
        help="Base name for renamed files (required if --rename is used). Example: --base-name image",
    )

    # Filters command
    filters_parser = subparsers.add_parser(
        "filter",
        help="Apply filters to the image(s).",
        description=(
            "This command applies a filter (e.g., grayscale, sepia) to the image(s). "
            "Choose a filter from the list of available options."
        ),
    )
    filters_parser.add_argument("path", help="Path to the directory containing images.")
    filters_parser.add_argument(
        "--filter",
        choices=available_filters,
        required=True,
        help=f"Filter to apply to the images. Available options: {', '.join(available_filters)}.",
    )

    # Add text command
    text_parser = subparsers.add_parser(
        "add-text",
        help="Add text to the image(s).",
        description=(
            "This command adds custom text to image(s) at a specified position. "
            "You can customize the font, size, color, and position of the text."
        ),
    )
    text_parser.add_argument("path", help="Path to the directory containing images.")
    text_parser.add_argument("--text", required=True, help="Text to add to the image(s).")
    text_parser.add_argument(
        "--font",
        help="Font to use for the text. Default: the first available font in the fonts directory.",
    )
    text_parser.add_argument(
        "--size",
        type=float,
        help="Font size as a percentage of image width. Example: --size 5.0 (5% of the image width).",
    )
    text_parser.add_argument(
        "--color",
        choices=["black", "white", "red", "blue", "green"],
        required=True,
        help="Color of the text.",
    )
    text_parser.add_argument(
        "--position",
        choices=["Top Left", "Top Right", "Center", "Bottom Left", "Bottom Right"],
        required=True,
        help="Position of the text on the image. Example: --position 'Top Left'.",
    )

    # Parse arguments
    args = parser.parse_args()

    if args.command == "reduce":
        compress(args.path, [], args.can_resize, args.force, args.max_size)

    elif args.command == "resize":
        if args.mode == "fixed":
            if not args.dimensions:
                display_msg("Dimensions are required for fixed mode", msg_allowed["ERROR"], False)
                sys.exit(1)
            process_images_resize(args.path, [], args.mode, tuple(args.dimensions), None)
        elif args.mode == "scale":
            if not args.scale:
                display_msg("Scale percentage is required for scale mode", msg_allowed["ERROR"], False)
                sys.exit(1)
            process_images_resize(args.path, [], args.mode, args.scale, None)

    elif args.command == "convert":
        if args.rename and not args.base_name:
            display_msg("Base name is required if renaming files", msg_allowed["ERROR"], False)
            sys.exit(1)
        new_format(args.path, [], args.format, args.rename, args.base_name)

    elif args.command == "filter":
        apply_filter_to_images(args.path, [], args.filter)

    elif args.command == "add-text":
        available_fonts = get_available_fonts()
        font_choice = args.font if args.font else (available_fonts[0] if available_fonts else None)
        if not font_choice:
            display_msg("No fonts available in the fonts directory", msg_allowed["ERROR"], False)
            sys.exit(1)
        add_text_to_image(
            args.path, [], args.text, args.position, font_choice, args.size, args.color
        )

    else:
        parser.print_help()
