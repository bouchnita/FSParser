# FSParser

This script parses MBR partitions, FAT32 filesystems, and EXT filesystems to extract useful information.

## Features
- Parses MBR partitions and displays partition table information, such as partition type and size.
- Parses FAT32 filesystems and displays information about the filesystem, such as total size, free space, and cluster size.
- Parses EXT filesystems and displays information about the filesystem, such as total size, free space, and inode count.
- Accepts command line arguments to control script behavior.
    - `-h`: Display help message.
    - `-m`: Parse MBR partition only.
    - `-i <image>`: Specify the image file to parse.
    - `-f`: Parse the filesystem only.

## Usage
1. Clone the repository.
2. Run the script using `python FSParser.py` (check --help for further infos).
3. Follow the instructions provided by the script.

Example usage:

python disk_parser.py -i disk_image.img -m


This will parse the MBR partition of the `disk_image.img` file.

## Contributions
Contributions are welcome! If you would like to contribute, please open a pull request with your changes. If you would like to add support for more filesystems, please make sure to include tests and documentation for your changes.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

