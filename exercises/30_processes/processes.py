"""Exercise 30: Processes.

The subprocess module (portable, the idiomatic choice) versus os.fork/exec
(POSIX-only, the low-level mechanism subprocess is built on).
"""

import os
import subprocess
import sys


def main() -> None:
    # --- subprocess.run: the standard way to launch and wait for a process ---
    result = subprocess.run(
        [sys.executable, "-c", "print('hello from a subprocess')"],
        capture_output=True,
        text=True,
        check=True,
    )
    print(f"stdout: {result.stdout.strip()}")
    print(f"returncode: {result.returncode}")

    # --- Piping one process's stdout into another's stdin ---
    p1 = subprocess.Popen(
        [sys.executable, "-c", "print('one\\ntwo\\nthree')"], stdout=subprocess.PIPE
    )
    assert p1.stdout is not None
    p2 = subprocess.run(
        [sys.executable, "-c", "import sys; print(len(sys.stdin.readlines()))"],
        stdin=p1.stdout,
        capture_output=True,
        text=True,
    )
    p1.stdout.close()  # allow p1 to receive SIGPIPE if p2 exits early
    print(f"piped line count: {p2.stdout.strip()}")

    # --- Capturing a non-zero exit without raising ---
    failed = subprocess.run([sys.executable, "-c", "import sys; sys.exit(3)"])
    print(f"failed.returncode: {failed.returncode}")

    # --- check=True raises CalledProcessError on non-zero exit ---
    try:
        subprocess.run([sys.executable, "-c", "import sys; sys.exit(1)"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"caught CalledProcessError: returncode={e.returncode}")

    # --- os.fork()/os.wait(): POSIX-only, the low-level primitive ---
    # subprocess uses fork+exec (or posix_spawn) under the hood on POSIX;
    # this shows what that looks like directly.
    if hasattr(os, "fork"):
        pid = os.fork()
        if pid == 0:
            # Child process: this branch runs ONLY here, with a copy of the
            # parent's memory at the moment of fork().
            os.write(1, b"  child: hello from the child process\n")
            os._exit(0)  # os._exit skips cleanup handlers -- correct in a child
        else:
            # Parent process: pid is the child's process ID.
            _, status = os.waitpid(pid, 0)
            print(f"  parent: child exited with status {os.WEXITSTATUS(status)}")
    else:
        print("  os.fork() unavailable on this platform (Windows)")


if __name__ == "__main__":
    main()
