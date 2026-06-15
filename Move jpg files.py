import os
import shutil
from datetime import datetime

# ─────────────────────────────────────────────────────
#  Horizon TechX — Task 3: Task Automation with Python
#  Sub-task : Move all .jpg files from one folder
#             to another folder automatically
#  Key concepts: os, shutil, file handling
# ─────────────────────────────────────────────────────


def get_folder(prompt, must_exist=True):
    """Prompt the user for a folder path and validate it."""
    while True:
        path = input(prompt).strip().strip('"').strip("'")
        if not path:
            print("  ⚠  Path cannot be empty. Try again.\n")
            continue
        if must_exist and not os.path.isdir(path):
            print(f"  ⚠  Folder not found: {path}")
            print("  ℹ  Please enter a valid existing folder path.\n")
            continue
        return path


def move_jpg_files(source_folder, dest_folder, rename_duplicates=True):
    """
    Move all .jpg / .jpeg files from source_folder to dest_folder.
    Returns a summary dict with moved, skipped, and error counts.
    """
    os.makedirs(dest_folder, exist_ok=True)

    summary = {"moved": [], "skipped": [], "errors": []}

    # Collect all .jpg / .jpeg files (case-insensitive)
    all_files = os.listdir(source_folder)
    jpg_files = [
        f for f in all_files
        if f.lower().endswith((".jpg", ".jpeg"))
        and os.path.isfile(os.path.join(source_folder, f))
    ]

    if not jpg_files:
        return summary  # nothing to move

    print(f"\n  Found {len(jpg_files)} .jpg file(s). Starting transfer...\n")

    for filename in jpg_files:
        src_path = os.path.join(source_folder, filename)
        dst_path = os.path.join(dest_folder, filename)

        # ── Handle duplicate filenames ───────────────
        if os.path.exists(dst_path):
            if rename_duplicates:
                name, ext = os.path.splitext(filename)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                new_name  = f"{name}_{timestamp}{ext}"
                dst_path  = os.path.join(dest_folder, new_name)
                print(f"  ⚠  Duplicate — renaming to: {new_name}")
            else:
                print(f"  ⏭  Skipped (already exists): {filename}")
                summary["skipped"].append(filename)
                continue

        # ── Move the file ────────────────────────────
        try:
            shutil.move(src_path, dst_path)
            moved_name = os.path.basename(dst_path)
            print(f"  ✅  Moved: {filename}"
                  + (f" → {moved_name}" if moved_name != filename else ""))
            summary["moved"].append(filename)
        except Exception as e:
            print(f"  ❌  Error moving '{filename}': {e}")
            summary["errors"].append((filename, str(e)))

    return summary


def print_summary(summary, source, dest):
    """Print a final report of the operation."""
    total   = len(summary["moved"]) + len(summary["skipped"]) + len(summary["errors"])
    divider = "─" * 52

    print("\n  " + "═" * 52)
    print("         📁  MOVE OPERATION SUMMARY")
    print("  " + "═" * 52)
    print(f"  Source      : {source}")
    print(f"  Destination : {dest}")
    print(f"  " + divider)
    print(f"  Total .jpg files found  : {total}")
    print(f"  ✅  Successfully moved  : {len(summary['moved'])}")
    print(f"  ⏭  Skipped (duplicate) : {len(summary['skipped'])}")
    print(f"  ❌  Errors              : {len(summary['errors'])}")
    print("  " + "═" * 52)

    if summary["errors"]:
        print("\n  Files with errors:")
        for fname, err in summary["errors"]:
            print(f"    • {fname}: {err}")

    if not summary["moved"] and not summary["skipped"] and not summary["errors"]:
        print("\n  ℹ  No .jpg or .jpeg files were found in the source folder.")

    print()


def save_log(summary, source, dest):
    """Optionally save a log file of the operation."""
    log_path = os.path.join(dest, f"move_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    with open(log_path, "w") as f:
        f.write("=" * 52 + "\n")
        f.write("  JPG FILE MOVE — OPERATION LOG\n")
        f.write(f"  Date    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"  Source  : {source}\n")
        f.write(f"  Dest    : {dest}\n")
        f.write("=" * 52 + "\n\n")

        f.write(f"MOVED ({len(summary['moved'])}):\n")
        for name in summary["moved"]:
            f.write(f"  + {name}\n")

        f.write(f"\nSKIPPED ({len(summary['skipped'])}):\n")
        for name in summary["skipped"]:
            f.write(f"  - {name}\n")

        f.write(f"\nERRORS ({len(summary['errors'])}):\n")
        for name, err in summary["errors"]:
            f.write(f"  ! {name}: {err}\n")

    print(f"  📄  Log saved → {os.path.abspath(log_path)}\n")


def main():
    print("\n" + "═" * 52)
    print("     📂  JPG FILE MOVER — Horizon TechX")
    print("  " + "Task 3: Task Automation with Python Scripts")
    print("═" * 52)
    print("  Moves all .jpg / .jpeg files from a source")
    print("  folder into a destination folder automatically.\n")

    # ── Get source folder ────────────────────────────
    source = get_folder("  Enter SOURCE folder path\n  (where .jpg files are): ", must_exist=True)

    # ── Preview what will be moved ───────────────────
    all_jpgs = [
        f for f in os.listdir(source)
        if f.lower().endswith((".jpg", ".jpeg"))
        and os.path.isfile(os.path.join(source, f))
    ]

    if not all_jpgs:
        print(f"\n  ℹ  No .jpg or .jpeg files found in:\n  {source}")
        print("  Nothing to move. Exiting.\n")
        return

    print(f"\n  Found {len(all_jpgs)} .jpg file(s) in source folder:")
    for f in all_jpgs[:10]:
        print(f"    • {f}")
    if len(all_jpgs) > 10:
        print(f"    ... and {len(all_jpgs) - 10} more.")

    # ── Confirm before proceeding ────────────────────
    confirm = input("\n  Proceed? (y/n): ").strip().lower()
    if confirm != "y":
        print("\n  Operation cancelled. No files were moved.\n")
        return

    # ── Get destination folder ───────────────────────
    dest = get_folder(
        "\n  Enter DESTINATION folder path\n"
        "  (will be created if it doesn't exist): ",
        must_exist=False
    )

    # ── Duplicate handling preference ────────────────
    print("\n  If a file with the same name exists in destination:")
    print("  [1] Rename with timestamp (safe — default)")
    print("  [2] Skip the duplicate")
    dup_choice = input("  Your choice (1/2): ").strip()
    rename_dupes = dup_choice != "2"

    # ── Run the automation ───────────────────────────
    print()
    summary = move_jpg_files(source, dest, rename_duplicates=rename_dupes)

    # ── Print summary ────────────────────────────────
    print_summary(summary, source, dest)

    # ── Optionally save log ──────────────────────────
    if summary["moved"] or summary["errors"]:
        save = input("  Save operation log to destination folder? (y/n): ").strip().lower()
        if save == "y":
            save_log(summary, source, dest)


if __name__ == "__main__":
    main()