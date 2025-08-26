import os
import importlib.util
import shutil
import filecmp
from pathlib import Path
from typing import Callable
from utils import logger


def iter_files(from_dir: str, to_dir: str, ext: str):
    """
    Recursively walk from_dir, yield (src_file, dest_file) pairs for .py files.
    Only yield if the file is new or changed relative to dest_file.
    """
    from_path = Path(from_dir).resolve()
    to_path = Path(to_dir).resolve()

    if not from_path.exists():
        raise FileNotFoundError(f"Source directory {from_path} does not exist")

    for root, _, files in os.walk(from_path):
        root_path = Path(root)
        py_files = [f for f in files if f.endswith(ext)]
        if not py_files:
            continue

        rel_subdir = root_path.relative_to(from_path)
        dest_subdir = to_path / rel_subdir
        dest_subdir.mkdir(parents=True, exist_ok=True)

        for py_file in py_files:
            src_file = root_path / py_file
            dest_file = dest_subdir / py_file

            needs_copy = not dest_file.exists() or not filecmp.cmp(
                src_file, dest_file, shallow=False
            )
            if needs_copy:
                yield src_file, dest_file


def process_file(
    src_file: Path, dest_file: Path, line_to_replace: str, replacement_line: str
) -> None:
    """
    Copy a .py file from src_file to dest_file, transforming one line (we used it to replace the import line to cover for one corner case):
    - line_to_replace must exist and will be commented out; if missing, warn and copy unchanged.
    - replacement_line is ensured:
        * uncommented if it was commented out
        * inserted after line_to_replace if it was missing
    """
    with src_file.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    old_line_idx = None
    found_new_commented = False
    found_new_active = False
    new_lines = []

    for idx, line in enumerate(lines):
        stripped = line.strip()
        if stripped == line_to_replace:
            old_line_idx = idx
            new_lines.append("# " + line if not line.startswith("#") else line)
        elif stripped == "# " + replacement_line:
            found_new_commented = True
            new_lines.append(replacement_line + "\n")  # uncomment
        elif stripped == replacement_line:
            found_new_active = True
            new_lines.append(line)  # keep as-is
        else:
            new_lines.append(line)

    if old_line_idx is None:
        logger.warning(f"no '{line_to_replace}' found in {src_file}, file may be bad")
        dest_file.write_text("".join(lines), encoding="utf-8")
        return

    if not (found_new_commented or found_new_active):
        new_lines.insert(old_line_idx + 1, replacement_line + "\n")
        logger.debug(f"inserted new import in {src_file}")

    with dest_file.open("w", encoding="utf-8") as f:
        f.writelines(new_lines)

    logger.debug(f"processed: {src_file} -> {dest_file}")


def copy_replacing_line(
    from_dir: str, to_dir: str, ext: str, line_to_replace: str, replacement_line: str
) -> None:
    """
    Main entry point: copy & transform .py files from from_dir to to_dir.
    """
    for src_file, dest_file in iter_files(from_dir, to_dir, ext):
        process_file(src_file, dest_file, line_to_replace, replacement_line)


def copy_files(from_dir: str, to_dir: str, ext: str = ".py") -> None:
    """
    Recursively copy .py files from from_dir to to_dir.
    - Subdirectories without any .py files are ignored.
    - Files are only copied if they are new or different.
    """
    from_path = Path(from_dir).resolve()
    to_path = Path(to_dir).resolve()

    if not from_path.exists():
        message = f"source directory {from_path} does not exist"
        logger.error(message)
        raise FileNotFoundError(message)

    for root, dirs, files in os.walk(from_path):
        root_path = Path(root)

        # collect .py files in this directory
        py_files = [f for f in files if f.endswith(ext)]

        if not py_files:
            continue  # ignore dirs without .py files

        # destination subdir (preserve relative structure)
        rel_subdir = root_path.relative_to(from_path)
        dest_subdir = to_path / rel_subdir
        dest_subdir.mkdir(parents=True, exist_ok=True)

        for py_file in py_files:
            src_file = root_path / py_file
            dest_file = dest_subdir / py_file

            # copy if file missing OR different
            if not dest_file.exists() or not filecmp.cmp(
                src_file, dest_file, shallow=False
            ):
                shutil.copy2(src_file, dest_file)
                logger.debug(f"copied: {src_file} -> {dest_file}")


def load_user_functions(folder_path: str) -> dict[str, Callable]:
    """
    Recursively load all top-level functions from Python scripts in a folder.

    Args:
        folder_path (str): Path to the folder containing Python scripts.

    Returns:
        dict: A dictionary { "module.func_name": function } with callable objects.
    """
    logger.debug(f"enter, folder_path={folder_path}")

    folder = Path(folder_path).resolve()
    if not folder.is_dir():
        raise ValueError(f"The provided path {folder_path} is not a valid directory")

    user_functions: dict[str, Callable] = {}

    for py_file in folder.rglob("*.py"):  # recursive search
        module_name = py_file.stem
        module_path = str(py_file)

        try:
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                logger.debug("module: %s from %s", module_name, module_path)

                for attr_name in dir(module):
                    if attr_name.startswith("_"):
                        continue
                    attr = getattr(module, attr_name)
                    if callable(attr):
                        key = f"{module_name}.{attr_name}"  # avoid collisions
                        user_functions[key] = attr
                        logger.debug("function: %s", key)
        except Exception as e:
            logger.error("failed to load module %s: %s", module_path, e, exc_info=True)

    return user_functions


def get_next_filename(folder: str, base_name: str, ext: str = ".py") -> tuple[str, int]:

    index = 0
    while True:
        filename = f"{base_name}{index if index > 0 else ''}{ext}"
        file_path = os.path.join(folder, filename)
        if not os.path.exists(file_path):  # Check if file exists
            return file_path, index
        index += 1


if __name__ == "__main__":
    import utils

    utils.setup_logging()

    # functions = load_user_functions(folder_path="./transforms")
    # logger.debug("functions={functions}")

    copy_replacing_line(
        from_dir="./transforms",
        to_dir="./new_transforms",
        ext=".py",
        line_to_replace="from gin.common.tool_decorator import make_tool",
        replacement_line="from asg_runtime import make_tool",
    )
