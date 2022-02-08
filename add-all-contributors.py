import subprocess
import shlex
import sys


def init():
    print("Initialize all-contributors")
    subprocess.run(shlex.split("npx all-contributors-cli init"), shell=True)


def check(dryrun=False):
    all_contributors_check_result = subprocess.run(
        shlex.split("npx all-contributors-cli check"),
        shell=True,
        stdout=subprocess.PIPE,
    ).stdout.decode("utf-8")
    missing_contributors = all_contributors_check_result.replace(
        "Missing contributors in .all-contributorsrc:\n", ""
    ).strip()
    if missing_contributors in ["", "dependabot[bot]"]:  # ignore dependabot[bot]
        print("No missing contributors")
        return
    default_contribution_type = "code"  # default contribution type
    contributors_to_add = missing_contributors.split(", ")
    if "dependabot[bot]" in contributors_to_add:
        contributors_to_add.remove("dependabot[bot]")  # ignore dependabot[bot]

    print("Update .all-contributorsrc to include all contributors read from Github")
    for contributor in contributors_to_add:
        command = (
            f"npx all-contributors-cli add {contributor} {default_contribution_type}"
        )
        if not dryrun:
            print("run: " + command)
            subprocess.run(shlex.split(command), shell=True)
        else:
            print("dryrun: " + command)


def generate():
    print("Update README.md to generate table of contributors")
    subprocess.run(shlex.split("npx all-contributors-cli generate"), shell=True)
    print("Done!")


def main():
    command = sys.argv[1] if len(sys.argv) > 1 else "help"
    # execute command
    if command == "init":
        init()
        check()
        generate()
    elif command == "help":
        print(
            """
        Commands:
        init: initialize all-contributors for the first time (will generate .all-contributorsrc)
         - python add-all-contributors.py init
        add: add missing contributors (when you already have .all-contributorsrc)
         - python add-all-contributors.py add
        dryrun: dryrun add missing contributors (test without adding)
         - python add-all-contributors.py dryrun
        """
        )
    elif command == "add":
        check()
        generate()
    elif command == "dryrun":
        check(True)
    else:
        print("Unknown command: " + command)
        exit(1)


if __name__ == "__main__":
    main()
