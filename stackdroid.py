import argparse
import json
import os
import shutil
import subprocess

def banner():
    BANNER = r"""
 ____  _             _    ____            _     _ 
/ ___|| |_ __ _  ___| | _|  _ \ _ __ ___ (_) __| |
\___ \| __/ _` |/ __| |/ / | | | '__/ _ \| |/ _` |
 ___) | || (_| | (__|   <| |_| | | | (_) | | (_| |
|____/ \__\__,_|\___|_|\_\____/|_|  \___/|_|\__,_|
                                                           
       📦 Detect Android APK Tech Stacks via CLI
"""
    print(BANNER)


def load_signatures(json_path):
    with open(json_path, "r") as file:
        return json.load(file)

def run_apktool(apk_path, output_dir):
    if os.path.exists(output_dir):
        print(f"[!] Output directory {output_dir} already exists. Overwriting...")
    subprocess.run(["apktool", "d", apk_path, "-o", output_dir, "-f"], check=True)

def detect_tech_stack(output_dir, signatures, verbose=False):
    found_stacks = set()
    for tech, patterns in signatures.items():
        for root, dirs, files in os.walk(output_dir):
            all_items = files + dirs
            for item in all_items:
                item_path = os.path.join(root, item)

                # Check filenames and paths
                for pattern in patterns:
                    if pattern.lower() in item.lower() or pattern.lower() in item_path.lower():
                        found_stacks.add(tech)
                        if verbose:
                            print(f"[MATCH:PATH] {tech} ← '{pattern}' matched in path: {item_path}")
                        break

                # Check file contents (binary-safe)
                try:
                    with open(item_path, "rb") as f:
                        content = f.read()
                        for pattern in patterns:
                            byte_pattern = bytes(pattern, "utf-8")
                            if byte_pattern in content:
                                found_stacks.add(tech)
                                if verbose:
                                    try:
                                        with open(item_path, "r", encoding="utf-8", errors="ignore") as text_file:
                                            for line_num, line in enumerate(text_file, start=1):
                                                if pattern in line:
                                                    print(f"[MATCH:CONTENT] {tech} ← '{pattern}' found in {item_path}:{line_num}")
                                                    break
                                    except Exception:
                                        print(f"[MATCH:CONTENT] {tech} ← '{pattern}' found in (binary) {item_path}")
                                break
                except Exception:
                    continue
    return sorted(found_stacks)

def main():
    banner()
    parser = argparse.ArgumentParser(description="📦 APK Tech Stack Detector")
    parser.add_argument("apk", help="Path to the APK file")
    parser.add_argument("-o", "--output", help="Decompile output directory", default="/tmp/decompiled_apk")
    parser.add_argument("-s", "--signatures", help="Path to tech_stacks.json", default="tech_stacks.json")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output for matches")
    args = parser.parse_args()

    if not os.path.isfile(args.apk):
        print(f"[✘] APK file not found: {args.apk}")
        return

    print("[*] Loading tech stack signatures...")
    signatures = load_signatures(args.signatures)

    print("[*] Running apktool to decompile the APK...")
    run_apktool(args.apk, args.output)

    print("[*] Detecting tech stacks used in the APK...")
    stacks = detect_tech_stack(args.output, signatures, verbose=args.verbose)

    print("\n[+] Detected Tech Stacks:" if stacks else "[-] No known tech stacks detected.")
    for s in stacks:
        print(f"  🔹 {s}")

    # Clean up
    try:
        shutil.rmtree(args.output)
        print(f"\n[✓] Cleaned up: removed temporary directory '{args.output}'")
    except Exception as e:
        print(f"[!] Failed to delete output directory: {e}")

if __name__ == "__main__":
    main()
