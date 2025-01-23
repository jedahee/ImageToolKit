import warnings
import argparse
import sys, os
from PIL import Image
from src.compress import compress
from src.rescale import process_images_resize
from src.extension import new_format
from src.color import apply_filter_to_images
from src.addtext import add_text_to_image, get_available_fonts
from src.utils import display_msg
from src.variables import msg_allowed, available_filters, valid_extensions

# Main function to handle command-line interface (CLI) commands
def cli():
    # Suppress decompression bomb warnings from PIL
    warnings.simplefilter('ignore', Image.DecompressionBombWarning)

    # Create an argument parser for the CLI tool
    parser = argparse.ArgumentParser(
        description="Image Tools CLI: A comprehensive command-line tool for editing images.",
        epilog="For more information, consult the documentation or use the specific command's --help flag.",
    )

    # Define subcommands for the CLI
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Reduce command: Reduce the file size of images
    reduce_parser = subparsers.add_parser(
        "reduce",
        help="Reduce the file size of the image(s).",
        description=(
            "This command reduces the size of image files to a specified maximum size "
            "(512KB, 1024KB, or 2048KB). You can allow resizing and force quality reduction if necessary."
        ),
    )
    reduce_parser.add_argument("directory", help="Directory containing images.")
    reduce_parser.add_argument(
        "--max-size",
        choices=["512KB", "1024KB", "2048KB"],
        required=True,
        help="Maximum size for the image(s): 512KB, 1024KB, or 2048KB.",
    )
    reduce_parser.add_argument(
        "--resize-allowed",
        action="store_true",
        help="Allow resizing images to smaller dimensions if required.",
    )
    reduce_parser.add_argument(
        "--quality-priority",
        action="store_true",
        help="Force size reduction by compromising on image quality if needed.",
    )

    # Resize command: Resize or scale images
    resize_parser = subparsers.add_parser(
        "resize",
        help="Resize or scale the image(s).",
        description=(
            "This command resizes image(s) to new dimensions or scales them by a percentage. "
            "Use 'fixed' mode for exact dimensions or 'scale' mode for proportional resizing."
        ),
    )
    resize_parser.add_argument("directory", help="Directory containing images.")
    resize_parser.add_argument(
        "--resize-mode",
        choices=["fixed", "scale"],
        required=True,
        help="Resize mode: 'fixed' for specific dimensions or 'scale' for percentage resizing.",
    )
    resize_parser.add_argument(
        "--size-dimensions",
        nargs=2,
        type=int,
        metavar=("WIDTH", "HEIGHT"),
        help="New dimensions for the image(s) (required for 'fixed' mode). Example: --size-dimensions 1920 1080",
    )
    resize_parser.add_argument(
        "--scale-percentage",
        type=int,
        help="Scaling percentage for the image(s) (required for 'scale' mode). Example: --scale-percentage 50",
    )

    # Format conversion command: Convert the format of the images
    format_parser = subparsers.add_parser(
        "convert",
        help="Convert the format of the image(s).",
        description=(
            "This command converts image(s) to a specified format (JPEG, PNG, BMP). "
            "Optionally, you can rename the files during conversion."
        ),
    )
    format_parser.add_argument("directory", help="Directory containing images.")
    format_parser.add_argument(
        "--output-format",
        choices=["JPEG", "PNG", "BMP"],
        required=True,
        help="Target format for the image(s).",
    )
    format_parser.add_argument(
        "--rename-files",
        action="store_true",
        help="Rename the files during format conversion.",
    )
    format_parser.add_argument(
        "--file-base-name",
        help="Base name for renamed files (required if --rename-files is used). Example: --file-base-name image",
    )

    # Filters command: Apply filters (e.g., grayscale, sepia) to images
    filters_parser = subparsers.add_parser(
        "filter",
        help="Apply filters to the image(s).",
        description=(
            "This command applies a filter (e.g., grayscale, sepia) to the image(s). "
            "Choose a filter from the list of available options."
        ),
    )
    filters_parser.add_argument("directory", help="Directory containing images.")
    filters_parser.add_argument(
        "--filter-type",
        choices=available_filters,
        required=True,
        help=f"Filter to apply to the images. Available options: {', '.join(available_filters)}.",
    )

    # Add text command: Add custom text to the images
    text_parser = subparsers.add_parser(
        "add-text",
        help="Add text to the image(s).",
        description=(
            "This command adds custom text to image(s) at a specified position. "
            "You can customize the font, size, color, and position of the text."
        ),
    )
    text_parser.add_argument("directory", help="Directory containing images.")
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

    # Parse the command-line arguments
    args = parser.parse_args()

    # Check if the specified directory exists
    if not os.path.exists(args.directory):
        display_msg("The specified directory does not exist. Please check the path and try again.", msg_allowed["ERROR"], True)
    else:
        # Get list of image files in the directory
        files = os.listdir(args.directory)
        images = [file for file in files if os.path.isfile(os.path.join(args.directory, file)) and os.path.splitext(file)[1].lower() in valid_extensions]

        # Execute the corresponding command based on user input
        if args.command == "reduce":
            # Compress the images to the specified maximum size
            compress(args.directory, images, args.resize_allowed, args.quality_priority, args.max_size)

        elif args.command == "resize":
            # Resize or scale the images
            if args.resize_mode == "fixed":
                if not args.size_dimensions:
                    display_msg("Dimensions are required for fixed mode", msg_allowed["ERROR"], False)
                    sys.exit(1)
                process_images_resize(args.directory, images, args.resize_mode, tuple(args.size_dimensions), None)
            elif args.resize_mode == "scale":
                if not args.scale_percentage:
                    display_msg("Scale percentage is required for scale mode", msg_allowed["ERROR"], False)
                    sys.exit(1)
                process_images_resize(args.directory, images, args.resize_mode, args.scale_percentage, None)

        elif args.command == "convert":
            # Convert images to the specified format and optionally rename them
            if args.rename_files and not args.file_base_name:
                display_msg("Base name is required if renaming files", msg_allowed["ERROR"], False)
                sys.exit(1)
            new_format(args.directory, images, args.output_format, args.rename_files, args.file_base_name)

        elif args.command == "filter":
            # Apply the selected filter to the images
            apply_filter_to_images(args.directory, images, args.filter_type)

        elif args.command == "add-text":
            # Add custom text to the images
            available_fonts = get_available_fonts()
            font_choice = args.font if args.font else (available_fonts[0] if available_fonts else None)
            if not font_choice:
                display_msg("No fonts available in the fonts directory", msg_allowed["ERROR"], False)
                sys.exit(1)
            add_text_to_image(
                args.directory, images, args.text, args.position, font_choice, args.size, args.color
            )

        else:
            # Show help if no valid command is provided
            parser.print_help()
